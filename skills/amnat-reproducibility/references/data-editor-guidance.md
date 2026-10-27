# Data editor guidance beyond the published checklist

The published checklist ([amnat-checklist.md](amnat-checklist.md)) does not cover
everything a data editor runs into. This file adds guidance for four situations.
Item IDs (`PRIV-1`, `SENS-1`, ...) can be cited in reports like checklist IDs.
Where a point is a decision for the journal (e.g. an exception to data sharing),
say so and send the author to the editor; do not promise an outcome.

## Privacy: what may leave the author's computer (PRIV)

A coding agent sends what it reads to the model provider (Anthropic for Claude
Code, OpenAI for Codex): file contents, command output, and the output of the
bundled scripts. Some authors cannot allow that for unpublished, licensed, or
sensitive data. Running the analysis itself stays on the author's machine.

| ID | Item |
|----|------|
| PRIV-1 | Before reading any data file, manuscript, or output, ask the author what may be read and therefore leave their computer: (a) everything; (b) code, README, and manuscript, but not data contents; or (c) only what the author pastes in. Record the answer at the top of the report. |
| PRIV-2 | Under (b), do not open data files or print their rows. Work from file names, sizes, column names, and the counts and types reported by `audit_archive.py --no-values`; rerun code and compare outputs by computing comparisons locally and reading only the results the author agrees to. Under (c), give the author commands to run and interpret what they choose to share. |
| PRIV-3 | Suggest the author check their institution's rules, any data-use agreement, and the data settings of their agent account before choosing (a). |
| PRIV-4 | Never upload, deposit, push, email, or post anything. Depositing to Dryad or Zenodo, and pushing to GitHub, are the author's actions. |

## Sensitive data (SENS)

Ask early, before reading data contents: "Do any of these data have restrictions
on sharing?" Examples:

- locations of threatened, collectable, or persecuted species (nests, roosts, rare
  plants, cave or den sites);
- human-subject data or personal information (names, contact details, exact
  locations of homes or private land, interview or survey responses);
- Indigenous data, or data collected on Indigenous lands, where community
  agreements or the CARE principles govern use;
- data covered by permits, landowner agreements, data-use agreements, or
  third-party licenses that forbid redistribution;
- commercially or legally sensitive information (e.g. under an MTA or patent).

| ID | Item |
|----|------|
| SENS-1 | Ask the question above, and record the answer. Do not read the contents of files the author identifies as sensitive. |
| SENS-2 | For each restricted data set, discuss options with the author: (i) share a de-identified or coarsened version (e.g. coordinates rounded to 0.1° or to a grid cell, identifiers replaced by codes, free text removed), with the method stated in the README; (ii) deposit in a controlled-access repository and explain how to request access; (iii) for third-party data, give the source, version, and access route instead of redistributing it. |
| SENS-3 | Keep the full code in the archive even when data are restricted, so readers can see and rerun the analysis on data they are allowed to obtain. If results cannot be reproduced from the shared version, say which ones in the README. |
| SENS-4 | The README states which data are withheld or altered, why, and how to obtain them. Advise the author to raise any withholding with the editor at submission; whether it is acceptable is the journal's decision. |
| SENS-5 | Do the de-identification outside the archive, so the original data never enter `data_and_code/`. Do not archive anything that would let it be reversed (e.g. the seed or offsets used to jitter coordinates). Check the shared files for leftover identifiers: other columns, file metadata, photo EXIF location tags. |

## Figures not made entirely by code (FIG)

Not every figure comes straight out of a script. Ask the author how each figure
was made, rather than guessing from its appearance; some figures that look drawn
are simulation output.

| Kind of figure | What to expect | Traceability status |
|----------------|----------------|---------------------|
| Made by code, unchanged | Code reproduces it | match / mismatch |
| Made by code, then edited (Illustrator, Inkscape, PowerPoint, Affinity, ...) | Code produces the data-bearing base figure, archived (e.g. `outputs/fig2_base.pdf`). Compare data content (points, values, axes, scales, groups, panels), not styling. | edited after code, plus match / mismatch on data content |
| Conceptual diagram, schematic, study design or map drawn by hand | No code expected | not computational |
| Photo or video used as illustration | No code or archive expected | not computational |
| Photo, video, or recording used as data (measured, scored, counted) | Raw media or representative examples archived (`DATA-6`), with how they were scored | not computational, with `DATA-6` check |
| Mixed (code panels and drawn or photo panels) | Check each panel separately | per panel |

| ID | Item |
|----|------|
| FIG-1 | For every figure not marked "match" on first comparison, ask the author how it was made before assigning a status. |
| FIG-2 | Editing after code must not change data content: moved, removed, or added points, rescaled axes, altered error bars, or redrawn curves are a mismatch, even if done for clarity. Cosmetic edits (fonts, colours, layout, labels, arrows, insets of photos) are fine. |
| FIG-3 | The README has a section "Figures not produced entirely by code" listing each such figure (or panel), what was done by hand and with which software, and for edited figures the archived base file. |
| FIG-4 | "Not computational" items are listed in the traceability table but left out of the coverage count, which reports them separately (e.g. "38 of 38 computational items reproduced; 3 not computational"). |

## Point-and-click analyses (GUI)

Analyses done only by pointing and clicking cannot be rerun by a reader, so
**the data editor does not accept them**. Every reported result must come from a
script, command file, or saved configuration that reproduces it. Help the author
move to a reproducible version:

| Done in | Reproducible version |
|---------|----------------------|
| Excel formulas, pivot tables, Excel charts | R or Python script reading the CSV export |
| JMP, SPSS, Prism, Statistica, Minitab, PAST (menus) | R or Python equivalent; where the software saves a script (SPSS syntax, JMP JSL, Stata do-file, SAS program), that script is acceptable code, though an open tool is preferable |
| BEAST / BEAUti | Archive the XML, run it from the command line (`beast -seed 42 analysis.xml`), and script the LogCombiner and TreeAnnotator steps |
| MrBayes, RAxML, IQ-TREE, PAUP* | NEXUS files with command blocks, or a shell script of the exact commands |
| STRUCTURE GUI | Command-line STRUCTURE with `mainparams`/`extraparams`, or an R wrapper, with seeds |
| Geneious, MEGA, CLC (menus) | Command-line tools for the same steps (e.g. MAFFT, trimAl, IQ-TREE) in a script, with versions |
| ImageJ / Fiji by hand | Macros (`.ijm`) or scripts; manual measurements are raw data, archived as CSV |
| QGIS, ArcGIS by hand | R (`sf`, `terra`) or Python (`geopandas`, `rasterio`), or PyQGIS / exported model scripts |

| ID | Item |
|----|------|
| GUI-1 | Identify any reported result produced only through a graphical interface (ask the author; look for project files such as `.jmp`, `.spv`, `.pzfx`, `.mtw`, or analyses described in the Methods with no matching code). |
| GUI-2 | Offer to write the scripted version. Rerun it and compare with the reported values. If they differ, this is a revised analysis, not a refactor: report the differences to the author, who must decide how to update the manuscript. |
| GUI-3 | Manual data entry, scoring, or measurement is fine as raw data; every step after the raw data must be scripted. |
