## Reproducible archive

This project will be archived with its paper under The American Naturalist's data
and code policy. While writing or changing code and data here:

- Load packages at the top of each script, then read raw data from files in this
  project. Use paths relative to the project root; never `setwd()` to an absolute
  path.
- Keep raw data as CSV and never edit it by hand; do all cleaning, merging, and
  filtering in code.
- Set a random seed for every stochastic step, including samplers.
- Script every analysis step; results produced only through point-and-click
  software cannot be reproduced and are not accepted.
- Label code that produces a manuscript figure or table with its number.
- For slow steps, keep a `quick`/`full` run mode and save full outputs under
  `outputs/full/` for downstream code to read.
- Keep the README's file list, variable descriptions (with units), and software
  versions up to date when files or columns change.

Do not upload, push, or deposit anything without the author's explicit request.

Use the `amnat-reproducibility` skill for a full check before submission.
