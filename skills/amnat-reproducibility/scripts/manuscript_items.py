#!/usr/bin/env python3
"""List the figures, tables, and numeric statements in a manuscript.

Used to build the traceability table that links each reported result to the code
that produces it. Reads .docx, .tex, .md, .qmd, .Rmd, and .txt with the Python
standard library, and .pdf if `pdftotext` (poppler) is installed.

Usage:
    python3 manuscript_items.py PATH [PATH ...] [--out ITEMS.md] [--text FULL.txt]

PATH may be a file or a folder such as ms_files/; folders are searched for
supported files.
"""

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from html import unescape
from pathlib import Path

TEXT_EXT = {".tex", ".md", ".qmd", ".rmd", ".txt"}
SUPPORTED = TEXT_EXT | {".docx", ".pdf"}
OTHER_ITEMS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".svg", ".eps", ".ps", ".csv", ".xlsx", ".xls", ".pptx"}

LABEL = re.compile(r"\b(Fig(?:ure)?s?\.?|Tables?|Appendix)\s+(S?\d+[A-Za-z]?|[A-Z]\d*)\b")
CAPTION = re.compile(r"^\s*(Fig(?:ure)?\.?|Table)\s+(S?\d+[A-Za-z]?)\s*[.:|—-]")
NUMERIC = re.compile(
    r"\d+\.\d+|\d+(?:\.\d+)?\s*%|\bp\s*[<=>]|\b(?:CI|HPDI|SE|SD|df|n)\s*[=:]|"
    r"\b\d+\s*(?:of|out of)\s+\d+\b|\bR\^?2\b|[±]"
)
SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")


def docx_paragraphs(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    paragraphs = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S):
        p = re.sub(r"<w:tab/>", "\t", p)
        p = re.sub(r"<w:br/>", " ", p)
        text = "".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p))
        paragraphs.append(unescape(text))
    return paragraphs


def pdf_paragraphs(path):
    if not shutil.which("pdftotext"):
        sys.exit(f"{path}: pdftotext is not installed; export the manuscript as .docx, .md, or .txt instead.")
    result = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True)
    if result.returncode != 0:
        return []
    text = result.stdout
    return [re.sub(r"\s+", " ", block).strip() for block in re.split(r"\n\s*\n", text)]


def text_paragraphs(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".tex":
        text = re.sub(r"(?<!\\)%.*", "", text)
        # Start a new paragraph at sections, floats, and captions, and drop the markup.
        text = re.sub(r"\\(sub)*section\*?\{([^}]*)\}", r"\n\n\2\n\n", text)
        text = re.sub(r"\\(begin|end)\{(figure|table)\*?\}(\[[^\]]*\])?", "\n\n", text)
        text = re.sub(r"\\caption\{", "\n\n", text)
        text = re.sub(r"\\(begin|end)\{document\}|\\documentclass(\[[^\]]*\])?\{[^}]*\}", "\n\n", text)
    return [re.sub(r"\s+", " ", block).strip() for block in re.split(r"\n\s*\n", text)]


def paragraphs(path):
    ext = path.suffix.lower()
    if ext == ".docx":
        return docx_paragraphs(path)
    if ext == ".pdf":
        return pdf_paragraphs(path)
    return text_paragraphs(path)


def collect(paths):
    """Return (documents to read, other files to list) from files and folders."""
    docs, others = [], []
    for p in paths:
        if p.is_dir():
            for f in sorted(p.rglob("*")):
                ext = f.suffix.lower()
                if not f.is_file() or f.name.startswith(("~$", ".")):
                    continue
                if ext == ".pdf" and not shutil.which("pdftotext"):
                    others.append(f)  # may be a figure; cannot read text without pdftotext
                elif ext in SUPPORTED:
                    docs.append(f)
                elif ext in OTHER_ITEMS:
                    others.append(f)
        elif p.suffix.lower() in SUPPORTED:
            docs.append(p)
        else:
            sys.exit(f"Unsupported file type: {p}")
    return docs, others


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", type=Path, nargs="+")
    ap.add_argument("--out", type=Path, help="write the item list here instead of stdout")
    ap.add_argument("--text", type=Path, help="also write the full extracted text here")
    args = ap.parse_args()

    out, full_text = [], []
    docs, others = collect(args.paths)
    for f in docs:
        paras = [p for p in paragraphs(f) if p.strip()]
        if f.suffix.lower() == ".pdf" and len(paras) < 5:
            others.append(f)  # unreadable or mostly graphics: treat as a figure file
            continue
        full_text += [f"===== {f} =====", *paras, ""]
        captions = [(i, p) for i, p in enumerate(paras, 1) if CAPTION.match(p)]
        mentions = {}
        for p in paras:
            for kind, num in LABEL.findall(p):
                key = f"{'Figure' if kind.lower().startswith('fig') else kind.rstrip('s').capitalize()} {num}"
                mentions[key] = mentions.get(key, 0) + 1
        numeric = [
            (i, s.strip())
            for i, p in enumerate(paras, 1)
            if not CAPTION.match(p)
            for s in SENTENCE.split(p)
            if NUMERIC.search(s)
        ]
        out += [f"# {f}", "", f"{len(paras)} paragraphs.", "", "## Captions", ""]
        out += [f"- para {i}: {p[:200]}" for i, p in captions] or ["- none found"]
        out += ["", "## Figure and table mentions", ""]
        out += [f"- {k}: {n}" for k, n in sorted(mentions.items())] or ["- none found"]
        out += ["", "## Sentences with reported numbers", ""]
        out += [f"- para {i}: {s[:300]}" for i, s in numeric] or ["- none found"]
        out.append("")

    if others:
        out += ["# Figure, table, and other files", "", "Match each to its manuscript number.", ""]
        out += [f"- {f}" for f in others] + [""]
    report = "\n".join(out)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(report)
    if args.text:
        args.text.write_text("\n".join(full_text), encoding="utf-8")
        print(f"Wrote {args.text}")


if __name__ == "__main__":
    main()
