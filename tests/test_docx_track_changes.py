"""Check docx_track_changes.py on the made-up beetle manuscript.

Run from the repository root:  python3 tests/test_docx_track_changes.py
"""
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT.parent / "skills/amnat-reproducibility/scripts/docx_track_changes.py"
DOCX = ROOT / "examples/beetles/ms_files/manuscript.docx"

GOOD = [
    {"find": "45.3% under heat", "replace": "43.3% under heat",
     "comment": "From outputs/table1.csv (heat: survival = 0.433). Was 45.3%."},
    {"find": " Body mass did not differ between treatments (t-test, p = 0.43).", "replace": ""},
    {"find": "(5000 resamples)", "insert_after": " with a fixed random seed"},
    {"find": "0.617", "replace": "0.62", "comment": "Rounded to two decimals."},
]
BAD = GOOD[:1] + [{"find": "Survival", "replace": "x"}]  # "Survival" occurs many times


def run(edits, out):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(edits, f)
    return subprocess.run([sys.executable, str(SCRIPT), str(DOCX), f.name, "--out", str(out),
                           "--author", "Test Author"], capture_output=True, text=True)


def accepted_text(xml):
    """Document text as it reads after accepting all tracked changes."""
    xml = re.sub(r"<w:del\b.*?</w:del>", "", xml, flags=re.S)
    return " ".join("".join(re.findall(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", p, re.S))
                    for p in re.findall(r"<w:p\b.*?</w:p>", xml, re.S))


def main():
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "tracked.docx"
        r = run(GOOD, out)
        if r.returncode != 0:
            failures.append(f"good edits failed: {r.stderr}")
        else:
            z = zipfile.ZipFile(out)
            doc = z.read("word/document.xml").decode()
            comments = z.read("word/comments.xml").decode()
            text = accepted_text(doc)
            checks = {
                "43.3% under heat accepted": "43.3% under heat" in text,
                "45.3% gone after accepting": "45.3%" not in text,
                "t-test sentence deleted": "t-test" not in text,
                "insertion present": "(5000 resamples) with a fixed random seed" in text,
                "table cell edited": "0.62" in text and "0.617" not in text,
                "changes attributed": 'w:author="Test Author"' in doc,
                "minimal change (no retyped words)": "<w:delText xml:space=\"preserve\">45.3%</w:delText>" in doc,
                "two comments": comments.count("<w:comment ") == 2,
                "comment text": "outputs/table1.csv" in comments,
            }
            failures += [name for name, ok in checks.items() if not ok]
            if zipfile.ZipFile(DOCX).read("word/document.xml").decode().count("<w:ins ") != 0:
                failures.append("original document was modified")
        out2 = Path(tmp) / "bad.docx"
        r = run(BAD, out2)
        if r.returncode == 0 or out2.exists():
            failures.append("ambiguous edit was not refused, or a file was written")
        r = run([{"find": "45.3% under heat", "replace": "45.3% under heat"}], Path(tmp) / "noop.docx")
        if r.returncode == 0:
            failures.append("no-op edit was not refused")
    for f in failures:
        print("FAIL", f)
    print(f"{len(failures)} failure(s)")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
