# User guide

A suggested workflow from first review to deposit, with prompts you can paste at
each step, followed by reference sections. To get set up, follow the quick start in
the [README](../README.md); [Setup details](#setup-details) below covers
installing without git and other setup questions.

The skill is an optional pre-submission aid. It does not submit anything to the
journal, and passing it does not guarantee acceptance: the journal's data editors
make that decision.

**Workflow**

1. [Review](#1-review)
2. [Read the report](#2-read-the-report)
3. [Go through the mismatches](#3-go-through-the-mismatches)
4. [Answer the to-do list](#4-answer-the-to-do-list)
5. [Fix the archive](#5-fix-the-archive)
6. [Correct the manuscript (optional)](#6-correct-the-manuscript-optional)
7. [Wrap up](#7-wrap-up)
8. [Deposit](#8-deposit)

[Tips](#tips)

**Reference:**
[Setup details](#setup-details) ·
[Result statuses](#result-statuses) ·
[Files the review creates](#files-the-review-creates) ·
[Slow analyses](#slow-analyses) ·
[Privacy](#privacy) ·
[Troubleshooting](#troubleshooting) ·
[Scripts without an agent](#scripts-without-an-agent)

Before you start, work on a copy of your project or commit it to git, so you can
always go back.

## 1. Review

In your project folder, start `claude` or `codex` and ask:

> Do a full reproducibility review of this project using the
> amnat-reproducibility skill. My manuscript and supplement are in ms_files/.

Before it reads anything, the agent asks:

1. **What may it read?** Everything; code, README, and manuscript but not data
   contents; or only what you paste in. What it reads is sent to Anthropic or
   OpenAI: see [Privacy](#privacy).
2. **Are any data sensitive or restricted?** For example threatened-species
   locations, personal data, Indigenous data, or data under a permit or license.
   If so, it will not read those files and will go through sharing options with
   you.
3. **How deep should it go?** A quick scan (minutes), a full review (no files
   changed), or a review followed by fixes you choose.

In a full review it scans the archive for common problems, checks every item of
the journal's checklist, reruns your code in a fresh session, and checks every
figure, table, and number in your manuscript and supplement against the rerun. It
asks before starting anything slow, and asks you about figures that look drawn,
photographed, or edited in a graphics program. Expect an hour or more, plus your
code's run time.

It does not change your data or results, and does not invent information such as
units or citations: anything only you know goes on your to-do list.

Other things you can ask for:

> Do a quick reproducibility scan before I submit.

> Write a README and codebook for the Dryad archive.

> My brms model takes 8 hours. How should I archive it?

## 2. Read the report

Two files appear at the top of your project folder:

- `REPRODUCIBILITY_REPORT.md`: one page with the verdict, the results check, and
  what to fix;
- `AUTHOR_TODO.md`: checkboxes for what only you can supply or decide.

The details are in `reproducibility_review/` (see
[Files the review creates](#files-the-review-creates)). A short report for one of
the test projects in this repository looks like this:

> **Verdict.** The code runs and reproduces Table 1 and Figure 2. One number in the
> Results differs from the code and one has no code. The README needs a citation,
> who collected the data, and software versions before you deposit.
>
> **Results check.** 6 of 8 results reproduced; 1 differs; 1 has no code.
> - Results ¶1, survival under heat: 45.3% in the paper, 43.3% from the code.
> - Results ¶1, "body mass did not differ (p = 0.43)": no code computes this test.
>
> **What to fix**
> 1. Correct or explain the survival value above.
> 2. Add the code for the body-mass test.
> 3. Complete the README: citation, who collected the data, package versions.
> 4. Save the survival difference to a file, not only to the console (recommended).
>
> **What we need from you:** see `AUTHOR_TODO.md` (3 items).
>
> Checked: all code and data; everything was rerun. Details:
> `reproducibility_review/full_report.md`.

## 3. Go through the mismatches

Mismatches between the paper and the code matter most. Take them one at a time:

> Walk me through the mismatches one at a time, starting with any that change a
> conclusion. For each, show me where it is in the manuscript and in the code
> output, and what you think caused it.

> Is this a typo, or did the manuscript come from an earlier version of the
> analysis?

> Where is this in the compiled HTML? I want to check it myself.

A mismatch is often a typo in the manuscript, but it can also mean the paper
reports an older analysis, or that the code changed. Decide for each one which is
right; the agent will not decide for you.

## 4. Answer the to-do list

> Here are my answers to AUTHOR_TODO.md: ...

> I don't know this one yet. Leave it on the list and move on.

If you find an error in your data, such as two beetles with the same ID:

> Beetle B017 in the mass sheet is a different individual. Correct it in the code,
> not the raw file, and tell me what it changes.

The agent makes the correction in a labelled step in the code, so readers can see
it, and describes it in the README.

## 5. Fix the archive

> Fix the required items in data_and_code/. Show me each change before you make it.

> Fix the required items except the README; I'll write that myself.

> Write the README for readers: no notes to me, no checklist codes.

> Rerun everything from scratch and confirm the results did not change.

The agent can draft a README in the journal's required order and a codebook of
your variables, save Excel sheets as CSV, replace absolute paths, add random seeds
and labels linking code to figures and tables, set up quick and full run modes for
slow analyses, and script an analysis you did by pointing and clicking.

Two things to watch:

- **Adding a random seed changes random results slightly.** Regenerate the affected
  numbers from the seeded code and update the manuscript.
- **Scripting a point-and-click analysis can change results.** The agent reports
  any difference; decide with your co-authors how to report it.

If you are still writing the analysis:

> Add the skill's coding rules to this project's AGENTS.md (or CLAUDE.md).

Coding agents working in your project will then follow them from the start.

## 6. Correct the manuscript (optional)

Only for corrections you have decided on:

> Make tracked-change copies of the manuscript and supplement in
> revised_manuscript/ for the corrections we agreed. Add a Word comment to each
> changed number saying where the new value comes from.

> For the result that is no longer significant, suggest wording in a comment, but
> don't change my interpretation.

Every change is a Word tracked change in a copy; your originals are not touched.
Review the changes in Word, and accept or reject them yourself.

## 7. Wrap up

> We're done. Rerun everything from scratch with the final code and data,
> regenerate every figure and table, and check they still match the manuscript.

This matters most if anything changed during the review (a data correction, a code
fix, a new R version): figures made before the change will be out of date.

> Put the tracked copies back in ms_files/, replacing the old versions. Don't accept
> any tracked changes; I'll do that. Tell me first how I can get the old versions
> back.

> Write WHAT_CHANGED.md: a summary of every change I can send to my co-authors.

> Update AUTHOR_TODO.md so it lists only what is left for me.

> Clean up: delete the scratch files, keep the full report and run log, and list
> what you deleted.

Afterwards your project folder holds your own folders plus `AUTHOR_TODO.md`,
`WHAT_CHANGED.md`, `REPRODUCIBILITY_REPORT.md`, and a small
`reproducibility_review/` folder recording what was checked.

## 8. Deposit

> Do a final check before I deposit: is AUTHOR_TODO.md done, is the README clean
> for readers, and is data_and_code/ free of clutter?

Then, yourself:

- deposit `data_and_code/` on **Dryad or Zenodo** (a GitHub repository alone does
  not count; a GitHub release archived on Zenodo does), filling in every metadata
  field;
- put the private reviewer link in your submission;
- if any data are withheld or de-identified, say so in the README and raise it with
  the editor at submission;
- check the current
  [Instructions for Authors](https://www.journals.uchicago.edu/journals/an/instruct).

The agent never uploads or deposits anything.

## Tips

- **Short answers are fine.** "Yes", "separate individuals", "move on" all work.
  If you say move on, the agent records the open point and continues.
- **Ask to see evidence.** "Show me the output", "which line?", "how did you get
  that number?"
- **If the agent goes off track,** say so plainly: "Stop. Don't edit the raw
  data." It should follow you.

---

## Setup details

**What you need.**
[Claude Code](https://code.claude.com/docs) or
[Codex](https://developers.openai.com/codex), installed and signed in (both need an
account; usage may cost money depending on your plan); Python 3 (check with
`python3 --version`; on Windows install it from
[python.org](https://www.python.org/downloads/)); and the software your analysis
uses, on the same computer, so the agent can rerun your code.

**Project layout.** One folder per paper, e.g. `selfing_speciation/`, containing:

```text
selfing_speciation/
├── ms_files/              manuscript, supplement, and figure files; any names
└── data_and_code/         what you will deposit on Dryad or Zenodo
    ├── README.md          describes the data and code for readers (or README.txt)
    ├── data/
    ├── code/
    └── outputs/
```

The names inside `data_and_code/` are suggestions. The README describing your data
and code goes at the top of `data_and_code/`, because it is deposited with them.
If your project is organised differently, the agent will ask where things are; if
you move files to match this layout, rerun your code, since paths in your scripts
may need updating.

**Installing.** The easiest way is to ask the agent. Start it in your project
folder and say:

> Clone https://github.com/yanivjb/data_editor somewhere outside this project and
> run its install.sh for this folder.

Then quit and restart the agent so it loads the skill. To update later, ask the
same again. To install by hand with git: `git clone https://github.com/yanivjb/data_editor`, then
`data_editor/install.sh /path/to/selfing_speciation`. Use `--user` instead of a
path to install for all your projects, and `--claude` or `--codex` for one tool.
Without git: on the GitHub page click **Code → Download ZIP**, unzip it, and copy
`skills/amnat-reproducibility` into `selfing_speciation/.claude/skills/` (Claude
Code) or `selfing_speciation/.agents/skills/` (Codex). Folders starting with a dot
are hidden: on a Mac press <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> in Finder;
on Windows choose **View → Show → Hidden items**. To update, repeat the install.

**Starting the agent.** `cd /path/to/selfing_speciation`, then `claude` or `codex`.
Claude Code also runs in its desktop app and in VS Code: open the project folder
there. You can call the skill by name with `/amnat-reproducibility` (Claude Code)
or `$amnat-reproducibility` (Codex).

## Result statuses

Each figure, table, and number in the manuscript is marked:

| Status | Meaning |
|--------|---------|
| match | the rerun gives the reported value (within sampling error for MCMC and other random results) |
| mismatch | the rerun gives a different value; both are shown |
| not found in code | nothing in the archive produces it |
| not rerun | the code exists but could not be run here, with the reason |
| edited after code | a code-made figure later polished in another program; the data shown are still checked |
| not computational | a diagram, drawing, or photo, confirmed with you |

In the full report each finding also cites a checklist item, e.g. `CODE-2`
(relative paths) or `DATA-5` (Excel sheets saved as CSV); the list is in
[`references/amnat-checklist.md`](../skills/amnat-reproducibility/references/amnat-checklist.md).

## Files the review creates

| File | Contents |
|------|----------|
| `REPRODUCIBILITY_REPORT.md` | one-page summary |
| `AUTHOR_TODO.md` | what only you can supply or decide |
| `WHAT_CHANGED.md` | summary of all changes, written when you wrap up |
| `revised_manuscript/` | tracked-change copies, only if you ask for manuscript corrections |
| `reproducibility_review/full_report.md` | every finding with evidence, and the full table of manuscript results |
| `reproducibility_review/runlog.md` | every command the agent ran, and whether it worked |
| `reproducibility_review/audit.md` | the automated scan |
| `reproducibility_review/manuscript_items.md` | figures, tables, and numbers found in the manuscript |
| `reproducibility_review/work/` | scratch files; safe to delete |

Nothing from the review is put in `data_and_code/` or `ms_files/` unless you ask.

## Slow analyses

If part of your analysis takes hours or days (MCMC, large simulations, SLiM,
bioinformatics pipelines), archive the full code with its settings and seeds, the
full outputs of the slow steps (which your figure and table code reads in), and a
quick mode that runs the slow steps at reduced scale in minutes. The agent will
not start a long run without asking; it runs the quick mode, reruns everything
downstream of the archived outputs, and marks the slow steps "not rerun". Details
are in
[`references/long-computations.md`](../skills/amnat-reproducibility/references/long-computations.md).

## Privacy

- Your code runs on your computer. What leaves it is what the agent reads: file
  contents, command output, and the helper scripts' reports, sent to Anthropic
  (Claude Code) or OpenAI (Codex) under your account's terms.
- Before letting it read everything, check your institution's rules, any data-use
  agreement, and your agent account's data settings.
- With "not data contents", the scan reports only column names, counts, and types.
- The agent never uploads, pushes, posts, or deposits anything.

## Troubleshooting

| Problem | What to do |
|---------|------------|
| The agent does not seem to use the skill | Call it by name (`/amnat-reproducibility` or `$amnat-reproducibility`). Check the skill folder is in `.claude/skills/` or `.agents/skills/` inside the folder where you started the agent. |
| Many items are "not rerun" because R, MATLAB, etc. are missing | Run the agent on the computer where your analysis normally runs, or run the commands it gives you and share the output. |
| R packages fail to load | Install them, or run `renv::restore()` if your project has an `renv.lock`. The agent can help set up `renv`. |
| The report lists many findings | Start with the required fixes. Recommended items are optional. |
| A finding is wrong | The scan uses pattern matching and makes mistakes. Tell the agent; it should check by reading the code. |
| The PDF manuscript cannot be read | Install `pdftotext` (part of poppler), or put a `.docx`, `.md`, or `.txt` version in `ms_files/`. |
| A number moved while fixing | Ask the agent to compare the before and after outputs; it keeps a log. Do not report numbers you have not regenerated. |
| `reproducibility_review/work/` is large | Delete it once you have the reports, or ask the agent to. |

## Scripts without an agent

The helper scripts need only Python 3:

```sh
# scan the archive; writes selfing_speciation/reproducibility_review/audit.md
python3 path/to/amnat-reproducibility/scripts/audit_archive.py selfing_speciation --out reproducibility_review/audit.md

# the same, without showing any data values
python3 path/to/amnat-reproducibility/scripts/audit_archive.py selfing_speciation --no-values

# list the figures, tables, and numbers in the manuscript
python3 path/to/amnat-reproducibility/scripts/manuscript_items.py selfing_speciation/ms_files --out selfing_speciation/reproducibility_review/manuscript_items.md

# apply edits to a copy of a Word file as tracked changes (see the script's header for the format)
python3 path/to/amnat-reproducibility/scripts/docx_track_changes.py ms_files/manuscript.docx edits.json --out revised_manuscript/manuscript_tracked.docx
```

The scan finds leads, not verdicts. It cannot run your code or check results
against the paper; that is what the agent adds.
