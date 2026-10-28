# AmNat reproducibility skill

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23744295.svg)](https://doi.org/10.5281/zenodo.23744295)

> **Beta.** This skill is new and still being tested. Comments, problems, and
> suggestions are very welcome: [open an issue](https://github.com/yanivjb/data_editor/issues/new)
> or email Yaniv Brandvain (ybrandva AT umn dot edu).

> **Before you use it, check your institution's and your journal's rules.** A
> coding agent sends what it reads to its model provider (Anthropic or OpenAI).
> Make sure that using an AI agent on your project is allowed by your
> institution (research data policies, ethics or IRB approvals, data-use
> agreements, permits) and by the journal you are submitting to (its policy on
> AI assistance, and any disclosure it requires). 

An optional helper for authors that works with Claude Code or Codex. Before you
submit to *The American Naturalist*, it checks your data, code, and README against
the journal's
[checklist for archiving data and code](http://comments.amnat.org/2021/12/guidelines-for-archiving-code-with-data.html)
and against reproducibility best practice, checks that your code reproduces every
result in your manuscript, and helps you fix what you choose.

It is a pre-submission aid, not part of the journal's review: the journal's data
editors still decide what is acceptable. Use it early, while the analysis is still
being written, when fixes are cheap.

**AI Statement.** This product was developed with and written by claude code.

**Other journals.** The skill is built around *The American Naturalist*'s
checklist. Its practices are good ones and will likely serve you well at any
journal. If you are submitting elsewhere, tell the agent which journal and give it
that journal's data and code policy (a link, the text, or a PDF). It will check
your project against both, note where the journal's rules differ, and follow the
journal's sharing expectations, for example if human-subject data may only be
shared as summaries or through controlled access.

## Quick start

The steps below get a first review running. For the whole process, see the
**[user guide](docs/user-guide.md)**: a suggested workflow from first review to
deposit (going through mismatches, answering the to-do list, fixing the archive,
correcting the manuscript with tracked changes, and wrapping up), with prompts you
can paste at each step, plus troubleshooting and other reference.

1. Install [Claude Code](https://code.claude.com/docs) or
   [Codex](https://developers.openai.com/codex), and Python 3.
2. Make a folder for the paper with a short name, e.g. `selfing_speciation/`, and
   inside it two folders:

   ```text
   selfing_speciation/
   ├── ms_files/          your manuscript and supplement (any format), figure files
   └── data_and_code/     what you will deposit:
       ├── README.md      describes your data and code for readers (or README.txt)
       ├── data/          e.g. your CSV files
       └── code/          e.g. your R or Python scripts
   ```

   The README for your data and code goes in `data_and_code/`, at the top. If you
   don't have one yet, the agent can draft it. Inside `data_and_code/`, any
   sensible structure works. If your files are elsewhere or arranged differently,
   the agent will offer to help reorganise them.
3. Start the agent in your project folder (`cd selfing_speciation`, then `claude`
   or `codex`) and ask it to install the skill:

   > Clone https://github.com/yanivjb/data_editor somewhere outside this project
   > and run its install.sh for this folder.

   Then quit the agent and start it again, so it loads the skill. (To install by
   hand instead: `git clone https://github.com/yanivjb/data_editor`, then
   `data_editor/install.sh /path/to/selfing_speciation`.)
4. Ask: "Check this project against the AmNat data and code checklist."
5. Answer its questions: whether your institution's and journal's rules allow
   using an AI agent, which journal you are submitting to, what it may read, and
   whether any data are sensitive. Read the one-page `REPRODUCIBILITY_REPORT.md` and work through
   `AUTHOR_TODO.md`; details are in `reproducibility_review/`.
6. Carry on with the [user guide](docs/user-guide.md) for what to do next and
   suggested prompts.

## What it does

- **Asks first** what it may read, because a coding agent sends what it reads to
  its model provider: everything, code and manuscript but not data, or only what
  you paste in. It also asks whether any data are sensitive (e.g. threatened-species
  locations, personal data, permit limits) and guides you through sharing options.
  It never uploads, pushes, or deposits anything.
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
  that makes it, and records whether the rerun matches (e.g. "38 of 41
  computational items reproduced; 2 not found in code; 1 mismatch"). Every
  "match" is backed by a logged command and output file.
- **Asks about figures** that look drawn, photographed, or polished in a graphics
  editor, checks that editing did not change the data shown, and records each in
  the README.
- **Flags point-and-click analyses** (Excel, JMP, Prism, GUI-only phylogenetics,
  and so on), which cannot be reproduced, and helps write scripted versions.
- **Helps fix**, with your approval: drafts a README and codebook, exports Excel
  sheets to CSV, replaces absolute paths, adds seeds and figure/table labels, and
  sets up quick/full run modes for long analyses.

It does not change your data values or results. It also does not invent metadata
such as units, citations, or who collected the data. Anything it needs from you
goes in `AUTHOR_TODO.md`, outside the archive, so the README stays clean for
readers.

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
at reduced scale in minutes. It includes specific advice for SLiM simulations. See
[`references/long-computations.md`](skills/amnat-reproducibility/references/long-computations.md).

## Languages

The agent can read and check code in any language. The scan recognises R, R
Markdown, Quarto, Python, Jupyter, Julia, MATLAB, Mathematica, C/C++, Fortran,
Rust, Go, Java, Stan, JAGS, SLiM, Stata, SAS, shell scripts, Snakemake, and
Nextflow, and checks seeds, paths, and data reads for the common ones. The agent
can only rerun code whose runtime is installed; MATLAB and Mathematica also need
licences. Otherwise it checks by reading, marks results **not rerun**, and gives
you the commands to run yourself.

## More

- [User guide](docs/user-guide.md): the workflow from review to deposit with
  prompts to paste, setup details, privacy, and troubleshooting.
- [Contributing](CONTRIBUTING.md): repository layout and tests.

## How to cite

If you use this skill, please cite it:

> Brandvain, Y. AmNat reproducibility skill: an AI agent helper for archiving data
> and code. Zenodo. https://doi.org/10.5281/zenodo.23744295

This DOI always points to the latest version; each release also has its own DOI,
listed on the [Zenodo record](https://doi.org/10.5281/zenodo.23744295). GitHub's
"Cite this repository" button (right-hand side of the repository page) gives the
citation in APA and BibTeX, from [`CITATION.cff`](CITATION.cff).

## License

[MIT](LICENSE).

## Source and caveats

The checklist is from Bolnick, Schürch, Vedder, Reuter, Perez & Montgomerie
(2021), *From the Editor's Desk of The American Naturalist*. Journal policy can
change, so check the current
[Instructions for Authors](https://www.journals.uchicago.edu/journals/an/instruct)
before you submit.
