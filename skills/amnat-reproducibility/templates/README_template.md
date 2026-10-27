# TODO(author): Title of the data and code archive

<!--
Sections 1-6 are required by The American Naturalist, in this order (DOC-2).
Sections 7 onward are recommended. Replace every TODO(author) with real
information; do not leave guesses in place of facts. Delete these comments.
-->

## 1. Citation

TODO(author): Authors. Year. Title. *The American Naturalist* volume:pages.
DOI. (Use "In review" or "In press" before publication.)

## 2. Authors and contact

- TODO(author): Name, affiliation, email, ORCID
- Corresponding author: TODO(author)

## 3. Study summary

TODO(author): Two to five sentences on the question, study system, and design.

## 4. Responsibilities

- Data collection: TODO(author)
- Code: TODO(author)

## 5. Files and variables

### Folder structure

```text
.
├── README.md          this file
├── data/              raw data (CSV)
├── code/              analysis scripts, run in the order below
└── outputs/           figures, tables, and intermediate results written by the code
```

### Data files

#### `data/example.csv`

TODO(author): What one row represents, how and when the data were collected, and
which analyses use the file. Missing values are coded as `NA`.

| Variable | Description | Type | Units / levels |
|----------|-------------|------|----------------|
| `site` | Sampling site | categorical | `A`, `B`, `C` |
| `mass_g` | Fresh body mass | numeric | g |

<!-- Repeat for every data file. A separate codebook CSV is acceptable
(DATA-3); if you use one, name it here. Explain how files link to each other,
e.g. "join on `plant_id`". -->

### Code files

| File | Purpose | Reads | Writes | Manuscript output |
|------|---------|-------|--------|-------------------|
| `code/01_clean.R` | TODO(author) | `data/example.csv` | `outputs/clean.rds` | — |
| `code/02_models.R` | TODO(author) | `outputs/clean.rds` | `outputs/fig1.pdf` | Figure 1, Table 1 |

### Output files

TODO(author): List intermediate and final outputs, noting which are provided so
slow steps need not be rerun (CODE-12).

## 6. Software and versions

- Operating system: TODO(author)
- R TODO(author) / Python TODO(author)
- Packages: TODO(author). Paste the output of `sessionInfo()` in R or
  `pip list --format freeze` in Python, or point to `renv.lock` /
  `requirements.txt`.

Packages installed by the scripts themselves: TODO(author) or "none".

## 7. How to reproduce the results

1. Download the archive and open a terminal in its top-level folder.
2. Install the software listed in section 6.
3. Run the scripts in order, for example:

   ```sh
   Rscript code/01_clean.R
   Rscript code/02_models.R
   ```

TODO(author): Random seeds used, and how to start from the provided
intermediate outputs instead of rerunning slow steps.

### Computational cost

<!-- Needed if any step takes more than a few minutes. See
references/long-computations.md in the reproducibility skill. -->

| Step | Full run time | Hardware | Quick mode | Archived outputs |
|------|---------------|----------|------------|------------------|
| `code/02_models.R` | TODO(author), e.g. 6 h | TODO(author), e.g. 4 cores, 16 GB RAM | `RUN_MODE=quick`, about 5 min | `outputs/full/model_fit.rds` |

By default the scripts run expensive steps in quick mode (results in
`outputs/quick/`, for checking that the code works only) and build all reported
figures and tables from the archived full outputs in `outputs/full/`. Run with
`RUN_MODE=full` to regenerate the full outputs.

## 8. License

TODO(author): e.g. Code under the MIT License; data under CC0 1.0. (Not needed
on Dryad, which sets the license at deposit.)

## 9. Funding and permits

TODO(author): Funding sources and collection, animal care, or other permits, if
applicable. (Not needed on Dryad, which records these at deposit.)

## 10. Protocols

TODO(author): Links to protocols.io or other methods repositories, if any.
