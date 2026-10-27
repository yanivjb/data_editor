"""Check that audit_archive.py finds the problems planted in tests/examples.

Run from the repository root:  python3 tests/test_audit.py
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent / "skills/amnat-reproducibility/scripts/audit_archive.py"

# example -> (item IDs that must be found, item IDs that must not be found)
EXPECTED = {
    "clean": (set(), {"CODE-13", "CODE-2", "DATA-1", "DOC-1"}),
    "beetles": ({"DOC-2", "DATA-3"}, {"CODE-13", "CODE-2", "GUI-1"}),
    "lizards": (
        {"DOC-1", "CODE-1", "CODE-2", "CODE-13", "DATA-2", "DATA-5", "DATA-8", "DATA-11",
         "GUI-1", "SENS-1", "ARCH-5"},
        {"DATA-10"},
    ),
    "drift": ({"CODE-13", "DOC-2"}, set()),
    "languages": ({"CODE-2", "CODE-13", "DATA-1"}, set()),
}
# example -> files that must (True) or must not (False) get a CODE-13 seed finding
SEED_FILES = {
    "languages": {
        "code/unseeded.jl": True, "code/seeded.jl": False,
        "code/unseeded.wl": True, "code/seeded.wl": False,
        "code/unseeded.cpp": True, "code/seeded.cpp": False,
        "code/analysis.m": True, "code/model.stan": False,
    },
    "drift": {"slim/selection.slim": True, "slim/run_sweeps.sh": True},
}


def audit(example):
    out = subprocess.run([sys.executable, str(AUDIT), str(ROOT / "examples" / example), "--json"],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)["findings"]


def main():
    failures = []
    for example, (must, must_not) in EXPECTED.items():
        findings = audit(example)
        if example == "clean" and findings:
            failures.append(f"clean: expected no findings, got {[f['item'] for f in findings]}")
        found = {f["item"] for f in findings}
        for item in sorted(must - found):
            failures.append(f"{example}: missing {item}")
        for item in sorted(must_not & found):
            failures.append(f"{example}: unexpected {item}")
        seeds = {f["where"].split(":")[0] for f in findings if f["item"] == "CODE-13" and f["where"]}
        for path, flagged in SEED_FILES.get(example, {}).items():
            if (path in seeds) != flagged:
                failures.append(f"{example}: {path} seed finding should be {flagged}")
        # The audit report must never include the manuscript folder.
        if any((f["where"] or "").startswith("ms_files") for f in findings):
            failures.append(f"{example}: scanned ms_files/")
    for f in failures:
        print("FAIL", f)
    print(f"{len(failures)} failure(s)")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
