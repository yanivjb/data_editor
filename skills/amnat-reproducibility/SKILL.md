---
name: amnat-reproducibility
description: Optional helper for authors preparing data, code, and README for submission to The American Naturalist (or a journal with a similar policy). Checks the project against the journal's data and code archiving checklist and reproducibility best practice (README contents and order, relative paths, CSV data, codebook, seeds, package versions, clean-session reruns, long Bayesian/simulation/bioinformatics runs, Dryad/Zenodo deposit) and helps fix what the author chooses, including tracked-change manuscript corrections on request. Use when an author asks to check reproducibility, check that code reproduces the manuscript, get ready for submission, prepare a Dryad or Zenodo archive, write a data README or codebook, handle slow analyses, or respond to a data editor report.
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
you report. Also read
[references/data-editor-guidance.md](references/data-editor-guidance.md) (privacy,
sensitive data, figures not made by code, point-and-click analyses; IDs `PRIV`,
`SENS`, `FIG`, `GUI`) and, for slow analyses (MCMC, simulations including SLiM,
bioinformatics pipelines), [references/long-computations.md](references/long-computations.md).

## Choosing how deep to go

Unless the author has already said, ask which they want:

1. **Quick scan**: run the audit script, summarise the main gaps in chat. Minutes.
2. **Full review**: steps 1–6 below, ending in a written report. No files changed.
3. **Guided fixes**: full review, then fix the items the author picks (step 7).

In every mode, ask the privacy and sensitive-data questions in "Before you start"
first, before the audit script or anything else reads the author's files. Respect
the choice of mode. Do not start editing during a scan or review.

**The person in the chat may not be the author.** A co-author, student, or data
editor may run the review and hand the results to authors who never saw the
conversation. Write every author-facing file (`REPRODUCIBILITY_REPORT.md`,
`AUTHOR_TODO.md`, `WHAT_CHANGED.md`) so it stands alone: plain language, no
checklist IDs, no references to the chat ("as discussed"), and enough context
that someone opening it cold knows what to do.

**Coming back after changes.** If the project already has a
`reproducibility_review/` folder, this is a re-review. Read the previous
`full_report.md` and `AUTHOR_TODO.md` first, find what the authors changed, rerun
everything, and update the existing reports rather than starting new ones: say
which earlier findings are now fixed, which remain, and anything new.

## Ground rules

These protect the scientific record. Do not break them, even when asked casually.

1. **Never change data values.** Do not edit, reorder, recode, or "clean" raw data
   files. Converting an `.xlsx` sheet to `.csv` must reproduce cell values exactly.
   Data cleaning belongs in code (`CODE-8`). When the author identifies a genuine
   data error (e.g. two plants sharing an ID), make the correction in a clearly
   labelled step in the code, not in the raw file, so readers can see it. Say what
   the correction changes: records gained or dropped from each analysis, sample
   sizes, results. Describe it for readers in a "Data corrections" section of the
   README. Edit a raw file only if the author insists after hearing this; then keep
   the original outside the archive and document the change the same way.
2. **Never change results.** Code edits for reproducibility (paths, seeds, package
   loading, comments, file layout) must not change any reported number, table, or
   figure. Before editing code that produces results, record the current outputs;
   afterwards, rerun and compare. Report any difference to the author rather than
   accepting it.
3. **Never invent metadata.** Citations, author contacts, who collected the data,
   units, missing-value codes, permits, funding, and variable meanings come from
   the author or from the project's own files. If you cannot find a value, add it
   to `AUTHOR_TODO.md` (see rule 8). A plausible guess presented as fact is worse
   than a visible gap.
4. **Ask before acting.** Auditing is read-only. Present the report first, then fix
   only what the author approves. Do not delete files; propose moving unused
   material to an `extra/` folder or a script coda (`CODE-11`, `ARCH-5`) instead.
5. **Required vs recommended.** Make clear which findings block compliance (REQ)
   and which are good practice (REC). Do not inflate recommendations into demands,
   and do not comment on code elegance; the journal only cares that it works.
6. **Verify, never assume.** Every "pass", "match", or "runs" must rest on something
   you actually ran or read in this session, logged with the command, exit status,
   and output file. If you did not run it, the status is "not rerun"; if you only
   read the code, say "checked by reading". Never fill in a status from what the
   code looks like it should produce.
7. **Only what the author allows leaves their computer.** Everything you read is
   sent to your model provider, so ask first (see "Before you start"). Never
   upload, deposit, email, or post anything; those are the author's actions
   (`PRIV-4`). Do not commit to version control or push to a remote unless the
   person you are working with asks; if you do, say exactly what was committed and
   where it was pushed.
8. **The archive is for readers; notes are for the author.** Files in the archive
   (README, codebook, code comments) contain only finished, reader-facing content:
   what the files are, what the variables mean, how to run the code. Never put
   these in the archive:
   - `TODO`s, placeholders, or questions for the author;
   - checklist IDs (`DOC-2`, `DATA-12`, ...) or mentions of this review, the
     checklist, or the journal's data editor;
   - the history of how a fact was established ("the author confirmed", "no data
     were converted", "import behaviour has not been changed", "not a verified
     rerun");
   - audit detail such as line numbers of odd values, or links to files outside
     the archive (`../reproducibility_review/runlog.md`).

   Write confirmed facts plainly ("Leaf area is in cm²", "Blank cells are missing
   values"). Everything still to do goes in `AUTHOR_TODO.md` in the project folder,
   outside the archive, based on
   [templates/AUTHOR_TODO_template.md](templates/AUTHOR_TODO_template.md): one
   checkbox per item, saying what is needed, where it goes, and why. Leave a
   README section out until its content is known, rather than filling it with a
   placeholder; list it in `AUTHOR_TODO.md` instead. Use exactly the file names in
   "Where review files go"; do not invent others, and link to them with paths
   relative to the project folder.
9. **Ask once, then respect the answer.** Explain the consequence of a choice and
   ask. If the author says to proceed or move on, do so: record any open question
   in `AUTHOR_TODO.md` and the consequence in the full report, and do not ask again.

## Workflow

### Before you start: privacy and sensitive data

Before opening any data file, manuscript, or output, ask the author two questions
and record the answers at the top of the report:

1. **What may leave this computer?** Explain that what you read is sent to the model
   provider, then offer: (a) everything; (b) code, README, and manuscript, but not
   data contents; (c) only what the author pastes in (`PRIV-1`). Under (b), run the
   audit script with `--no-values` and do not print data rows (`PRIV-2`).
2. **Are any data sensitive or restricted?** For example threatened-species
   locations, human-subject or personal data, Indigenous data, or data under permit
   or license limits (`SENS-1`). If yes, do not read those files' contents, and
   guide the author through the options in
   [references/data-editor-guidance.md](references/data-editor-guidance.md)
   (`SENS-2` to `SENS-5`).

Running code locally is fine under every option; what matters is what you read.

### Where review files go

Keep the author's view small. Only two files go at the top of the project folder;
everything else goes in one review folder:

```text
project_name/
├── REPRODUCIBILITY_REPORT.md      one-page summary for the author (step 6)
├── AUTHOR_TODO.md                 what only the author can supply or decide
├── revised_manuscript/            only if the author asks for manuscript edits (step 7)
├── WHAT_CHANGED.md                written when finishing (step 9)
└── reproducibility_review/
    ├── full_report.md             every checklist item and the full results table
    ├── runlog.md                  every command run, with exit status and outputs
    ├── audit.md                   output of audit_archive.py
    ├── manuscript_items.md        output of manuscript_items.py
    └── work/                      scratch: helper scripts, logs, rerun copies,
                                   local package library; safe to delete
```

Nothing from the review goes in `data_and_code/` or `ms_files/`. In `work/`:

- **Save small, targeted evidence** (a CSV of the compared values, a log), not
  whole R workspaces or environment dumps; save a large object only when a later
  step needs it, and say so in `runlog.md`.
- **Reuse one rerun copy** of the archive rather than making a new copy for each
  attempt, and name what you keep after the step it belongs to.
- **Do not mention `work/` in the reports** except to point to evidence a finding
  depends on.

At the end, tell the author how much space `work/` uses and offer to delete it.

### 1. Find the archive and the manuscript

The recommended layout keeps what will be deposited apart from the paper:

```text
project_name/
├── ms_files/                  manuscript in any format (.docx, .tex, .qmd, .md, .pdf),
│                              plus figures, tables, supplements: any structure
├── data_and_code/             the archive to deposit: README.md, data, code,
│                              outputs, intermediate files, in any sensible structure
├── .claude/skills/amnat-reproducibility/   this skill (Claude Code)
└── .agents/skills/amnat-reproducibility/   this skill (Codex)
```

If the project has `ms_files/` and `data_and_code/`, use them. Otherwise ask the
author where the archive root (the folder that will be deposited) and the manuscript
are.

**If the files are not in this layout** (everything in one folder, the manuscript
somewhere else, data and code scattered), offer to help organise them. Show the
author the layout you propose, file by file, and wait for agreement. Then:

- copy rather than move when the originals live elsewhere (e.g. a manuscript in a
  Dropbox folder), and say which you did;
- after moving code or data, update the paths in the code, rerun it, and confirm
  the outputs are unchanged (ground rule 2);
- leave out of `data_and_code/` anything that is not part of the archive (drafts,
  notes, old versions), but delete nothing.

The author may prefer to keep their own layout; then work with it, and record
where the archive and the manuscript are in the full report.

**If something is missing, ask for it** before going further, and say why it
matters. Check for:

- the manuscript and supplement: optional, but without them you cannot check that
  the code reproduces the paper (step 5), so ask for the current versions;
- data files that the code reads but that are not in the project;
- code for analyses described in the Methods (including any run in other software);
- the README, if there is one; if not, offer to draft it later (step 7);
- outputs of slow steps, if the code expects to read them.

If the author cannot supply something yet, record it in `AUTHOR_TODO.md` and carry
on with what you have.

The manuscript is used only for checking. It is not part of the archive.

### 2. Inventory

Run the bundled audit script for a quick mechanical scan of the archive:

```sh
python3 <skill-dir>/scripts/audit_archive.py <project_name> --out reproducibility_review/audit.md
```

`<skill-dir>` is the directory containing this `SKILL.md`. Given the project folder,
the script scans `data_and_code/` if it exists and never scans `ms_files/`; you can
also pass the archive folder directly. It uses only the Python standard library. It
finds file types, README sections, absolute paths, `setwd()`, missing seeds, data
reads of files not in the archive, CSV column-name problems, mixed column types,
missing-value codes, and columns not mentioned in the README. Treat its output as
leads to check, not verdicts: it uses pattern matching and will produce false
positives and miss things.

Then read the archive yourself: the README, every script in run order, and the
headers of every data file. Work out:

- the entry point(s) and run order;
- which data files feed which scripts, and which outputs each script writes.

### 3. Audit

Go through every item in the checklist. For each, record **pass**, **fail**,
**partial**, **not applicable**, or **can't tell** (e.g. no manuscript to compare
against), with evidence as `path:line` or a file name. Pay particular attention to
the things the journal's data editors report most often:

- no README, or a README that does not explain variable names and units;
- data left only in Excel or proprietary formats;
- data files that the code reads but that are missing from the archive;
- scripts that do not run in a fresh session (absolute paths, objects assumed to
  exist in the workspace, packages loaded halfway through, undocumented run order);
- results produced by point-and-click software with no script, which the data
  editor does not accept (`GUI-1`): ask the author how each analysis in the Methods
  was run if no code for it is found.

For README content (`DOC-2`), check the required order as well as presence:
citation → authors and contacts → summary → who collected data and wrote code →
file list with variables and units → software and package versions.

### 4. Clean-session run (CODE-6)

If the language runtime is available, run the analysis from the archive root in a
fresh process, in the documented order:

| Language | Fresh run | Versions to record |
|----------|-----------|--------------------|
| R | `Rscript --vanilla script.R`; `quarto render file.qmd`. `--vanilla` ignores `.Rprofile`, so run `Rscript -e 'renv::restore()'` first in an `renv` project | `sessionInfo()` |
| Python | new virtual environment with the listed requirements, then `python script.py`; notebooks with `jupyter nbconvert --to notebook --execute` | `python --version`, `pip list --format freeze` |
| Julia | `julia --project=. -e 'using Pkg; Pkg.instantiate()'`, then `julia --project=. script.jl` | `Project.toml` and `Manifest.toml`, `versioninfo()` |
| MATLAB | `matlab -batch "run('script.m')"` | `ver` (MATLAB and toolbox versions) |
| Mathematica | `wolframscript -file script.wls`; notebooks need evaluating in the front end, so ask the author to export a `.wl`/`.wls` script or run it themselves | `$Version` |
| C / C++ / Fortran | build from scratch with the documented command (`make`, `cmake`), then run | compiler and version, flags, library versions |
| SLiM | `slim -s SEED -d param=value model.slim` | `slim -v` |
| Stan / JAGS models | run through the calling R/Python/Julia script | CmdStan or JAGS version |
| Workflows | `snakemake -n` (dry run) then the documented target; `nextflow run ... -profile test` | workflow manager version, tool versions |

MATLAB and Mathematica need licences, and many runtimes may not be installed. If
you cannot run a language, say so, check the code by reading, and mark its items
**not rerun**; offer the author the exact commands to run themselves and share the
output.

Log every command you run in `reproducibility_review/runlog.md`: the command, working directory, start time, run time, exit
status, warnings or errors, and the output files written. This log is the evidence
for every "runs" and "match" in the report. If the runtime is not installed, say
so plainly; do not claim the code runs.

Render Quarto and R Markdown documents with caches cleared (delete `*_cache/` and
`_freeze/` folders, or render a fresh copy of the archive), so the clean run does
not reuse old results.

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

### 5. Reproduce every manuscript result

This is the core of the review. Its question: does every result in the paper come
out of the archive? Consult everything in `ms_files/`: the main text, the
supplement, and the figure and table files.

**List every item.** Extract the manuscript's captions, figure and table mentions,
and sentences with numbers:

```sh
python3 <skill-dir>/scripts/manuscript_items.py <project_name>/ms_files --out <project_name>/reproducibility_review/manuscript_items.md
```

The script reads `.docx`, `.tex`, `.md`, `.qmd`, `.Rmd`, and `.txt` with the
standard library, and `.pdf` if `pdftotext` is installed; otherwise ask the author
for a text or Word export. Treat its list as a starting point: read the Results,
the figure and table legends, and the supplement yourself, and add anything it
missed (numbers in tables, values inside figure panels, results reported only in
the Methods or Discussion). Also list the image and table files in `ms_files/`
(e.g. `fig1.png`, `table_s2.docx`) and match them to their manuscript numbers.

The list should cover, at minimum:

- every main and supplementary **figure**, panel by panel where panels show
  different analyses;
- every main and supplementary **table**, including every reported cell value;
- every **number in the text** that comes from the analysis: estimates, intervals,
  test statistics, p-values or posterior probabilities, sample sizes, percentages,
  and model diagnostics.

**Trace and reproduce each item.** For each, find the code that produces it, rerun
that code (step 4), and compare. Record one row per item:

| Manuscript item | Value in paper | Produced by | Output file | Value from rerun | Status |
|-----------------|----------------|-------------|-------------|------------------|--------|
| Table 2, row "Self" | 41.2% (95% CI 35.0–47.5) | `code/03_summaries.R:88` | `outputs/table2.csv` | 41.2% (35.0–47.5) | match |
| Figure 3B | (plot) | `code/04_figures.R:120` | `outputs/fig3.pdf` | same data, axes, and groups | match |
| Results ¶2, "n = 214 seed batches" | 214 | not found | — | — | not found in code |
| Figure 1 | (diagram) | — | — | — | not computational |

Status is one of:

- **match**: the rerun gives the reported value at the precision the paper reports.
  For MCMC and other stochastic results, a difference within Monte Carlo error is a
  match (see [references/long-computations.md](references/long-computations.md)).
- **mismatch**: the rerun gives a different value. Give both values.
- **not rerun**: the code exists but could not be run here (slow step with no quick
  mode, missing runtime). Say why.
- **not found in code**: no code in the archive produces the item (a `DATA-1`
  failure unless the value is not computed, e.g. a sample size taken from the
  study design; say so if that is the case). For each such item, check whether
  the data needed to make it are in the archive (e.g. by looking for the columns
  or files a figure plots), so the authors know whether they need to add only
  code or also source data. This is read-only; do it as part of the review.
- **edited after code**: a figure made by code and then changed in another tool.
  Also give match or mismatch for its data content (`FIG-2`).
- **not computational**: a conceptual diagram, drawn schematic or map, or photo or
  video, confirmed as such by the author (`FIG-1`).

For **figures**, open the regenerated figure and the manuscript figure (from
`ms_files/` or the manuscript itself) and compare them visually: same data, panels,
axes, groups, and overall pattern. Say which figures you could not view. When a
figure does not match exactly, or looks drawn, photographed, or polished in a
graphics editor, ask the author how it was made before assigning a status; do not
guess (`FIG-1`). Agree with them on a README entry for each figure or panel that is
not produced entirely by code (`FIG-3`).

**Summarise coverage** at the top of the table, counting only computational items,
e.g. "38 of 41 computational items reproduced; 2 not found in code; 1 mismatch;
3 not computational" (`FIG-4`). Use the table to assess `DATA-1` (every result has
its data and code), `CODE-4` and `CODE-10` (code labels match figure and table
numbers), and `CODE-5` (packages used are cited in the paper). Report mismatches to
the author; do not change the code or the manuscript to make them agree.

**Find out why each mismatch happened** before anyone corrects anything. Do not
assume the code is right and the paper wrong. Likely causes:

- a typo or rounding difference in the manuscript;
- the manuscript reports an earlier run (an older model, older data, or a
  different software version): look at old rendered outputs, version history, or
  dates;
- the code changed since the paper was written, possibly introducing an error,
  e.g. a join that now duplicates or drops records;
- a different subset or definition (all plants vs. those with seed data, raw vs.
  model-adjusted means).

Record the likely cause and your evidence for it. For a large discrepancy
(e.g. a test statistic of 21 in the paper and 16 from the code), say plainly that the cause is
unknown if you cannot establish it. Flag any mismatch that changes a conclusion,
e.g. a result that was significant and no longer is.

If there is no manuscript, mark these items **can't tell** and say in the report's
verdict that results were not checked against the paper. Offer to do this step
when the author can add the manuscript to `ms_files/`.

### 6. Report

Write two reports: a short one the author reads, and a full one that holds the
evidence.

**`REPRODUCIBILITY_REPORT.md`** (top of the project folder) fits on one page,
in plain language, with no checklist IDs or jargon (write "Summary", not
"Verdict"). Use these headings:

0. **How to use this report**, three or four lines: read the summary and the
   results check; work through `AUTHOR_TODO.md`, most important first; put new or
   corrected files in the archive folder and keep raw data unedited; then run the
   review again (e.g. "Check this project against the AmNat checklist") to
   confirm. Mention that the files in `reproducibility_review/` are only needed
   for details.
1. **Summary**, two or three sentences: does the code run, does it reproduce the
   paper, and is the archive ready to deposit?
2. **Results check**, one line: e.g. "38 of 41 results reproduced; 2 have no code;
   1 differs (Results ¶2: 45.3% in the paper, 43.3% from the code)." List every
   mismatch and every result with no code; these matter most.
   If any mismatch changes a conclusion (significance, direction, or a claim in
   the abstract), add a line **"Conclusions affected"** naming them; these come
   first.
3. **What to fix**, at most about ten one-line items, most important first, required
   before recommended. Group similar findings ("12 column names contain spaces").
4. **What we need from you**: "See `AUTHOR_TODO.md` (5 items)."
5. One line on what was and was not checked (what you were allowed to read, which
   steps were not rerun and why), and a pointer to
   `reproducibility_review/full_report.md` for the details.

**`reproducibility_review/full_report.md`** holds everything else: the privacy and
sensitive-data answers (`PRIV-1`, `SENS-1`); every finding with its checklist ID,
evidence (`path:line`), and the change needed; recommended improvements; the
clean-run results, pointing to `runlog.md`; the full manuscript traceability table
with its coverage summary; and a table of all checklist IDs with status.

Show the author the short report, in chat or by opening the file. Do not paste the
full report into the chat.

End the review by separating what is left: what only the authors can supply or
decide (in `AUTHOR_TODO.md`), and small, safe things you could still do, each with
its cost and whether it changes any file (e.g. "rebuild the ZIP files without
`__MACOSX` folders; contents verified by checksum"). Do them only if asked.

### 7. Fix (only with approval)

Typical fixes, each done only after the author agrees:

- **README**: draft from [templates/README_template.md](templates/README_template.md)
  using only confirmed information, in the required section order and following
  rule 8. Put every gap in `AUTHOR_TODO.md`. Before finishing, reread the README
  as a stranger downloading the archive would: every sentence should help them
  understand or run it.
- **Codebook**: for each CSV, list every column with description, type, units, and
  allowed values or range ([templates/codebook_template.csv](templates/codebook_template.csv)).
  Compute types, ranges, levels, and missing-value counts from the data; get
  meanings and units from the author, the manuscript, or existing documentation.
- **Excel to CSV** (`DATA-5`): export each data worksheet to its own CSV
  (`<workbook>_<sheet>.csv`), keep the workbook, check row and column counts and a
  sample of values against the original, and point the code at the CSV. If you
  change which file the code reads, rerun and confirm results are unchanged.
- **Paths** (`CODE-2`): replace absolute paths and `setwd()` with paths relative to
  the archive root (`here::here()` in R, `pathlib.Path(__file__).parent` in Python,
  or plain relative paths with the documented working directory). With the
  recommended layout, `here::here()` would find `project_name/` if that is where
  `.git` or the `.Rproj` file is, so put an empty `.here` file (or the `.Rproj`) in
  `data_and_code/` so paths resolve inside the archive.
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
- **Figures not produced entirely by code** (`FIG-3`): write the README section
  from what the author told you, and archive the code-made base file of each
  edited figure.
- **Point-and-click analyses** (`GUI-2`): write the scripted version following
  [references/data-editor-guidance.md](references/data-editor-guidance.md), rerun
  it, and compare with the reported values. Any difference makes this a revised
  analysis; report it to the author rather than adjusting the script to match.
- **Restricted data** (`SENS-2` to `SENS-5`): help write the de-identification
  script (run outside the archive) and the README statement on withheld data.
- **Data corrections** (rule 1): a labelled correction step in the code, its
  consequences for sample sizes and results, and a "Data corrections" section in
  the README written for readers.

#### Manuscript corrections (only if the author asks)

Correcting the paper goes beyond checking the archive, so do it only on request,
and only for items the author has decided on:

- **Never edit the originals.** Work on copies in `revised_manuscript/` at the top
  of the project folder.
- **Make every change visible.** For Word files, always use the bundled script,
  which writes genuine Word tracked changes and comments:

  ```sh
  python3 <skill-dir>/scripts/docx_track_changes.py ms_files/manuscript.docx \
      reproducibility_review/work/edits.json \
      --out revised_manuscript/manuscript_tracked.docx --author "<name the author chooses>"
  ```

  `edits.json` lists each edit as `{"find": ..., "replace": ...}` (or
  `"insert_after"`), with an optional `"context"` to make the location unique and a
  `"comment"`; the script's header documents the format. It changes only the words
  that differ, refuses any edit whose text is missing or ambiguous, and writes
  nothing unless every edit applies. Run it with `--dry-run` first. Apply all
  edits for one file in one run, so the tracked copy builds on the original. For
  LaTeX or Markdown, produce a marked-up diff (e.g. `latexdiff`) alongside the
  revised copy.
- **Explain every changed number in a comment** (a Word comment, or a note in the
  change table): the new value, the output file and line it comes from, and the
  old value. Keep `edits.json` in `reproducibility_review/work/` as the record of
  what was changed.
- **Use only verified values** from a rerun logged in `runlog.md`, at the
  precision the manuscript uses.
- **Keep interpretation with the author.** When a correction changes significance,
  direction, or a conclusion, propose the wording in a comment and say what
  changed. If the author asks you to rewrite the text, keep claims to what the
  verified output supports, and flag the change in the short report.
- **Keep the numbers and Methods consistent.** If the final results now come from
  a different software environment or a corrected data set than the original
  analysis, make sure the revised Methods says so, and record it as a revised
  analysis in the full report.
- Give the author one list of all changes made, in the full report, so co-authors
  can follow them.

After fixing, rerun the audit script and the clean-session run, and update the
report.

If the author is still developing the analysis, offer to add
[templates/AGENTS_snippet.md](templates/AGENTS_snippet.md) to the project's
`AGENTS.md` or `CLAUDE.md`, so coding agents keep to these practices from now on.

### 8. Final archive check

Before the author deposits:

- The archive folder (e.g. `data_and_code/`) contains only the README, data, code,
  and any intermediate outputs needed; no `.Rhistory`, `.DS_Store`, caches,
  personal notes, drafts, or manuscript files (`ARCH-5`).
- Every item in `AUTHOR_TODO.md` is done, and the README reads as finished text
  for readers: no placeholders, checklist IDs, or review notes (rule 8). Rerun the
  audit script to check.
- It goes to Dryad or Zenodo, not only GitHub (`ARCH-1`); all repository metadata
  fields are filled (`ARCH-2`); and the author gets a private reviewer link for
  submission (`ARCH-3`).
- Remind the author to confirm the current policy in The American Naturalist's
  Instructions for Authors.

### 9. Finish

When the author says they are done, or asks you to wrap up or clean up:

1. **Make everything consistent with the final analysis.** If any data, code, or
   software environment changed during the review, rerun the whole analysis from
   scratch, regenerate every output (figures, tables, rendered reports, session
   information), and recheck each manuscript item that the change could affect.
   Do this yourself rather than leaving it to the author. Compare each regenerated
   figure with the one in the manuscript; if it changed, put the new file in
   `revised_manuscript/` (figures cannot carry tracked changes) and list it in
   `WHAT_CHANGED.md`. If something cannot be regenerated, say so plainly.
2. **Before overwriting or deleting anything outside `reproducibility_review/`**,
   say exactly which files will be replaced or removed and how they can be
   recovered (version control, a backup copy, or rejecting all tracked changes in
   Word). Overwrite originals with tracked copies only when the author asks, and
   never accept tracked changes for them.
3. **Write `WHAT_CHANGED.md`** at the top of the project folder from
   [templates/WHAT_CHANGED_template.md](templates/WHAT_CHANGED_template.md): a
   high-level summary the author can send to co-authors of every change to data,
   code, results, the README, and the manuscript, with before and after values
   for results that changed.
4. **Update `AUTHOR_TODO.md`** so it lists only what is still open, most important
   first, and update the verdict in `REPRODUCIBILITY_REPORT.md`.
5. **Clean up** after asking. By default, delete `reproducibility_review/work/`
   (say how much space it frees) and keep `full_report.md` and `runlog.md`, which
   are small and show what was verified; delete them too only if the author asks.
   Delete nothing in the archive or manuscript folders except files the author
   names. Record checksums of every file you keep in the archive and manuscript
   folders before cleaning up, check them afterwards, and list what you deleted.

When you finish, the project folder should contain the author's own folders,
`AUTHOR_TODO.md`, `WHAT_CHANGED.md`, `REPRODUCIBILITY_REPORT.md`, any
`revised_manuscript/` folder the author kept, and the slimmed
`reproducibility_review/`.

## Style for code you write

Match the project's existing language, style, and comment density. Comments say
why, not what. Do not add banners, "changed by agent" notes, or comments that
restate the code.
