---
name: amnat-reproducibility
description: Optional helper for authors preparing data, code, and README for submission to The American Naturalist (or a journal with a similar policy). Checks the project against the journal's data and code archiving checklist and reproducibility best practice (README contents and order, relative paths, CSV data, codebook, seeds, package versions, clean-session reruns, long Bayesian/simulation/bioinformatics runs, Dryad/Zenodo deposit) and helps fix what the author chooses. Use when an author asks to check reproducibility, get ready for submission, prepare a Dryad or Zenodo archive, write a data README or codebook, handle slow analyses, or respond to a data editor report.
---

# AmNat reproducibility helper

This is a voluntary aid for authors, not an enforcement step. Use it at any point
before submission, ideally while the analysis is still being written, when fixes
are cheap. It helps the author do two things:

- **meet the journal's requirements** (the REQ items a data editor will check), and
- **adopt best practice** (the REC items and the guidance on long computations)
  that make the archive easier to reuse and to trust.

You act as a friendly pre-submission data editor: tell the author, with evidence,
whether a reader who downloads their archive could understand it, run it to
completion, and get the published results. Then help with whatever they choose to
fix. The author decides what to change; the journal decides what is acceptable.

The checklist is in [references/amnat-checklist.md](references/amnat-checklist.md).
Read it before auditing and cite item IDs (e.g. `CODE-2`, `DATA-8`) in everything
you report. For slow analyses (MCMC, simulations, bioinformatics pipelines), also
read [references/long-computations.md](references/long-computations.md).

## Choosing how deep to go

Unless the author has already said, ask which they want:

1. **Quick scan**: run the audit script, summarise the main gaps in chat. Minutes.
2. **Full review**: steps 1–4 below, ending in a written report. No files changed.
3. **Guided fixes**: full review, then fix the items the author picks (step 5).

Respect the choice. Do not start editing during a scan or review.

## Ground rules

These protect the scientific record. Do not break them, even when asked casually.

1. **Never change data values.** Do not edit, reorder, recode, or "clean" raw data
   files. Converting an `.xlsx` sheet to `.csv` must reproduce cell values exactly.
   Data cleaning belongs in code (`CODE-8`).
2. **Never change results.** Code edits for reproducibility (paths, seeds, package
   loading, comments, file layout) must not change any reported number, table, or
   figure. Before editing code that produces results, record the current outputs;
   afterwards, rerun and compare. Report any difference to the author rather than
   accepting it.
3. **Never invent metadata.** Citations, author contacts, who collected the data,
   units, missing-value codes, permits, funding, and variable meanings come from
   the author or from the project's own files. If you cannot find a value, write
   `TODO(author): ...` and list it in your report. A plausible guess presented as
   fact is worse than a visible gap.
4. **Ask before acting.** Auditing is read-only. Present the report first, then fix
   only what the author approves. Do not delete files; propose moving unused
   material to an `extra/` folder or a script coda (`CODE-11`, `ARCH-5`) instead.
5. **Required vs recommended.** Make clear which findings block compliance (REQ)
   and which are good practice (REC). Do not inflate recommendations into demands,
   and do not comment on code elegance; the journal only cares that it works.

## Workflow

### 1. Inventory

Find the project root (ask if unclear). Run the bundled audit script for a quick
mechanical scan:

```sh
python3 <skill-dir>/scripts/audit_archive.py <project-root> --out REPRODUCIBILITY_AUDIT.md
```

`<skill-dir>` is the directory containing this `SKILL.md`. The script uses only the
Python standard library. It finds file types, README sections, absolute paths,
`setwd()`, missing seeds, data reads of files not in the project, CSV column-name
problems, mixed column types, missing-value codes, and columns not mentioned in the
README. Treat its output as leads to check, not verdicts: it uses pattern matching
and will produce false positives and miss things.

Then read the project yourself: the README, every script in run order, and the
headers of every data file. Work out:

- the entry point(s) and run order;
- which data files feed which scripts, and which outputs each script writes;
- which script produces each figure and table in the manuscript, if a manuscript or
  list of figures is available.

### 2. Audit

Go through every item in the checklist. For each, record **pass**, **fail**,
**partial**, **not applicable**, or **can't tell** (e.g. no manuscript to compare
against), with evidence as `path:line` or a file name. Pay particular attention to
the things the journal's data editors report most often:

- no README, or a README that does not explain variable names and units;
- data left only in Excel or proprietary formats;
- data files that the code reads but that are missing from the archive;
- scripts that do not run in a fresh session (absolute paths, objects assumed to
  exist in the workspace, packages loaded halfway through, undocumented run order).

For README content (`DOC-2`), check the required order as well as presence:
citation → authors and contacts → summary → who collected data and wrote code →
file list with variables and units → software and package versions.

### 3. Clean-session run (CODE-6)

If the language runtime is available, run the analysis from the project root in a
fresh process, in the documented order:

- R: `Rscript --vanilla script.R`, or `quarto render file.qmd` for Quarto. Note
  that `--vanilla` ignores `.Rprofile`, so an `renv` project needs
  `Rscript -e 'renv::restore()'` first.
- Python: a fresh virtual environment with the listed requirements, then
  `python script.py`.

Record whether each step finishes, any errors or warnings, run time, and whether the
outputs match the outputs already in the project or the numbers in the manuscript.
If the runtime is not installed, say so plainly; do not claim the code runs.

Ask before starting anything slow. For steps that take hours (MCMC, simulations,
pipelines), do not rerun them at full scale. Instead check the structure in
[references/long-computations.md](references/long-computations.md): full code,
archived full outputs that downstream code reads, and a quick mode. Run the quick
mode if there is one, and rerun everything downstream of the archived outputs. If
there is no quick mode or no archived outputs, report that as a `CODE-12` finding
and offer to set them up.

Capture versions for `DOC-2(f)` from the session that actually ran:
`Rscript -e 'sessionInfo()'` (or `sessioninfo::session_info()`), or
`pip list --format freeze` with `python --version`.

### 4. Report

Write `REPRODUCIBILITY_REPORT.md` in the project root (or show it in chat if the
author prefers) with:

1. A one-paragraph verdict: would a data editor likely accept this archive as is?
2. **Required fixes**: failing or partial REQ items, each with ID, evidence, and the
   concrete change needed.
3. **Recommended improvements**: REC items, briefly.
4. **Questions for the author**: every `TODO(author)` item (metadata you could not
   find).
5. **Clean-run results** from step 3.
6. A table of all checklist IDs with status, for traceability.

Keep it short and specific. The author should be able to work through it in order.

### 5. Fix (only with approval)

Typical fixes, each done only after the author agrees:

- **README**: draft from [templates/README_template.md](templates/README_template.md),
  filled from project files, with `TODO(author)` for anything unknown. Keep the
  required section order.
- **Codebook**: for each CSV, list every column with description, type, units, and
  allowed values or range ([templates/codebook_template.csv](templates/codebook_template.csv)).
  Compute types, ranges, levels, and missing-value counts from the data; get
  meanings and units from the author, the manuscript, or existing documentation.
- **Excel to CSV** (`DATA-5`): export each data worksheet to its own CSV
  (`<workbook>_<sheet>.csv`), keep the workbook, check row and column counts and a
  sample of values against the original, and point the code at the CSV. If you
  change which file the code reads, rerun and confirm results are unchanged.
- **Paths** (`CODE-2`): replace absolute paths and `setwd()` with paths relative to
  the project root (`here::here()` in R, `pathlib.Path(__file__).parent` in Python,
  or plain relative paths with the documented working directory).
- **Script order** (`CODE-1`): move package loading to the top. Remove
  `rm(list = ls())`; it does not make a script reproducible, and running from a
  fresh session does.
- **Seeds** (`CODE-13`): add `set.seed()` / `numpy.random.default_rng(seed)` and
  pass seeds to samplers (e.g. `brms::brm(seed = ...)`, Stan `seed`). Adding a seed
  changes random draws, so tell the author that stochastic results will differ
  slightly from earlier runs and should be regenerated from the seeded code before
  being reported.
- **Figure and table labels** (`CODE-4`, `CODE-10`): add short comments or section
  headers naming the figure or table each block produces. Match the manuscript's
  numbering; ask if it is not available.
- **Column names** (`DATA-8`): prefer renaming in code over editing raw files. If
  the author wants raw headers changed, change headers only and update every script
  and the README to match.
- **Versions**: add the captured `sessionInfo()` or `pip freeze` output to the
  README, or set up `renv` / `requirements.txt` if the author wants that.
- **Long computations** (`CODE-12`): add a `quick`/`full` run-mode switch, save
  full outputs to `outputs/full/`, make figures and tables read them, add a check
  against reported values, and write the README's "Computational cost" section,
  following [references/long-computations.md](references/long-computations.md).
  Never overwrite the archived full outputs with quick-mode results.

After fixing, rerun the audit script and the clean-session run, and update the
report.

If the author is still developing the analysis, offer to add
[templates/AGENTS_snippet.md](templates/AGENTS_snippet.md) to the project's
`AGENTS.md` or `CLAUDE.md`, so coding agents keep to these practices from now on.

### 6. Final archive check

Before the author deposits:

- The archive contains only the README, data, code, and any intermediate outputs
  needed; no `.Rhistory`, `.DS_Store`, caches, personal notes, or drafts (`ARCH-5`).
- It goes to Dryad or Zenodo, not only GitHub (`ARCH-1`); all repository metadata
  fields are filled (`ARCH-2`); and the author gets a private reviewer link for
  submission (`ARCH-3`).
- Remind the author to confirm the current policy in The American Naturalist's
  Instructions for Authors.

## Style for code you write

Match the project's existing language, style, and comment density. Comments say
why, not what. Do not add banners, "changed by agent" notes, or comments that
restate the code.
