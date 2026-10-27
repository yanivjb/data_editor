# Long computations: Bayesian models, simulations, and bioinformatics

The checklist asks that code "run to completion and yield the same results"
(`CODE-6`) and recommends depositing outputs of computationally intensive steps
"as an alternative entry point to re-running your code" (`CODE-12`). When a full
rerun takes hours to weeks, meet both by archiving **three things**:

1. **The full code**, exactly as used for the paper, with the settings, seeds, and
   environment that produced the reported results.
2. **The full outputs** of the expensive steps, which the downstream code reads in to
   regenerate every reported figure, table, and number.
3. **A quick mode** that runs the expensive steps at reduced scale, so a reader or
   data editor can confirm the code works end to end in minutes.

## Run modes

Put a single switch at the top of the entry script (or in a config file) and
document it in the README:

| Mode | Expensive steps | Figures, tables, reported numbers | Typical time |
|------|-----------------|-----------------------------------|--------------|
| `quick` (default) | Rerun at reduced scale, written to `outputs/quick/` | Built from the archived full outputs in `outputs/full/` | Minutes |
| `full` | Rerun at publication scale, overwriting `outputs/full/` | Built from the new full outputs | As in the paper |

Rules that keep this honest:

- **Quick outputs never feed reported results.** Write them to a separate folder,
  label them as a smoke test in file names or plots, and never let them overwrite
  the full outputs.
- **Archived full outputs are the ones behind the paper.** Do not regenerate them
  with different settings before depositing. If they are regenerated, rebuild every
  reported number from the new ones.
- **Settings for both modes are in code**, not edited by hand between runs. The
  full settings are the default values in the code; quick mode scales them down.
- **Aim for quick mode to finish in about 10–30 minutes on a laptop.** If even a
  reduced run needs a cluster, say so and make the downstream step runnable from
  the archived outputs alone.
- **Include a check step.** When the downstream code reads the full outputs, have
  it compare the regenerated key numbers with a saved table of reported values
  (e.g. `outputs/full/reported_values.csv`) and report any difference.
- **README section "Computational cost"**: for each expensive step, give run time,
  hardware (cores, RAM, GPU, cluster), how to run quick and full modes, and which
  archived files it produces.

A minimal R pattern:

```r
run_mode <- Sys.getenv("RUN_MODE", "quick")  # "quick" or "full"; see README
stopifnot(run_mode %in% c("quick", "full"))

fit_settings <- if (run_mode == "full") {
  list(chains = 4, iter = 4000, warmup = 2000)
} else {
  list(chains = 2, iter = 500, warmup = 250)
}
fit_dir <- file.path("outputs", run_mode)

# Expensive step: always runs at the chosen scale.
fit <- do.call(fit_model, c(list(data = seed_data, seed = 42), fit_settings))
saveRDS(fit, file.path(fit_dir, "viability_fit.rds"))

# Reported results (Table 2, Figure 3) always come from the archived full fit.
fit_full <- readRDS("outputs/full/viability_fit.rds")
```

Run with `RUN_MODE=full Rscript code/02_model.R` to reproduce the paper's fit.
Python equivalent: `os.environ.get("RUN_MODE", "quick")` or a `--full` flag.

## Bayesian models (Stan, brms, JAGS, NIMBLE, PyMC)

- **Archive the fitted object or the posterior draws** (`outputs/full/*.rds`, or a
  draws CSV/Parquet for language-neutral reuse). With brms, the `file =` argument
  already caches a fit; note that brms refits when the model or data change, which
  is the behaviour you want.
- **Record the sampler setup**: chains, iterations, warmup, thinning, adapt_delta,
  max_treedepth, seed, backend (rstan or cmdstanr), and the Stan/CmdStan version.
- **Exact reproduction is not guaranteed.** Even with a seed, draws can differ
  across operating systems, compilers, and Stan versions. Say so in the README, and
  have the check step compare posterior summaries within Monte Carlo error (e.g.
  within a few MCSE, or to the reported number of decimal places) rather than
  requiring identical draws.
- **Quick mode proves the code runs, not that the model converges.** Short chains
  will show poor Rhat and ESS; tell readers to ignore diagnostics from quick mode.
  Archive the diagnostics from the full fit (Rhat, ESS, divergences, treedepth
  hits, posterior predictive checks) alongside it.
- **Archive prior and posterior predictive check outputs** that are reported in the
  paper or supplement, so they can be regenerated without refitting.

## Simulations

- **Archive per-replicate raw output**, not only summaries. This mirrors `DATA-7`:
  readers should be able to recompute summaries and figures from the replicates.
- **Seed every replicate reproducibly**, e.g. `seed = base_seed + replicate_id`, or
  parallel-safe streams (`RNGkind("L'Ecuyer-CMRG")` with `parallel`,
  `future.seed = TRUE` with `future`, `numpy.random.SeedSequence(...).spawn(n)` in
  Python). Store the seed in each replicate's output row.
- **Parameter grids as data**: keep the parameter combinations in a CSV or a clearly
  defined object in code, and archive it.
- **Quick mode**: fewer replicates, a smaller grid, or shorter run length, still
  covering each code path (every model variant and scenario at least once).
- **Cluster jobs**: archive the job scripts (SLURM, PBS, etc.) and note memory,
  cores, and wall time. Keep cluster-specific paths and module loads in one config
  file or the job script, not in the analysis code.

### SLiM and other forward simulators

- **Archive the model and the driver**: the `.slim` file(s), the script that calls
  them (`slim -s SEED -d N=500 -d rep=1 model.slim`), and the parameter grid.
- **Seed every run explicitly** with `slim -s` or `setSeed()` in the model. SLiM
  otherwise picks a random seed, so record it in each replicate's output (e.g.
  write `getSeed()` to the output file).
- **Record versions** of SLiM and of any downstream tools (pyslim, tskit, msprime
  for recapitation, which also needs its own seed). Results with the same seed can
  differ between SLiM versions.
- **Archive the outputs the statistics start from**: per-replicate summary tables,
  VCFs, or `.trees` files if size allows; otherwise per-replicate summaries, with
  the README saying what was not archived.
- **Quick mode** with fewer replicates, generations, or a smaller population only
  shows that the pipeline runs. Changing population size or run length changes the
  dynamics, so quick-mode output is never compared with the paper.

## Bioinformatics pipelines

- **Raw sequence data go to a sequence archive** (NCBI SRA, ENA, or DDBJ), not
  Dryad or Zenodo. Put the BioProject and run accessions in the README and in a
  sample table mapping each sample ID used in the code to its accession.
- **Use a workflow manager where possible** (Snakemake, Nextflow, or a documented
  shell script with numbered steps). Archive the workflow file, its config, and
  the sample sheet.
- **Pin the software environment**: conda/mamba `environment.yml` with versions, a
  container (Docker/Apptainer image tag or digest), or at least a table of every
  tool and version with the command-line options used.
- **Identify reference data exactly**: genome assembly name and version,
  annotation release, database versions (e.g. BLAST, Kraken, BUSCO lineage), with
  download URLs and checksums.
- **Archive the processed intermediates that start the statistics**: count
  matrices, filtered VCFs, alignments or trees, OTU/ASV tables, and similar. These
  are the entry point for the downstream analysis and should be CSV or a standard
  open format (VCF, FASTA, Newick), with checksums (`md5sum`) for large files.
- **Quick mode**: run the pipeline on a subsample (e.g. `seqtk sample -s 42` to a
  few thousand reads per sample), one chromosome or region, or two or three
  samples. Many workflow managers support this with a test config
  (`snakemake --configfile config/test.yaml`, a Nextflow `-profile test`).
- **Downstream statistics** (R or Python) should run in full from the archived
  intermediates in normal time, so reported results can always be regenerated.

## Archive size

Large outputs may exceed repository limits; check the current limits for Dryad and
Zenodo. If outputs are too large:

- archive the smallest output that still regenerates every reported result (e.g.
  thinned posterior draws, per-replicate summaries instead of full trajectories, a
  filtered VCF instead of BAM files);
- split very large outputs across linked records and list them in the README;
- for data that belong in a domain archive (sequences, images), deposit there and
  give accessions.

State in the README which steps cannot be rerun from the archive alone and why.
