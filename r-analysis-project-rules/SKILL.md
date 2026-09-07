---
name: r-analysis-project-rules
description: Use when creating, editing, migrating, or reviewing R scripts in analysis repos that use myutils path helpers, project-relative outputs, cohort/sample metadata, result registries, reporting folders, or Rscript-based validation.
---

# R Analysis Project Rules

## Overview

Use these rules for R analysis projects, not R package development. Match the local script contract: project-safe paths, reusable helpers, explicit outputs, and lightweight validation before claiming a result changed.

This skill is especially relevant in repos like `rna_tools`, where most scripts use `myutils`, `ensure_wd()`, `wd_path()`, `ws_path()`, `data.table`, `src/_*.R` helpers, and `Rscript` smoke checks.

## Start From Nearby Scripts

Before editing, inspect 2-3 scripts in the same lane:

- evaluation: `scripts/30_evaluate/...`
- reporting: `scripts/reporting/...` or `scripts/40_report/...`
- shared logic: `src/_*.R`
- own-model assets: `ours_model/...`
- published-model wrappers: `published_models/...`

Preserve the lane's output schema and naming unless the task explicitly changes the contract.

## Raw Data Inspection Boundary

Treat raw datasets as execution-only inputs:

- Do not open, preview, sample, or print raw records with shell readers, spreadsheet previews, `head()`, `tail()`, row sampling, or equivalent inspection.
- Allow only filenames, dimensions, row names, column names, and aggregate metrics that do not reveal individual records.
- Let analysis scripts load raw data locally for computation, while keeping console output, tool output, chat, and project logs limited to the permitted metadata and aggregates.
- Keep row names or aggregate groups that contain patient or sample identifiers out of chat and durable logs.
- Diagnose data problems with schema checks, counts, missingness rates, range summaries, and aggregate validation flags instead of record-level output.

## Exact Raw-Label Resolution

- Match source columns against the worksheet's original labels exactly; preserve unrepaired labels when reading the schema.
- Treat importer-generated suffixes such as `...372` as positional repair metadata, never as clinical meaning or a field contract.
- When original labels repeat, disambiguate them only inside semantic blocks whose boundaries are themselves anchored by exact, unique original labels.
- Resolve every contracted field to exactly one column. Stop with the standard name, expected label, semantic block, and match count when resolution returns zero or multiple columns.
- Column order may remain in a schema audit for traceability, but it must not select or define analysis fields.

## Script Header Contract

For standalone executable scripts, default to:

```r
rm(list = ls())

library(myutils)
library(data.table)

ensure_wd(workdir = "project_name")
source(wd_path("src", "_helper.R"))

cat("=== short step label ===\n")

out_dir <- wd_path("results")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
```

Local variations are allowed, but do not introduce `setwd()` or absolute paths when `myutils` is already the project convention.

Shared `src/_*.R` helper files usually do not call `ensure_wd()` themselves; they assume the caller has initialized the working directory.

## Standalone Module Contract

Treat every numbered analysis script as an independently executable module in both interactive and script-based use:

- It must start successfully both with `source("path/to/script.R")` in a fresh interactive R session and with `Rscript path/to/script.R`.
- It must initialize paths, load its own packages, declare its inputs and outputs, and create its output directories.
- It must not depend on objects already present in an interactive session or require a human to run or `source()` another entry script first.
- Its only code-level dependency may be shared functions that it explicitly `source()` from `src/`; helpers are not entry scripts and should not perform hidden analysis work on load.
- When a required input is absent or invalid, stop with an actionable error.
- Keep orchestration scripts optional. An orchestrator may call modules, but each module must remain directly runnable and testable.

## Path Rules

| Need | Use |
| --- | --- |
| Current project file | `wd_path("subdir", "file.csv")` |
| Sibling project or shared workspace file | `ws_path("sibling_project", "file.csv")` |
| File under an already-created output directory | `file.path(out_dir, "file.csv")` |

Rules:

- Never hard-code `/root/...` inside reusable scripts.
- Prefer defining `out_dir` once, then write all outputs under it.
- Use `dir.create(..., recursive = TRUE, showWarnings = FALSE)` before writing.
- When using `ws_path("..", ...)`, leave a comment if the extra parent hop is intentional.
- Re-check sibling paths and column names live; old object names often drift.

## Reuse Helpers Before Inlining

Prefer existing project helpers over copy-paste. When logic is genuinely reused by more than one entry script, place the shared function in `src/` and explicitly `source()` it from each caller. Keep one-off analysis logic in its entry script; do not create `src/` preemptively.

## Clinical Tables

For clinical Table 1, clinicopathological subgroup tables, nested comparison headers, or journal-style HTML/DOCX tables, read `references/clinical-table-reporting.md` before editing. Apply its comparison contract, P-value placement, missing-data presentation, literature-template adaptation, display-only recoding, and rendered-output checks.

## Top-Level Directory Contract

Respect the project's `AGENTS.md` first, then its existing layout. For a new analysis project without a local contract, create these required top-level directories:

- `scripts/`: independently runnable analysis entry scripts.
- `data/`: project data inputs and reproducible derived data.
- `results/`: generated tables, figures, reports, and analysis outputs.

Create `src/` only after shared functions actually exist. This skill defines no other top-level directories and no required subdirectory layout. Do not introduce cohort, model, evaluation, reporting, registry, archive, or other nested structures unless the local project contract or current work requires them.

## Shell And Rscript Rules

Use `Rscript` for parse and smoke checks:

```bash
Rscript -e 'parse(file="scripts/path/to_script.R")'
Rscript scripts/path/to_script.R
```

When inline R code references `$column`, wrap the whole `Rscript -e` expression in single quotes. Double quotes let the shell expand `$column` and corrupt the R code.

For parse sweeps, use a simple R regex:

```bash
Rscript -e 'files <- list.files("scripts", pattern="[.]R$", recursive=TRUE, full.names=TRUE); invisible(lapply(files, parse))'
```

## Verification Checklist

Before claiming the edit is done:

- Parse every touched `.R` file.
- Run each touched entry script both via `source()` in a fresh R process and directly with `Rscript`. If required real inputs are unavailable, verify that both modes stop at the declared input boundary with an actionable message.
- Confirm output files exist and are non-empty when outputs are expected.
- Check sample counts, cohort labels, endpoint names, and key columns after data joins.
- If registry rows are touched, verify `source_path` exists and key fields include both stable display names and code/model IDs when the repo expects both.
- If conclusions, model status, benchmark ranking, or reporting artifacts change, update the project log/docs in the same task.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Writing absolute paths because the script is "just local" | Use `wd_path()` / `ws_path()` |
| Editing a wrapper but leaving copied old sample IDs or endpoints | Grep the old cohort/model names after edits |
| Recomputing shared metrics inline | Source the project helper and preserve metric semantics |
| Treating a copied result as a new-cohort output | Regenerate or clearly label it as reference-only |
| Using double-quoted `Rscript -e` with `$sample_id` | Use single quotes or a temporary script |
| Declaring success after parse only | Run a smoke path that loads target inputs or writes expected outputs |
