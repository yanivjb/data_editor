<!--
INSTRUCTIONS FOR THE AGENT. Do not copy this block into the README.

- This is the structure for the archive README. Sections 1-6 are required by the
  journal, in this order. Later sections are optional: include them only when
  they apply.
- Replace each <angle-bracket placeholder> with confirmed information. If a value
  is not known yet, leave that line or section out and add it to AUTHOR_TODO.md.
  The finished README must contain no placeholders, TODOs, or HTML comments.
- Write for a reader who downloads the archive. Do not mention the review, the
  checklist or its item IDs, the data editor, the agent, or how a fact was
  confirmed. Do not link to files outside the archive.
- Example rows (site, mass_g, ...) show the format only; replace them.
-->

# <Title of the paper>: data and code

## Citation

<Authors>. <Year>. <Title>. *<Journal>* <volume>:<pages>. <DOI>

<!-- Before publication, use e.g. "Manuscript in review at The American Naturalist." -->

## Authors and contact

- <Name>, <affiliation>, <email>, <ORCID>
- Corresponding author: <name>, <email>

## Study summary

<Two to five sentences: the question, the study system, and the design.>

## Responsibilities

<Who collected the data, and who wrote the code.>

## Files and variables

### Folder structure

```text
.
├── README.md
├── data/          raw data (CSV)
├── code/          analysis scripts, run in the order below
└── outputs/       figures, tables, and intermediate results written by the code
```

### Data files

#### `data/<file>.csv`

<What one row represents, how and when the data were collected, and which
analyses use the file. How it links to other files, e.g. "joins to
`plants.csv` on `plant_id`".> Missing values are coded as `NA`.

| Variable | Description | Type | Units / levels |
|----------|-------------|------|----------------|
| `site` | Sampling site | categorical | `A`, `B`, `C` |
| `mass_g` | Fresh body mass | numeric | g |

<Repeat for every data file, or point to a codebook file.>

### Restricted or modified data

<Only if some data are withheld or changed for privacy or permits: what was
withheld or changed (e.g. coordinates rounded to 0.1°), why, which results
cannot be reproduced from the shared files, and how to request the full data.>

### Code files

| File | Purpose | Reads | Writes | Manuscript output |
|------|---------|-------|--------|-------------------|
| `code/01_clean.R` | <purpose> | `data/<file>.csv` | `outputs/clean.rds` | — |
| `code/02_models.R` | <purpose> | `outputs/clean.rds` | `outputs/fig1.pdf` | Figure 1, Table 1 |

### Output files

<Intermediate and final outputs, noting which are provided so slow steps need
not be rerun.>

## Software and versions

- Operating system: <OS and version>
- <R or Python version>
- Packages: <list with versions, or "see `renv.lock`" / "see `requirements.txt`">

<Packages the scripts install themselves, if any.>

## How to reproduce the results

1. Open a terminal in this folder.
2. Install the software listed above.
3. Run the scripts in order:

   ```sh
   Rscript code/01_clean.R
   Rscript code/02_models.R
   ```

<Random seeds used; how to start from the provided intermediate outputs.>

### Computational cost

<Only if a step takes more than a few minutes.>

| Step | Full run time | Hardware | Quick mode | Archived outputs |
|------|---------------|----------|------------|------------------|
| `code/02_models.R` | about 6 h | 4 cores, 16 GB RAM | `RUN_MODE=quick`, about 5 min | `outputs/full/model_fit.rds` |

By default the scripts run expensive steps in quick mode (results in
`outputs/quick/`, for checking that the code works only) and build all reported
figures and tables from the archived full outputs in `outputs/full/`. Run with
`RUN_MODE=full` to regenerate the full outputs.

### Figures not produced entirely by code

<Only if some figures were drawn, photographed, or edited after the code made them.>

| Figure / panel | How it was made | Software | Code-made base file |
|----------------|-----------------|----------|---------------------|
| Figure 1 | Conceptual diagram, drawn by hand | Inkscape | — |
| Figure 2 | Made by `code/04_figures.R`; labels and layout edited, data unchanged | Illustrator | `outputs/fig2_base.pdf` |
| Figure 3A | Photograph of the study organism | — | — |

## License

<e.g. Code under the MIT License; data under CC0 1.0.>

## Funding and permits

<Funding sources and collection, animal care, or other permits.>

## Protocols

<Links to protocols.io or other methods repositories.>
