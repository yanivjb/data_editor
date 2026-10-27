# Test projects

Small made-up projects with planted problems. `test_audit.py` checks the scripted
part (`audit_archive.py`); the answer keys below are for trying the whole skill in
Claude Code or Codex and checking the agent's report by hand.

```sh
python3 tests/test_audit.py
```

## Answer keys for agent trials

**beetles** (Python, `.docx` manuscript, figures in `ms_files/`)
- Results: "45.3% under heat" is a **mismatch**; the code gives 43.3%.
- Results: "p = 0.43" (t-test on mass) is **not found in code**.
- Table 1, 61.7%, the difference 0.183 and its CI: **match** (seeded bootstrap).
- Figure 1 is a design diagram: **not computational**, after asking the author.
- Figure 2 in `ms_files/` was restyled: **edited after code**, data content matches
  `outputs/fig2.png`.
- README lacks a citation, who collected the data, and versions; the difference
  is printed to the console rather than saved.

**lizards** (Python, `.tex` manuscript, Excel-only data)
- The agent should ask the privacy and sensitive-data questions first: the data
  hold exact GPS points of an endangered lizard (`SENS`).
- `os.chdir` to an absolute path; Excel only; spaces in names; `escaped` in a
  numeric column; unseeded permutation test, so p = 0.006 can only match
  approximately; the ANOVA was run in Prism (`GUI`), so F and its p are not
  reproducible; Figure 1 is a photo (**not computational**); no code makes Figure 2.

**drift** (Python and SLiM, `.md` manuscript)
- Table 1: **match** (seeded).
- Figure 1: **not found in code** (no plotting code).
- SLiM sweeps (412 generations, Figure 2): about 3 days on a cluster, no seed, no
  archived outputs, `results/` missing: **not rerun**, with a `CODE-12` finding and
  an offer to set up quick and full modes. `slim` may not be installed.

**languages**: one file per language (Julia, MATLAB, Mathematica, C++, Stan,
Snakemake), seeded and unseeded, for the scan only.

**review_notes**: a README that mixes review notes into reader-facing text
(a `TODO(author)`, checklist IDs in headings, "author-confirmed", a link to
`../reproducibility_review/runlog.md`). The scan should flag both placeholders and review
notes; an agent fixing it should move the notes to `AUTHOR_TODO.md`.

**clean**: should give no findings, including from the review's own scratch
folder (`reproducibility_review/work/`), which the scan must skip.
