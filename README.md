# AmNat reproducibility skill

An optional helper for authors that works with Claude Code or Codex. Before you
submit to *The American Naturalist*, it checks your data, code, and README against
the journal's
[checklist for archiving data and code](http://comments.amnat.org/2021/12/guidelines-for-archiving-code-with-data.html)
and against reproducibility best practice, and helps you fix what you choose.

It is a pre-submission aid, not part of the journal's review: the journal's data
editors still decide what is acceptable. Use it early, while the analysis is still
being written, when fixes are cheap.

## What it does

- **Scans** the project (`scripts/audit_archive.py`, Python standard library only)
  for a missing or incomplete README, absolute paths and `setwd()`, packages loaded
  after data import, missing seeds, data the code reads but the project lacks,
  Excel-only data, column-name problems, mixed column types, missing-value codes,
  undocumented columns, and clutter.
- **Reviews** the project against every checklist item and writes a report that
  separates required fixes from recommendations, with file and line evidence.
- **Runs** the code in a fresh session where possible and records whether it
  finishes.
- **Checks the paper is reproduced**: it reads your manuscript and supplement,
  lists every figure, table, and reported number, traces each one to the code
  that makes it, and records whether the rerun matches (e.g. "38 of 41 items
  reproduced; 2 not found in code; 1 mismatch").
- **Helps fix**, with your approval: drafts a README and codebook, exports Excel
  sheets to CSV, replaces absolute paths, adds seeds and figure/table labels, and
  sets up quick/full run modes for long analyses.

It does not change your data values or results. It also does not invent metadata
such as units, citations, or who collected the data; it leaves `TODO(author)` for
you to fill in.

## Recommended project layout

Keep the paper next to, but outside, the archive you will deposit:

```text
project_name/
├── ms_files/                  manuscript in any format (.docx, .tex, .qmd, .md, .pdf),
│                              plus figures, tables, supplements: any structure
├── data_and_code/             the archive to deposit: README.md, data, code,
│                              outputs, intermediate files, in any sensible structure
├── .claude/skills/amnat-reproducibility/   added by ./install.sh (Claude Code)
└── .agents/skills/amnat-reproducibility/   added by ./install.sh (Codex)
```

The skill reads `ms_files/` to find every result it must reproduce, and audits
only `data_and_code/`. The manuscript is optional; without it, the skill can
check the archive but not whether it reproduces the paper. Other layouts work
too; the agent will ask where things are.

## Long analyses

For MCMC, large simulations, and bioinformatics pipelines, the skill recommends
archiving the full code, the full outputs of the slow steps (which downstream code
reads to rebuild every figure and table), and a quick mode that runs the slow steps
at reduced scale in minutes. See
[`references/long-computations.md`](skills/amnat-reproducibility/references/long-computations.md).

## Install

```sh
git clone https://github.com/yanivjb/data_editor
cd data_editor
./install.sh /path/to/project_name   # Claude Code and Codex, this project only
./install.sh --user                  # Claude Code and Codex, all your projects
./install.sh --claude --user         # Claude Code only
```

This copies `skills/amnat-reproducibility/` to `.claude/skills/` (Claude Code)
and/or `.agents/skills/` (Codex). You can also copy the folder by hand.

## Use

Open your project in Claude Code or Codex and ask, for example:

- "Check this project against the AmNat data and code checklist."
- "Do a quick reproducibility scan before I submit."
- "Write a README and codebook for the Dryad archive."
- "My brms model takes 8 hours. How should I archive it?"

In Claude Code you can also type `/amnat-reproducibility`; in Codex, `$amnat-reproducibility`
or `/skills`. The agent asks how deep you want to go: a quick scan, a full review,
or a review with guided fixes.

To run the scripts with no agent:

```sh
python3 skills/amnat-reproducibility/scripts/audit_archive.py /path/to/project_name
python3 skills/amnat-reproducibility/scripts/manuscript_items.py /path/to/project_name/ms_files
```

## Contents

```text
skills/amnat-reproducibility/
├── SKILL.md                       instructions the agent follows
├── references/
│   ├── amnat-checklist.md         the journal checklist, with item IDs
│   └── long-computations.md       Bayesian, simulation, and pipeline guidance
├── scripts/
│   ├── audit_archive.py           automated scan of the archive
│   └── manuscript_items.py        lists figures, tables, and numbers in the paper
└── templates/
    ├── README_template.md         README in the journal's required order
    ├── codebook_template.csv      variable-level codebook
    └── AGENTS_snippet.md          rules to add to a project's AGENTS.md/CLAUDE.md
```

## Source and caveats

The checklist is from Bolnick, Schürch, Vedder, Reuter, Perez & Montgomerie
(2021), *From the Editor's Desk of The American Naturalist*. Journal policy can
change, so check the current
[Instructions for Authors](https://www.journals.uchicago.edu/journals/an/instruct)
before you submit.
