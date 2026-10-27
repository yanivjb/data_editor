# Quick start for authors

A suggested order of work, with prompts you can paste. Setup and details are in
the [user guide](user-guide.md).

## Before you start

- Put your manuscript and supplement in `my_paper/ms_files/`, and the data and code
  you will deposit in `my_paper/data_and_code/`.
- Install the skill (`install.sh my_paper`), then open a terminal in `my_paper/`
  and start `claude` or `codex`.
- Work on a copy, or commit your project to git first, so you can always go back.

## 1. Review

> Do a full reproducibility review of this project using the
> amnat-reproducibility skill. My manuscript and supplement are in ms_files/.

The agent asks what it may read, whether any data are sensitive, and how deep to
go. Then it reruns your code and checks every result in the paper. Expect an hour
or more, plus your code's run time. If something is slow, it will ask before
running it.

When it finishes, read `REPRODUCIBILITY_REPORT.md` (one page) and
`AUTHOR_TODO.md`.

## 2. Go through the mismatches

Mismatches between your paper and your code matter most. Take them one at a time:

> Walk me through the mismatches one at a time, starting with any that change a
> conclusion. For each, show me where it is in the manuscript and in the code
> output, and what you think caused it.

> Is this a typo, or did the manuscript come from an earlier version of the
> analysis?

> Where is this in the compiled HTML? I want to check it myself.

Decide for each one which is right: the paper or the code. The agent will not
decide for you.

## 3. Answer the to-do list

> Here are my answers to AUTHOR_TODO.md: ...

> I don't know this one yet. Leave it on the list and move on.

If you find an error in your data (e.g. two plants with the same ID):

> Plant 131 in the harvest sheet is a different individual. Correct it in the code,
> not the raw file, and tell me what it changes.

## 4. Fix the archive

> Fix the required items in data_and_code/. Show me each change before you make
> it.

> Write the README for readers: no notes to me, no checklist codes.

> Rerun everything from scratch and confirm the results did not change.

## 5. Correct the manuscript (optional)

Only for the corrections you have decided on:

> Make tracked-change copies of the manuscript and supplement in
> revised_manuscript/ for the corrections we agreed. Add a Word comment to each
> changed number saying where the new value comes from.

> For the biomass result that is no longer significant, suggest wording in a
> comment, but don't change my interpretation.

Review the tracked changes in Word, and accept them yourself.

## 6. Final check

> Do a final check before I deposit: is AUTHOR_TODO.md done, is the README clean
> for readers, and is data_and_code/ free of clutter?

> How big is reproducibility_review/work/? Delete it.

Then deposit `data_and_code/` on Dryad or Zenodo yourself, and put the private
reviewer link in your submission.

## Tips

- **Short answers are fine.** "Yes", "separate individuals", "move on" all work.
  If you say move on, the agent should record the open point and continue.
- **Ask to see evidence.** "Show me the output", "which line?", "how did you get
  that number?"
- **Nothing is deposited or sent anywhere** unless you do it.
- **If the agent goes off track,** say so plainly: "Stop. Don't edit the raw
  data." It should follow you.
