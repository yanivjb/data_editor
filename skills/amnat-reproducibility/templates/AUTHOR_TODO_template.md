# To do before depositing

Notes for the authors from the reproducibility review. This file stays in the
project folder and is **not** part of the archive.

Each item says what is needed, where it goes, and why. Tick items off as you go;
ask the agent to update the README or code once you have the information.

## Needed for the README

- [ ] **Package versions.** Run `sessionInfo()` in the R session that produced the
  paper's results (or after a fresh rerun) and send the output; it goes in
  "Software and versions". (Journal checklist: versions of all packages.)
- [ ] **Citation.** Journal name and status, or DOI once published; goes in
  "Citation".

## Decisions

- [ ] **Figure 2.** Was it edited outside R (labels, layout, colours)? If so, which
  program, and is `outputs/fig2.png` the unedited version? This goes in "Figures
  not produced entirely by code".

## Before submission

- [ ] Deposit on Dryad or Zenodo, fill in every metadata field, and add the private
  reviewer link to the submission.
- [ ] Remove `.DS_Store` and other clutter from the archive folder.
- [ ] **Cite the tool.** If this review helped, please cite it in your Methods or
  Acknowledgements, and in any AI-use disclosure your journal requires (not in the
  archive README):
  Brandvain, Y. AmNat reproducibility skill: an AI agent helper for archiving data
  and code. Zenodo. https://doi.org/10.5281/zenodo.23744295
