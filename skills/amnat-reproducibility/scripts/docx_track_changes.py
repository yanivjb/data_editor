#!/usr/bin/env python3
"""Apply edits to a copy of a Word document as tracked changes, with comments.

Each edit replaces, deletes, or inserts text inside one paragraph and appears in
Word as a tracked insertion and/or deletion by AUTHOR, optionally with a comment.
The original file is never modified. Uses only the Python standard library.

Usage:
    python3 docx_track_changes.py IN.docx EDITS.json --out OUT.docx [--author NAME] [--dry-run]

EDITS.json is a list of edits:

    [
      {"find": "45.3%", "replace": "43.3%",
       "context": "45.3% under heat",
       "comment": "From outputs/table1.csv (heat, survival = 0.433). Was 45.3%."},
      {"find": " all p < 0.05", "replace": ""},
      {"find": "(Table 1, Figure 2)", "insert_after": " (Appendix S7)"}
    ]

- "find" must occur exactly once in the document, or exactly once inside
  "context" when given (and "context" must occur exactly once).
- Use "replace" to replace "find" ("" deletes it), or "insert_after" to add text
  after "find" without changing it.
- Text is matched within a single paragraph, including table cells. Edits that
  cross paragraphs, fields, or existing tracked changes are refused.

All edits are checked before anything is written: if any edit cannot be applied,
no file is written and the script exits with an error.
"""

import argparse
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from html import escape, unescape
from pathlib import Path

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
COMMENTS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments"
COMMENTS_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"

PARAGRAPH = re.compile(r"<w:p\b[^>]*?(?:/>|>.*?</w:p>)", re.S)
RUN = re.compile(r"<w:r\b[^>]*?(?:/>|>.*?</w:r>)", re.S)
TEXT = re.compile(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>|<w:t\s*/>", re.S)
RPR = re.compile(r"<w:rPr\b.*?</w:rPr>|<w:rPr\s*/>", re.S)
# Allowed between adjacent runs that an edit spans
GAP_OK = re.compile(r"^(\s|<w:proofErr\b[^>]*/>|<w:bookmark(Start|End)\b[^>]*/>)*$")
# Run children we can safely rebuild: properties, text, and layout hints
RUN_CHILD_OK = re.compile(r"^(\s|<w:rPr\b.*?</w:rPr>|<w:rPr\s*/>|<w:t(\s[^>]*)?>.*?</w:t>|<w:t\s*/>|<w:lastRenderedPageBreak\s*/>)*$", re.S)
TRACKED = re.compile(r"<w:(ins|del|moveFrom|moveTo)\b.*?</w:\1>", re.S)


class EditError(Exception):
    pass


def paragraph_runs(p_xml):
    """Return the text-bearing runs of a paragraph as dicts with offsets."""
    runs, pos = [], 0
    tracked = [(m.start(), m.end()) for m in TRACKED.finditer(p_xml)]
    for m in RUN.finditer(p_xml):
        body = m.group(0)
        texts = [unescape(t.group(1) or "") for t in TEXT.finditer(body)]
        if not texts:
            continue
        text = "".join(texts)
        runs.append({
            "start": m.start(), "end": m.end(), "xml": body, "text": text,
            "from": pos, "to": pos + len(text),
            "in_tracked": any(a <= m.start() < b for a, b in tracked),
        })
        pos += len(text)
    return runs


def run_props(run_xml):
    m = RPR.search(run_xml)
    return m.group(0) if m else ""


def run_open_tag(run_xml):
    return re.match(r"<w:r\b[^>]*>", run_xml).group(0)


def text_run(open_tag, props, text):
    return f'{open_tag}{props}<w:t xml:space="preserve">{escape(text, quote=False)}</w:t></w:r>'


def deleted_run(props, text):
    return f'<w:r>{props}<w:delText xml:space="preserve">{escape(text, quote=False)}</w:delText></w:r>'


def minimal_edit(edit):
    """Shrink a replacement to the words that change, so Word shows only those.

    "brms (Bürkner 2017)" -> "brms version 2.22 (Bürkner 2017)" becomes an
    insertion of "version 2.22 " rather than deleting and retyping the phrase.
    """
    if "replace" not in edit or not edit["replace"]:
        return edit
    old = re.split(r"(\s+)", edit["find"])
    new = re.split(r"(\s+)", edit["replace"])
    i = 0
    while i < min(len(old), len(new)) and old[i] == new[i]:
        i += 1
    j = 0
    while j < min(len(old), len(new)) - i and old[-1 - j] == new[-1 - j]:
        j += 1
    prefix, old_mid = "".join(old[:i]), "".join(old[i:len(old) - j])
    new_mid = "".join(new[i:len(new) - j])
    context = edit.get("context", edit["find"])
    if old_mid and context.count(old_mid) == 1:
        return {**edit, "find": old_mid, "replace": new_mid, "context": context}
    if not old_mid and prefix and context.count(prefix) == 1:
        return {k: v for k, v in edit.items() if k != "replace"} | {"find": prefix, "insert_after": new_mid, "context": context}
    return edit


def locate(paragraphs, edit):
    """Return (paragraph index, start offset, end offset) of the edit's target."""
    find = edit["find"]
    if not find:
        raise EditError("empty 'find'")
    texts = ["".join(r["text"] for r in paragraph_runs(p)) for p in paragraphs]
    anchor = edit.get("context", find)
    if find not in anchor:
        raise EditError("'find' does not occur inside 'context'")
    hits = [(i, m.start()) for i, t in enumerate(texts) for m in re.finditer(re.escape(anchor), t)]
    if len(hits) != 1:
        where = "'context'" if "context" in edit else "'find'"
        raise EditError(f"{where} {anchor!r} occurs {len(hits)} times in single paragraphs; it must occur exactly once (add or lengthen 'context')")
    i, at = hits[0]
    offset = anchor.index(find)
    if anchor.count(find) > 1:
        raise EditError("'find' occurs more than once inside 'context'")
    return i, at + offset, at + offset + len(find)


def apply_edit(p_xml, start, end, edit, ids, author, date, comment_id):
    runs = paragraph_runs(p_xml)
    span = [r for r in runs if r["from"] < end and r["to"] > start]
    if "insert_after" in edit:
        span = [r for r in runs if r["from"] < end <= r["to"]]
    if not span:
        raise EditError("text not found in runs")
    for a, b in zip(span, span[1:]):
        if not GAP_OK.match(p_xml[a["end"]:b["start"]]):
            raise EditError("text spans a field, hyperlink boundary, or other non-text element")
    for r in span:
        inner = re.sub(r"^<w:r\b[^>]*>|</w:r>$", "", r["xml"])
        if not RUN_CHILD_OK.match(inner):
            raise EditError("text is in a run with tabs, breaks, fields, or images")
        if r["in_tracked"]:
            raise EditError("text is inside an existing tracked change; accept or reject it first")

    first, last = span[0], span[-1]
    open_tag, props = run_open_tag(first["xml"]), run_props(first["xml"])
    before = first["text"][: max(start, first["from"]) - first["from"]] if "insert_after" not in edit else first["text"][: end - first["from"]]
    after = last["text"][end - last["from"]:]
    pieces = []
    if before:
        pieces.append(text_run(open_tag, props, before))
    if comment_id is not None:
        pieces.append(f'<w:commentRangeStart w:id="{comment_id}"/>')
    attrs = f'w:author="{escape(author)}" w:date="{date}"'
    if "insert_after" in edit:
        new_text = edit["insert_after"]
    else:
        new_text = edit.get("replace", "")
        old = []
        for r in span:
            seg = r["text"][max(start, r["from"]) - r["from"]: min(end, r["to"]) - r["from"]]
            if seg:
                old.append(deleted_run(run_props(r["xml"]), seg))
        pieces.append(f'<w:del w:id="{next(ids)}" {attrs}>{"".join(old)}</w:del>')
    if new_text:
        pieces.append(f'<w:ins w:id="{next(ids)}" {attrs}>{text_run("<w:r>", props, new_text)}</w:ins>')
    if comment_id is not None:
        pieces.append(f'<w:commentRangeEnd w:id="{comment_id}"/>')
        pieces.append(f'<w:r><w:commentReference w:id="{comment_id}"/></w:r>')
    if after:
        pieces.append(text_run(run_open_tag(last["xml"]), run_props(last["xml"]), after))
    return p_xml[: first["start"]] + "".join(pieces) + p_xml[last["end"]:]


def comment_xml(cid, author, date, text):
    paras = "".join(
        f'<w:p><w:r><w:t xml:space="preserve">{escape(line, quote=False)}</w:t></w:r></w:p>'
        for line in text.splitlines() or [""]
    )
    first = paras.replace("<w:p><w:r>", "<w:p><w:r><w:annotationRef/></w:r><w:r>", 1)
    initials = "".join(w[0] for w in author.split()[:3]).upper() or "A"
    return f'<w:comment w:id="{cid}" w:author="{escape(author)}" w:date="{date}" w:initials="{initials}">{first}</w:comment>'


def add_comments_part(files, new_comments):
    if not new_comments:
        return
    if "word/comments.xml" in files:
        xml = files["word/comments.xml"].decode("utf-8")
        xml = re.sub(r"<w:comments\b([^>]*?)\s*/>", r"<w:comments\1></w:comments>", xml, count=1)
        if "</w:comments>" not in xml:
            raise SystemExit("word/comments.xml has an unexpected structure; nothing was written.")
        xml = xml.replace("</w:comments>", "".join(new_comments) + "</w:comments>", 1)
    else:
        xml = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
               f'<w:comments xmlns:w="{W_NS}">{"".join(new_comments)}</w:comments>')
        rels = files["word/_rels/document.xml.rels"].decode("utf-8")
        ids = [int(n) for n in re.findall(r'Id="rId(\d+)"', rels)]
        rel = f'<Relationship Id="rId{max(ids, default=0) + 1}" Type="{COMMENTS_REL}" Target="comments.xml"/>'
        files["word/_rels/document.xml.rels"] = rels.replace("</Relationships>", rel + "</Relationships>").encode("utf-8")
        types = files["[Content_Types].xml"].decode("utf-8")
        if "/word/comments.xml" not in types:
            override = f'<Override PartName="/word/comments.xml" ContentType="{COMMENTS_TYPE}"/>'
            files["[Content_Types].xml"] = types.replace("</Types>", override + "</Types>").encode("utf-8")
    files["word/comments.xml"] = xml.encode("utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx", type=Path)
    ap.add_argument("edits", type=Path)
    ap.add_argument("--out", type=Path, required=True, help="where to write the tracked copy")
    ap.add_argument("--author", default="Reproducibility review", help="name shown on the tracked changes")
    ap.add_argument("--dry-run", action="store_true", help="check every edit but write nothing")
    args = ap.parse_args()

    if args.out.resolve() == args.docx.resolve():
        sys.exit("--out must differ from the input file; the original is never modified.")
    edits = json.loads(args.edits.read_text(encoding="utf-8"))
    if not isinstance(edits, list):
        sys.exit("EDITS.json must contain a list of edits.")
    with zipfile.ZipFile(args.docx) as z:
        order = z.namelist()
        files = {n: z.read(n) for n in order}
    doc = files["word/document.xml"].decode("utf-8")

    used = [int(n) for n in re.findall(r'w:id="(\d+)"', doc)]
    if "word/comments.xml" in files:
        used += [int(n) for n in re.findall(r'w:id="(\d+)"', files["word/comments.xml"].decode("utf-8"))]
    counter = iter(range(max(used, default=0) + 1, 10**9))
    date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    matches = list(PARAGRAPH.finditer(doc))
    paragraphs = [m.group(0) for m in matches]
    comments, errors = [], []
    for n, edit in enumerate(edits, 1):
        try:
            if not isinstance(edit, dict) or "find" not in edit or ("replace" in edit) == ("insert_after" in edit):
                raise EditError("each edit needs 'find' and exactly one of 'replace' or 'insert_after'")
            if edit.get("replace") == edit["find"] or edit.get("insert_after") == "":
                raise EditError("edit changes nothing")
            edit = minimal_edit(edit)
            i, start, end = locate(paragraphs, edit)
            cid = next(counter) if edit.get("comment") else None
            paragraphs[i] = apply_edit(paragraphs[i], start, end, edit, counter, args.author, date, cid)
            if cid is not None:
                comments.append(comment_xml(cid, args.author, date, edit["comment"]))
            print(f"edit {n}: ok (paragraph {i + 1})")
        except EditError as e:
            errors.append(f"edit {n} ({edit.get('find', '')!r}): {e}" if isinstance(edit, dict) else f"edit {n}: {e}")
    if errors:
        for e in errors:
            print("ERROR", e, file=sys.stderr)
        sys.exit(f"{len(errors)} edit(s) could not be applied; nothing was written.")
    if args.dry_run:
        print(f"All {len(edits)} edits can be applied (dry run; nothing written).")
        return

    out, last = [], 0
    for m, new in zip(matches, paragraphs):
        out.append(doc[last:m.start()])
        out.append(new)
        last = m.end()
    out.append(doc[last:])
    files["word/document.xml"] = "".join(out).encode("utf-8")
    add_comments_part(files, comments)
    order += [n for n in files if n not in order]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED) as z:
        for name in order:
            z.writestr(name, files[name])
    print(f"Wrote {args.out}: {len(edits)} tracked edit(s), {len(comments)} comment(s), author {args.author!r}.")


if __name__ == "__main__":
    main()
