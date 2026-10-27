# User guide

This guide walks you through using the AmNat reproducibility skill, from setup to
depositing your archive. It assumes you are comfortable running your own analysis
code, but not necessarily with the terminal or with coding agents.

The skill is an optional pre-submission aid. It does not submit anything to the
journal, and passing it does not guarantee acceptance: the journal's data editors
make that decision.

## Contents

1. [What you need](#1-what-you-need)
2. [Organise your project](#2-organise-your-project)
3. [Install the skill](#3-install-the-skill)
4. [Start a review](#4-start-a-review)
5. [Answer the agent's first questions](#5-answer-the-agents-first-questions)
6. [What the agent does](#6-what-the-agent-does)
7. [Read the report](#7-read-the-report)
8. [Fix problems](#8-fix-problems)
9. [Before you deposit](#9-before-you-deposit)
10. [Slow analyses](#10-slow-analyses)
11. [Troubleshooting](#11-troubleshooting)
12. [Privacy](#12-privacy)
13. [Using the scripts without an agent](#13-using-the-scripts-without-an-agent)

## 1. What you need

- **A coding agent**: either
  [Claude Code](https://code.claude.com/docs) (Anthropic) or
  [Codex](https://developers.openai.com/codex) (OpenAI), installed and signed in.
  Both need an account; usage may cost money depending on your plan. Follow their
  install instructions.
- **Python 3**, for the skill's two helper scripts. Most Macs and Linux machines
  have it; check with `python3 --version`. On Windows, install it from
  [python.org](https://www.python.org/downloads/).
- **The software your analysis uses** (R, Python packages, Julia, MATLAB, ...),
  installed on the same computer, so the agent can rerun your code. If something is
  missing the agent will still check what it can, and tell you what it could not
  run.
- **Your manuscript**, in any format (`.docx`, `.tex`, `.md`, `.qmd`, `.pdf`).
  Optional, but without it the agent cannot check that your code reproduces the
  paper.

Plan on 15 minutes for a quick scan, and an hour or more for a full review of a
typical project, plus the time your code takes to run.

## 2. Organise your project

Put the paper and the archive side by side in one folder:

```text
my_paper/
├── ms_files/          your manuscript, supplement, and figure files
└── data_and_code/     everything you will deposit: README, data, code, outputs
```

- **`ms_files/`** can be organised however you like. The agent reads it to find
  every result it needs to check. It is never part of the archive.
- **`data_and_code/`** is what will go to Dryad or Zenodo. Use any sensible
  structure, for example `data/`, `code/`, `outputs/`, and a `README.md`.

If your project is organised differently, that is fine: the agent will ask where
your manuscript and archive are. If you move files to match this layout, rerun your
code afterwards, because file paths in your scripts may need updating. (The agent
can help with that.)

## 3. Install the skill

**Option A: with git (Mac, Linux, or Windows with Git Bash).** In a terminal:

```sh
git clone https://github.com/yanivjb/data_editor
cd data_editor
./install.sh /path/to/my_paper
```

This puts the skill in `my_paper/.claude/skills/` (for Claude Code) and
`my_paper/.agents/skills/` (for Codex). To install it for all your projects
instead, use `./install.sh --user`. To install for one tool only, add `--claude` or
`--codex`.

**Option B: without git.** On the GitHub page, click **Code → Download ZIP** and
unzip it. Copy the folder `skills/amnat-reproducibility` into your project:

- for Claude Code: `my_paper/.claude/skills/amnat-reproducibility/`
- for Codex: `my_paper/.agents/skills/amnat-reproducibility/`

Folders starting with a dot are hidden by default. On a Mac press
<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> in Finder to show them; on Windows
choose **View → Show → Hidden items** in File Explorer.

To update later, repeat the same steps; the installer replaces the old copy.

## 4. Start a review

Open a terminal in your project folder and start the agent:

```sh
cd /path/to/my_paper
claude        # Claude Code
# or
codex         # Codex
```

(Claude Code also runs in its desktop app and in VS Code; open the `my_paper`
folder there.)

Then ask for what you want, in plain words. For example:

- "Check this project against the AmNat data and code checklist."
- "Do a quick reproducibility scan before I submit."
- "Check that my code reproduces every result in the manuscript."
- "Write a README and codebook for the Dryad archive."
- "My brms model takes 8 hours. How should I archive it?"

You can also call the skill by name: type `/amnat-reproducibility` in Claude Code,
or `$amnat-reproducibility` in Codex.

## 5. Answer the agent's first questions

Before it reads your files, the agent asks:

1. **What may it read?** Anything the agent reads is sent to the company that runs
   it (Anthropic or OpenAI). Choose one:
   - **everything**;
   - **code, README, and manuscript, but not data contents**: the agent works from
     file names, column names, and counts, and never prints your data;
   - **only what you paste in**: the agent gives you commands to run and works from
     the output you choose to share.

   See [Privacy](#12-privacy) before choosing.
2. **Are any data sensitive or restricted?** For example locations of threatened
   species, personal or human-subject data, Indigenous data, or data under a permit
   or license that limits sharing. If so, the agent will not read those files and
   will go through options with you (see [Before you deposit](#9-before-you-deposit)).
3. **How deep should it go?**
   - **Quick scan**: an automated check and a short summary. Minutes.
   - **Full review**: everything in the next section, ending in a written report.
     Nothing is changed.
   - **Review and fix**: a full review, then help fixing the items you choose.

## 6. What the agent does

In a full review, the agent:

1. **Scans the archive** with a helper script for common problems: a missing or
   incomplete README, absolute file paths, `setwd()`, packages loaded mid-script,
   missing random seeds, data in Excel only, unclear column names, missing-value
   codes, and analyses done in point-and-click software.
2. **Reads your code and README**, works out the run order, and checks every item
   of the journal's checklist.
3. **Reruns your code** in a fresh session, logging every command it runs. It asks
   before starting anything slow.
4. **Checks the manuscript.** It lists every figure, table, and reported number in
   your main text and supplement, finds the code that produces each one, and
   compares the rerun with the paper. Each item is marked:

   | Status | Meaning |
   |--------|---------|
   | match | the rerun gives the reported value (within sampling error for MCMC and other random results) |
   | mismatch | the rerun gives a different value; both are shown |
   | not found in code | nothing in the archive produces it |
   | not rerun | the code exists but could not be run here, with the reason |
   | edited after code | a code-made figure later polished in another program; the data shown are still checked |
   | not computational | a diagram, drawing, or photo, confirmed with you |

5. **Asks you about figures** that look drawn, photographed, or edited in a
   graphics program, rather than guessing.

It does **not** change your data, change results, or invent information such as
units, citations, or who collected the data. Where it needs something only you
know, it adds the item to `AUTHOR_TODO.md` and asks you. The archive README only
ever contains finished text for readers: no to-dos, checklist codes, or notes
about the review.

## 7. Read the report

The agent writes these files in your project folder, outside `data_and_code/`:

| File | Contents |
|------|----------|
| `REPRODUCIBILITY_REPORT.md` | the review: verdict, required fixes, recommendations, questions for you, and the manuscript check |
| `REPRODUCIBILITY_RUNLOG.md` | every command the agent ran, with how long it took and whether it worked |
| `AUTHOR_TODO.md` | a checklist of what only you can supply or decide (package versions, citation, how a figure was made, ...) |
| `REPRODUCIBILITY_AUDIT.md` | the automated scan |
| `MANUSCRIPT_ITEMS.md` | the figures, tables, and numbers found in your manuscript |

Work through the report in order:

1. **Required fixes**: what a data editor would ask you to change. Each cites a
   checklist item, e.g. `CODE-2` (relative paths) or `DATA-5` (Excel sheets saved
   as CSV); the full list is in
   [`references/amnat-checklist.md`](../skills/amnat-reproducibility/references/amnat-checklist.md).
2. **Recommended improvements**: good practice, not required.
3. **Questions for you**: information only you have, listed with checkboxes in
   `AUTHOR_TODO.md`. Once you have the answers, ask the agent to put them in the
   README.
4. **The manuscript check**, with a summary such as "38 of 41 computational items
   reproduced; 2 not found in code; 1 mismatch".

A mismatch is often a typo in the manuscript rather than a problem in the code.
The agent reports it either way and leaves it to you to decide which is right.

Here is part of a report for one of the test projects in this repository:

> **Verdict.** The code runs and reproduces Table 1 and Figure 2, but one number in
> the Results does not match and one has no code. The README lacks a citation,
> who collected the data, and software versions.
>
> | Manuscript item | Value in paper | Produced by | Value from rerun | Status |
> |-----------------|----------------|-------------|------------------|--------|
> | Results ¶1, survival under heat | 45.3% | `code/01_analysis.py:21` | 43.3% | mismatch |
> | Results ¶1, mass t-test | p = 0.43 | not found | — | not found in code |
> | Table 1, all cells | | `code/01_analysis.py:21` | identical | match |
> | Figure 1 | (design diagram) | — | — | not computational |
> | Figure 2 | (plot) | `code/01_analysis.py:32` | same data; restyled | edited after code, data match |

## 8. Fix problems

Ask the agent to fix the items you choose, e.g. "Fix the required items except the
README; I'll write that myself." It can:

- draft a README in the journal's required order, and a codebook of your variables;
- save each Excel sheet as a CSV and point your code at it;
- replace absolute paths with relative ones;
- add random seeds and labels linking code to figure and table numbers;
- set up quick and full run modes for slow analyses;
- write a scripted version of a point-and-click analysis.

It shows you each change. Two things to watch:

- **Adding a random seed changes random results slightly.** Regenerate the affected
  numbers from the seeded code and update the manuscript.
- **Rewriting a point-and-click analysis as a script can change results.** The
  agent reports any difference; decide with your coauthors how to report it.

When you are done, ask for the review again to confirm the fixes.

If you are still writing the analysis, ask the agent to add the skill's short
coding rules to your project's `AGENTS.md` or `CLAUDE.md`. Coding agents working
in your project will then follow them from the start.

## 9. Before you deposit

- **Keep only what is needed** in `data_and_code/`: README, data, code, and any
  outputs readers need. Remove `.Rhistory`, `.DS_Store`, caches, drafts, and
  manuscript files.
- **Deposit in Dryad or Zenodo.** A GitHub repository alone does not count, but a
  GitHub release archived on Zenodo does. Fill in every metadata field, and get a
  private reviewer link to give the journal at submission.
- **Sensitive data**: share a coarsened or de-identified version (e.g. coordinates
  rounded to a grid), use controlled access, or explain how to obtain the data.
  Say in the README what was withheld or changed and why, and raise it with the
  editor at submission. The agent can help write the de-identification script and
  the README text; do the de-identification outside `data_and_code/`, so the
  original data never end up in the archive.
- **Check the current journal policy** in the
  [Instructions for Authors](https://www.journals.uchicago.edu/journals/an/instruct).

The agent never uploads or deposits anything: you do that yourself.

## 10. Slow analyses

If part of your analysis takes hours or days (MCMC, large simulations, SLiM,
bioinformatics pipelines), the recommended setup is:

1. the full code, with the settings and seeds used for the paper;
2. the full outputs of the slow steps, archived, which your figure and table code
   reads in;
3. a quick mode that runs the slow steps at reduced scale in minutes, to show the
   code works.

The agent will not start a long run without asking. It runs the quick mode, reruns
everything downstream of the archived outputs, and marks the slow steps "not
rerun". Details for Bayesian models, simulations, SLiM, and pipelines are in
[`references/long-computations.md`](../skills/amnat-reproducibility/references/long-computations.md).

## 11. Troubleshooting

| Problem | What to do |
|---------|------------|
| The agent does not seem to use the skill | Call it by name (`/amnat-reproducibility` in Claude Code, `$amnat-reproducibility` in Codex). Check that the skill folder is in `.claude/skills/` or `.agents/skills/` inside the folder where you started the agent. |
| Many items are "not rerun" because R, MATLAB, etc. are missing | Run the agent on the computer where your analysis normally runs. Or run the commands the agent gives you and share the output. |
| R packages fail to load | Install them, or use `renv` (`renv::restore()`) if your project has an `renv.lock`. The agent can help set up `renv`. |
| The report lists many findings | Start with the required fixes. Many recommended items are quick, but none are mandatory. |
| A finding is wrong | The scan uses pattern matching and makes mistakes. Tell the agent; it should check by reading the code. |
| The PDF manuscript cannot be read | Install `pdftotext` (part of poppler), or put a `.docx`, `.md`, or `.txt` version in `ms_files/`. |
| Your code changed while fixing and a number moved | Ask the agent to compare the before and after outputs; it keeps a log. Do not report numbers you have not regenerated. |

## 12. Privacy

- Your code **runs on your computer**. What leaves it is what the agent reads:
  file contents, command output, and the helper scripts' reports. These are sent to
  Anthropic (Claude Code) or OpenAI (Codex) under your account's terms.
- Before choosing "everything", check your institution's rules, any data-use
  agreement, and your agent account's data settings.
- With "not data contents", the helper script runs with `--no-values` and reports
  only column names, counts, and types.
- The agent never uploads, pushes, posts, or deposits anything.

## 13. Using the scripts without an agent

Both helper scripts need only Python 3 and work on their own:

```sh
# scan the archive; writes REPRODUCIBILITY_AUDIT.md in my_paper/
python3 path/to/amnat-reproducibility/scripts/audit_archive.py my_paper --out REPRODUCIBILITY_AUDIT.md

# the same, without showing any data values
python3 path/to/amnat-reproducibility/scripts/audit_archive.py my_paper --no-values

# list the figures, tables, and numbers in the manuscript
python3 path/to/amnat-reproducibility/scripts/manuscript_items.py my_paper/ms_files --out MANUSCRIPT_ITEMS.md
```

The scan finds leads, not verdicts. It cannot run your code or check results
against the paper; that is what the agent adds.
