# American Naturalist checklist for archiving data and code

Source: Bolnick, Schürch, Vedder, Reuter, Perez & Montgomerie (1 December 2021),
"A checklist for reproducible archiving data and code in ecology, evolution, and
behavior", *From the Editor's Desk of The American Naturalist*
(<http://comments.amnat.org/2021/12/guidelines-for-archiving-code-with-data.html>).
Policy page: <https://www.amnat.org/announcements/DataChecklist.html>.

The items below follow the published checklist. IDs are added here so audit reports
can cite them. **REQ** = required by the journal; **REC** = recommended. Journal
policy can change: before telling an author their archive is compliant, remind them
to confirm against the current Instructions for Authors.

The guiding question:

> If a reader downloads my data and code, will my scripts be comprehensible, and
> will they run to completion and yield the same results on their computer?

Editors and data editors judge whether code works and reproduces the reported
results, not whether it is elegant.

## 1. Documentation (README)

| ID | Level | Item |
|----|-------|------|
| DOC-1 | REQ | One README for the whole repository (code and data), named `README.txt`, `README.rtf`, or `README.md`. |
| DOC-2 | REQ | README contains, **in this order**: (a) citation to the associated publication; (b) author names and contact details; (c) brief study summary; (d) who collected the data and who wrote the code; (e) list of all folders and files with a brief description of each, and for each data file every variable (column) with a clear description including units; (f) versions of software and packages used, operating system, and dependencies not installed by the scripts (e.g. `sessionInfo()` in R, `pip list --format freeze` in Python). |
| DOC-3 | REC | Workflow instructions for running the code (run order, configuration parameters). |
| DOC-4 | REC | Informative folder and file names (e.g. `code/`, `data/`, `outputs/`). |
| DOC-5 | REC | License information (e.g. a Creative Commons or open source license; see choosealicense.com). Not needed on Dryad, which sets the license at submission. |
| DOC-6 | REC | Funding sources and permits (collection, animal care, human research), if applicable. Not needed on Dryad, which records them at submission. |
| DOC-7 | REC | Links to protocols.io or equivalent methods repositories, if applicable. |

Template suggested by the journal: <https://github.com/gchure/reproducible_research>.

## 2. Code

| ID | Level | Item |
|----|-------|------|
| CODE-1 | REQ | Scripts start by loading required packages, then import raw data from files archived in the repository. |
| CODE-2 | REQ | Relative paths only (no `setwd()` with an absolute path), so others can run the input steps on their machines. |
| CODE-3 | REQ | Comments explain the purpose ("why") of each set of commands. Unclear "how" should be rewritten more simply; in-line comments may give specifics. |
| CODE-4 | REQ | Comments indicate which figure, table, or Results subheading each block of code produces. |
| CODE-5 | REQ | Adapted code from other researchers is acknowledged and cited; packages used are cited in the article. |
| CODE-6 | REC | Code tested before upload, ideally on a pristine machine with no packages installed, at minimum in a fresh session. |
| CODE-7 | REC | Informative names for input files, variables, and functions, described in the README. |
| CODE-8 | REC | All data manipulation (merging, sorting, transforming, filtering) done in scripts, not by hand. |
| CODE-9 | REC | Code organised into logical sections (import/cleaning, transformation, analysis, figures/tables), as separate scripts run in a documented order or as clearly separated blocks or function calls. |
| CODE-10 | REC | Section headers match figure numbers, table numbers, or text subheadings of the paper. |
| CODE-11 | REC | Extraneous code not used for the published results removed, or moved to a coda at the end of the script. |
| CODE-12 | REC | Intermediate outputs saved and deposited where useful, especially outputs of computationally intensive steps, as an alternative entry point. |
| CODE-13 | REC | Random seed set for any stochastic process, at least once at the start of the script and preferably for each random sampling task. |
| CODE-14 | REC | Clear error messages or annotations explaining what might go wrong (e.g. wrong input type) and the effect of the error or warning. |

## 3. Data

### Repository contents

| ID | Level | Item |
|----|-------|------|
| DATA-1 | REQ | All data used to generate any published result are included (possibly several files for several experiments). |
| DATA-2 | REQ | Each file has a short, meaningful name and extension. |
| DATA-3 | REQ | README (preferably the single README of DOC-1) describes each data file's contents and lists every variable name with an explanation (e.g. units), so a new reader can relate columns to the Methods and Results. A tabular "codebook" (one row per variable: name, description, units, ...) is an acceptable alternative. Separate code and data READMEs under a master README are allowed for very complex repositories, but one README is preferred. |
| DATA-4 | REQ | README as `.txt` or `.md`; every data file as `.csv`. |
| DATA-5 | REQ | Excel workbooks may also be included (for colour coding, formulae), but every worksheet of data must also be saved as its own `.csv`. |
| DATA-6 | REC | Raw digital material used to generate data (photos, sound, video) archived, or at least a few example files showing the range of outcomes. |

### File contents and formatting

| ID | Level | Item |
|----|-------|------|
| DATA-7 | REQ | Raw data as used at the start of analysis, not group means or other summaries. Summaries may be given in a separate file or generated by archived code. |
| DATA-8 | REQ | Short variable (column) names, preferably under 10 characters, with no spaces or special characters; use `snake_case` or `CamelCase` to separate words. |
| DATA-9 | REC | Variables not analysed in the code omitted. |
| DATA-10 | REC | Tidy structure: each observation a row, each variable a column. |
| DATA-11 | REC | One data type per column (no numbers mixed with comments or categorical scores). |
| DATA-12 | REC | `NA` (or an equivalent) for missing data, with the code stated in the README. |

## 4. Archive

| ID | Level | Item |
|----|-------|------|
| ARCH-1 | REQ | Data and code deposited in a curated, version-controlled public repository (e.g. Dryad, Zenodo). A personal or agency-controlled GitHub or website does **not** qualify; GitHub archived to Zenodo does. |
| ARCH-2 | REQ | All metadata requested by the repository provided, even optional or redundant fields. |
| ARCH-3 | REQ | A private reviewer URL from the repository supplied at manuscript submission. |
| ARCH-4 | REC | Data, code, and README prepared before or during manuscript writing. |
| ARCH-5 | REC | When archiving GitHub to Zenodo, remove all extraneous files so only the core data, code, and README remain. |

The journal prefers Dryad or Zenodo: both are curated, files cannot be silently
changed after publication, and Dryad routes code and other non-data files to Zenodo
automatically when everything is uploaded to Dryad.

## Further reading listed by the journal

- British Ecological Society, *A guide to reproducible code in ecology and evolution* (2019).
- Real Python, *Documenting Python code: a complete guide*.
- Dockta (stencila) for building reproducible environments.
- Poetry for Python version management.
- *Principles of Software Development – an Introduction for Computational Scientists*, <https://doi.org/10.5281/zenodo.5721380>, and its code inspection checklist, <https://doi.org/10.5281/zenodo.5284377>.
- Tidyverse and Google R style guides; Google Python style guide.
