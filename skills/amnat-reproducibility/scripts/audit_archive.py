#!/usr/bin/env python3
"""Mechanical scan of a project against The American Naturalist archiving checklist.

Finds leads for a human or agent to check: it pattern-matches files, so expect some
false positives and misses. Item IDs refer to references/amnat-checklist.md.
Uses only the Python standard library.

Usage:
    python3 audit_archive.py PROJECT_DIR [--out REPORT.md] [--json]
"""

import argparse
import csv
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

SKIP_DIRS = {
    ".git", ".hg", ".svn", "renv", "packrat", "node_modules", ".venv", "venv",
    "env", "__pycache__", ".ipynb_checkpoints", ".Rproj.user", ".quarto",
    ".claude", ".agents", ".codex",
}
CODE_EXT = {".r", ".rmd", ".qmd", ".py", ".ipynb", ".m", ".jl", ".sh", ".do", ".sas"}
TABLE_EXT = {".csv", ".tsv"}
EXCEL_EXT = {".xlsx", ".xlsm", ".xls", ".ods"}
OTHER_DATA_EXT = {
    ".rds", ".rdata", ".rda", ".sav", ".dta", ".mat", ".h5", ".hdf5", ".feather",
    ".parquet", ".json", ".txt", ".dat",
}
CLUTTER_NAMES = {".rhistory", ".ds_store", "thumbs.db", ".rdata", ".rapp.history"}
CLUTTER_DIRS = {".rproj.user", "__pycache__", ".ipynb_checkpoints", ".quarto"}
LOCKFILES = {
    "renv.lock", "requirements.txt", "environment.yml", "environment.yaml",
    "pyproject.toml", "poetry.lock", "pipfile", "pipfile.lock", "description",
    "manifest.toml", "project.toml",
}
MISSING_TOKENS = {
    "", "NA", "na", "N/A", "n/a", "NaN", "nan", ".", "-", "?", "-999", "-9999",
    "null", "NULL", "None", "none", "missing",
}
MAX_ROWS = 200_000

PKG_LOAD = re.compile(
    r"^\s*(library|require|requireNamespace|suppressPackageStartupMessages|"
    r"pacman::p_load|p_load)\s*\(|^\s*(import|from)\s+\w"
)
DATA_READ = re.compile(
    r"\b(read\.csv2?|read\.table|read\.delim|read_csv2?|read_tsv|read_delim|"
    r"read_excel|read_xlsx|read_xls|read\.xlsx|fread|readRDS|read_rds|load|"
    r"pd\.read_\w+|np\.loadtxt|np\.genfromtxt|np\.load|xlsread|readtable|"
    r"readmatrix|csvread)\s*\("
)
READ_PATH = re.compile(
    DATA_READ.pattern + r"\s*(?:file\s*=\s*|path\s*=\s*)?[\"']([^\"']+)[\"']"
)
HERE_PATH = re.compile(r"\bhere(?:::here)?\s*\(\s*((?:[\"'][^\"']+[\"']\s*,?\s*)+)\)")
EXCEL_READ = re.compile(r"\b(read_excel|read_xlsx|read_xls|read\.xlsx|xlsread|pd\.read_excel)\s*\(")
SETWD = re.compile(r"\bsetwd\s*\(|\bos\.chdir\s*\(|^\s*cd\s+[\"']?[/~]")
ABS_PATH = re.compile(r"[\"'](/Users/|/home/|/Volumes/|/mnt/|~/|[A-Za-z]:[\\/])")
RM_ALL = re.compile(r"\brm\s*\(\s*list\s*=\s*ls\s*\(")
INSTALL = re.compile(r"\binstall\.packages\s*\(|\bpip\s+install\b|remotes::install|devtools::install")
STOCHASTIC = re.compile(
    r"\b(sample|sample_n|slice_sample|rnorm|runif|rbinom|rpois|rbeta|rgamma|rexp|"
    r"rmultinom|rnbinom|rlnorm|boot|bootMer|brm|stan|sampling|cmdstan\w*|MCMCglmm|"
    r"jags\w*|run\.jags|simulate|replicate|kmeans|randomForest|ranger|"
    r"train_test_split|shuffle|permutation)\s*\(|np\.random\.|\brandom\.\w+\(|"
    r"default_rng\s*\(|\.sample\s*\(|\brand[ni]?\s*\("
)
SEED = re.compile(
    r"\bset\.seed\s*\(|\bseed\s*=|np\.random\.seed\s*\(|random\.seed\s*\(|"
    r"default_rng\s*\(\s*\d|RandomState\s*\(\s*\d|torch\.manual_seed|\brng\s*\(\s*\d|"
    r"RNGkind\s*\("
)
FIG_TAB = re.compile(r"\b(fig(ure)?|tab(le)?|appendix|supp\w*)\.?\s*[A-Z]?\d", re.IGNORECASE)
COLUMN_NAME_OK = re.compile(r"^[A-Za-z][A-Za-z0-9_.]*$")
NUMBER = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$")

README_SECTIONS = [
    ("citation", re.compile(r"citation|cite|doi\b|reference", re.I)),
    ("authors and contact", re.compile(r"author|contact|e-?mail|orcid", re.I)),
    ("study summary", re.compile(r"summary|abstract|overview|about th|description of the study", re.I)),
    ("who collected data / wrote code", re.compile(r"collected|responsib|wrote|written by|data collection", re.I)),
    ("files and variables", re.compile(r"\bfiles?\b|folder|variable|column|codebook", re.I)),
    ("software versions", re.compile(r"version|sessioninfo|session info|dependenc|package", re.I)),
]


class Audit:
    def __init__(self, root):
        self.root = root
        self.findings = []
        self.inventory = defaultdict(list)

    def add(self, item, level, message, where=None):
        self.findings.append({"item": item, "level": level, "where": where, "message": message})

    def rel(self, path, line=None):
        r = path.relative_to(self.root).as_posix()
        return f"{r}:{line}" if line else r


def walk(root):
    for path in sorted(root.rglob("*")):
        parts = path.relative_to(root).parts
        if any(p in SKIP_DIRS for p in parts[:-1]) or (path.is_dir() and path.name in SKIP_DIRS):
            continue
        yield path


def code_lines(path):
    """Return (line_no, text, is_comment) for a script, notebook, or Quarto/R Markdown file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".ipynb":
        try:
            cells = json.loads(text).get("cells", [])
        except json.JSONDecodeError:
            return []
        lines, n = [], 0
        for cell in cells:
            src = cell.get("source", [])
            src = src.splitlines() if isinstance(src, str) else [s.rstrip("\n") for s in src]
            for s in src:
                n += 1
                if cell.get("cell_type") == "code":
                    lines.append((n, s, s.lstrip().startswith("#")))
        return lines
    comment = "%" if path.suffix.lower() == ".m" else "#"
    in_chunk = path.suffix.lower() not in {".rmd", ".qmd"}
    out = []
    for n, s in enumerate(text.splitlines(), 1):
        if not in_chunk:
            if re.match(r"^\s*```+\s*\{", s):
                in_chunk = True
            elif s.strip():
                out.append((n, s, True))  # prose in Quarto/R Markdown documents the code
            continue
        if re.match(r"^\s*```+\s*$", s) and path.suffix.lower() in {".rmd", ".qmd"}:
            in_chunk = False
            continue
        out.append((n, s, s.lstrip().startswith(comment) or s.lstrip().startswith("#|")))
    return out


def strip_comment(s):
    return re.sub(r"(^|\s)#.*$", "", s)


def check_code(audit, path, all_files):
    lines = code_lines(path)
    if not lines:
        return
    first_read, late_loads = None, []
    stochastic, seeded = None, False
    n_comments = n_code = n_labels = 0
    for n, s, is_comment in lines:
        if is_comment:
            n_comments += 1
            if FIG_TAB.search(s):
                n_labels += 1
            continue
        code = strip_comment(s)
        if not code.strip():
            continue
        n_code += 1
        if SETWD.search(code):
            audit.add("CODE-2", "REQ", "Working directory set in code; use paths relative to the project root.", audit.rel(path, n))
        if ABS_PATH.search(code):
            audit.add("CODE-2", "REQ", f"Absolute path: `{code.strip()[:100]}`", audit.rel(path, n))
        if RM_ALL.search(code):
            audit.add("CODE-6", "REC", "`rm(list = ls())` does not give a clean session; test with a fresh process instead.", audit.rel(path, n))
        if INSTALL.search(code):
            audit.add("DOC-2", "REQ", "Script installs packages; list these in the README's software section.", audit.rel(path, n))
        if EXCEL_READ.search(code):
            audit.add("DATA-5", "REQ", "Code reads Excel; each data sheet must also be archived as CSV (ideally read from CSV).", audit.rel(path, n))
        if DATA_READ.search(code) and first_read is None:
            first_read = n
        if PKG_LOAD.search(code) and first_read is not None:
            late_loads.append(n)
        if STOCHASTIC.search(code) and stochastic is None:
            stochastic = n
        if SEED.search(code):
            seeded = True
        for m in READ_PATH.finditer(code):
            check_read_target(audit, path, n, m.group(m.lastindex), all_files)
        for m in HERE_PATH.finditer(code):
            parts = re.findall(r"[\"']([^\"']+)[\"']", m.group(1))
            target = "/".join(parts)
            if Path(target).suffix and DATA_READ.search(code):
                check_read_target(audit, path, n, target, all_files, from_root=True)
    if late_loads:
        audit.add("CODE-1", "REQ", f"Packages loaded after data import (lines {', '.join(map(str, late_loads[:8]))}); load packages first.", audit.rel(path, late_loads[0]))
    if stochastic and not seeded:
        audit.add("CODE-13", "REC", "Stochastic function used but no random seed found.", audit.rel(path, stochastic))
    if n_code > 20 and n_comments / max(n_code, 1) < 0.05:
        audit.add("CODE-3", "REQ", f"Few comments ({n_comments} comment lines for {n_code} code lines); explain the purpose of each block.", audit.rel(path))
    if n_code > 20 and n_labels == 0:
        audit.add("CODE-4", "REQ", "No comments or headers mention figure or table numbers.", audit.rel(path))


def check_read_target(audit, script, line, target, all_files, from_root=False):
    if re.match(r"^(https?|ftp)://", target) or "{" in target or "%" in target:
        return
    if ABS_PATH.match('"' + target):
        return  # already reported as an absolute path
    candidates = [audit.root / target] if from_root else [script.parent / target, audit.root / target]
    if not any(c.resolve() in all_files for c in candidates):
        audit.add("DATA-1", "REQ", f"Code reads `{target}`, which is not in the project.", audit.rel(script, line))


def sniff_reader(path, handle):
    if path.suffix.lower() == ".tsv":
        return csv.reader(handle, delimiter="\t")
    sample = handle.read(20_000)
    handle.seek(0)
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    if dialect.delimiter == ";":
        return None
    return csv.reader(handle, dialect)


def check_table(audit, path, documented_text):
    with path.open(newline="", encoding="utf-8-sig", errors="replace") as fh:
        reader = sniff_reader(path, fh)
        if reader is None:
            audit.add("DATA-4", "REQ", "File appears to be semicolon-delimited; save as comma-separated.", audit.rel(path))
            return
        try:
            header = next(reader)
        except StopIteration:
            audit.add("DATA-1", "REQ", "Empty data file.", audit.rel(path))
            return
        kinds = [Counter() for _ in header]
        examples = [defaultdict(list) for _ in header]
        missing = Counter()
        n_rows = ragged = 0
        for row in reader:
            n_rows += 1
            if n_rows > MAX_ROWS:
                break
            if len(row) != len(header):
                ragged += 1
            for i, value in enumerate(row[: len(header)]):
                v = value.strip()
                if v in MISSING_TOKENS:
                    missing[v if v else "(blank)"] += 1
                    continue
                kind = "number" if NUMBER.match(v.replace(",", "")) else "text"
                kinds[i][kind] += 1
                if len(examples[i][kind]) < 3:
                    examples[i][kind].append(v)
    audit.inventory["data_tables"].append(f"{audit.rel(path)} ({n_rows:,} rows x {len(header)} columns)")
    bad = [h for h in header if not COLUMN_NAME_OK.match(h.strip())]
    long_names = [h for h in header if COLUMN_NAME_OK.match(h.strip()) and len(h.strip()) > 10]
    dupes = [h for h, c in Counter(header).items() if c > 1]
    if bad:
        audit.add("DATA-8", "REQ", f"Column names with spaces, special characters, or blanks: {fmt_list(bad)}", audit.rel(path))
    if long_names:
        audit.add("DATA-8", "REQ", f"Column names longer than 10 characters (journal preference): {fmt_list(long_names)}", audit.rel(path))
    if dupes:
        audit.add("DATA-8", "REQ", f"Duplicate column names: {fmt_list(dupes)}", audit.rel(path))
    if ragged:
        audit.add("DATA-10", "REC", f"{ragged} rows have a different number of fields from the header.", audit.rel(path))
    for i, h in enumerate(header):
        k = kinds[i]
        if k["number"] and k["text"] and min(k["number"], k["text"]) / (k["number"] + k["text"]) > 0.001:
            audit.add("DATA-11", "REC", f"Column `{h}` mixes numbers ({k['number']}) and text ({k['text']}), e.g. {fmt_list(examples[i]['text'])}", audit.rel(path))
    codes = [c for c in missing if c != "NA"]
    if codes:
        detail = ", ".join(f"`{c}` x{missing[c]}" for c in codes)
        audit.add("DATA-12", "REC", f"Missing values coded other than `NA`: {detail}. State the code(s) in the README.", audit.rel(path))
    if documented_text:
        undocumented = [h for h in header if h.strip() and not re.search(r"(?<![A-Za-z0-9_])" + re.escape(h.strip()) + r"(?![A-Za-z0-9_])", documented_text)]
        if undocumented:
            audit.add("DATA-3", "REQ", f"{len(undocumented)} of {len(header)} columns not mentioned in README or codebook: {fmt_list(undocumented)}", audit.rel(path))


def excel_sheets(path):
    if path.suffix.lower() not in {".xlsx", ".xlsm"}:
        return None
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("xl/workbook.xml").decode("utf-8", "replace")
    except (zipfile.BadZipFile, KeyError, OSError):
        return None
    return re.findall(r"<(?:\w+:)?sheet\b[^>]*\bname=\"([^\"]+)\"", xml)


def check_excel(audit, path, csv_stems):
    sheets = excel_sheets(path)
    label = f"{audit.rel(path)}" + (f" (sheets: {', '.join(sheets)})" if sheets else "")
    audit.inventory["excel"].append(label)
    stem = norm(path.stem)
    names = [norm(s) for s in sheets] if sheets else []
    matched = [s for s in csv_stems if stem in s or s in stem or any(n and n in s for n in names)]
    if not matched:
        audit.add("DATA-5", "REQ", "Excel file with no matching CSV export; save each data worksheet as its own CSV.", audit.rel(path))
    elif sheets and len(sheets) > len(matched):
        audit.add("DATA-5", "REQ", f"{len(sheets)} worksheets but {len(matched)} matching CSV file(s); check every data sheet is exported.", audit.rel(path))


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def fmt_list(items, n=8):
    items = [f"`{i}`" for i in items]
    return ", ".join(items[:n]) + (f", ... (+{len(items) - n})" if len(items) > n else "")


def check_readme(audit, files):
    readmes = [f for f in files if f.parent == audit.root and f.stem.lower() == "readme"]
    if not readmes:
        nested = [f for f in files if f.stem.lower() == "readme"]
        msg = "No README in the project root."
        if nested:
            msg += f" Found: {fmt_list([audit.rel(f) for f in nested])}"
        audit.add("DOC-1", "REQ", msg)
        return None, ""
    readme = readmes[0]
    if len(readmes) > 1:
        audit.add("DOC-1", "REQ", f"Several root READMEs: {fmt_list([audit.rel(f) for f in readmes])}; keep one.")
    if readme.suffix.lower() not in {".md", ".txt", ".rtf", ""}:
        audit.add("DOC-1", "REQ", f"README format `{readme.suffix}`; use .md or .txt.", audit.rel(readme))
    text = readme.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    found = []
    for name, pattern in README_SECTIONS:
        hit = next((i for i, s in enumerate(lines, 1) if pattern.search(s)), None)
        found.append((name, hit))
        if hit is None:
            audit.add("DOC-2", "REQ", f"README has no recognisable '{name}' section.", audit.rel(readme))
    hits = [h for _, h in found if h]
    if hits != sorted(hits):
        order = ", ".join(f"{n} (line {h})" for n, h in found if h)
        audit.add("DOC-2", "REQ", f"README sections may be out of the required order: {order}.", audit.rel(readme))
    if "TODO" in text:
        audit.add("DOC-2", "REQ", f"README still contains {text.count('TODO')} TODO placeholder(s).", audit.rel(readme))
    return readme, text


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("--out", type=Path, help="write the Markdown report here instead of stdout")
    ap.add_argument("--json", action="store_true", help="print findings as JSON")
    args = ap.parse_args()
    root = args.project.resolve()
    if not root.is_dir():
        sys.exit(f"Not a directory: {root}")

    audit = Audit(root)
    files = [p for p in walk(root) if p.is_file()]
    file_set = {p.resolve() for p in files}

    for p in walk(root):
        name = p.name.lower()
        if (p.is_file() and (name in CLUTTER_NAMES or name.startswith("~$"))) or (p.is_dir() and name in CLUTTER_DIRS):
            audit.add("ARCH-5", "REC", "Workspace or system clutter; leave out of the archive.", audit.rel(p))
    for d in root.iterdir():
        if d.is_dir() and d.name.lower() in CLUTTER_DIRS:
            audit.add("ARCH-5", "REC", "Workspace or system clutter; leave out of the archive.", audit.rel(d))

    readme, readme_text = check_readme(audit, files)
    codebooks = [f for f in files if f.suffix.lower() in TABLE_EXT and re.search(r"codebook|data.?dictionary|metadata", f.stem, re.I)]
    documented = readme_text + "\n".join(f.read_text(encoding="utf-8", errors="replace") for f in codebooks)

    if not any(f.name.lower().startswith(("license", "licence")) for f in files) and not re.search(r"licen[cs]e|CC0|CC[- ]BY|MIT\b|GPL", readme_text):
        audit.add("DOC-5", "REC", "No license file or license statement (not needed if depositing on Dryad).")
    locks = [audit.rel(f) for f in files if f.name.lower() in LOCKFILES]
    audit.inventory["environment"] = locks
    if not locks and not re.search(r"sessionInfo|R version \d|Python \d|pip freeze|==\d", readme_text):
        audit.add("DOC-2", "REQ", "No package versions found (no sessionInfo/pip freeze output in README, no renv.lock or requirements.txt).")

    csv_stems = [norm(f.stem) for f in files if f.suffix.lower() in TABLE_EXT]
    for f in files:
        ext = f.suffix.lower()
        if ext in CODE_EXT:
            audit.inventory["code"].append(audit.rel(f))
            check_code(audit, f, file_set)
        elif ext in TABLE_EXT:
            if f not in codebooks:
                check_table(audit, f, documented)
            if " " in f.name:
                audit.add("DATA-2", "REQ", "File name contains spaces; use a short name without spaces.", audit.rel(f))
        elif ext in EXCEL_EXT:
            check_excel(audit, f, csv_stems)
            if " " in f.name:
                audit.add("DATA-2", "REQ", "File name contains spaces; use a short name without spaces.", audit.rel(f))
        elif ext in OTHER_DATA_EXT and f != readme and not f.name.lower().startswith(("license", "licence", "requirements")):
            audit.inventory["other_data"].append(audit.rel(f))
        if readme_text and (ext in CODE_EXT | TABLE_EXT | EXCEL_EXT) and f.name not in readme_text:
            audit.add("DOC-2", "REQ", "File not listed in README.", audit.rel(f))

    if not audit.inventory["code"]:
        audit.add("CODE-1", "REQ", "No analysis code found; the journal requires code for all reported results.")
    if not audit.inventory["data_tables"]:
        audit.add("DATA-4", "REQ", "No CSV data files found.")
    if audit.inventory["other_data"]:
        audit.add("DATA-4", "REQ", f"Non-CSV data or intermediate files: {fmt_list(audit.inventory['other_data'])}. Raw data must also be CSV; intermediates are fine if documented.")

    if args.json:
        print(json.dumps({"root": str(root), "findings": audit.findings, "inventory": audit.inventory}, indent=2))
        return
    report = render(audit, readme)
    if args.out:
        out = args.out if args.out.is_absolute() else root / args.out
        out.write_text(report, encoding="utf-8")
        print(f"Wrote {out} ({len(audit.findings)} findings)")
    else:
        print(report)


def render(audit, readme):
    order = {"DOC": 0, "CODE": 1, "DATA": 2, "ARCH": 3}
    def key(f):
        prefix, num = f["item"].split("-")
        return (f["level"] != "REQ", order[prefix], int(num))
    findings = sorted(audit.findings, key=key)
    req = sum(f["level"] == "REQ" for f in findings)
    out = [
        f"# Reproducibility audit: `{audit.root.name}`",
        "",
        "Automated scan against The American Naturalist archiving checklist. These are",
        "leads to verify, not a verdict: the scan cannot run your code, judge whether",
        "comments are useful, or check that the archive reproduces the paper.",
        "",
        f"**{req} required-item leads, {len(findings) - req} recommended-item leads.**",
        "",
        "## Inventory",
        "",
        f"- README: {audit.rel(readme) if readme else 'none'}",
        f"- Code: {fmt_list(audit.inventory['code']) or 'none'}",
        f"- CSV/TSV data: {'; '.join(audit.inventory['data_tables']) or 'none'}",
        f"- Excel: {'; '.join(audit.inventory['excel']) or 'none'}",
        f"- Other data/intermediate files: {fmt_list(audit.inventory['other_data']) or 'none'}",
        f"- Environment files: {fmt_list(audit.inventory['environment']) or 'none'}",
        "",
        "## Findings",
        "",
        "| Item | Level | Where | Finding |",
        "|------|-------|-------|---------|",
    ]
    for f in findings:
        msg = f["message"].replace("|", "\\|")
        out.append(f"| {f['item']} | {f['level']} | {f['where'] or ''} | {msg} |")
    out += [
        "",
        "## Not checked by this scan",
        "",
        "- Whether the code runs to completion in a fresh session and reproduces the reported results (CODE-6).",
        "- Whether every result in the paper has its data and code here (DATA-1), and whether data are raw rather than summaries (DATA-7).",
        "- Citation of adapted code and packages (CODE-5), and quality of comments and README descriptions.",
        "- Deposit in Dryad/Zenodo, repository metadata, and the private reviewer link (ARCH-1 to ARCH-3).",
        "",
    ]
    return "\n".join(out)


if __name__ == "__main__":
    main()
