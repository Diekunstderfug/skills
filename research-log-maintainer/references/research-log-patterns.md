# Research Log Patterns

## Durable Insight Pattern

Use this when an analysis changes how future work should be interpreted.

Each bioinformatics or research analysis subproject needs its own `INSIGHTS.md` and `CHANGELOG.md`. Put local conclusions, thresholds, caveats, and negative results in `INSIGHTS.md` first, and record reproducibility-relevant scope or workflow changes in the local `CHANGELOG.md`. Use root `INSIGHTS.md` only for conclusions that should guide more than one subproject.

`INSIGHTS.md` is a current synthesis, not a dated experiment ledger. Retain only
stable conclusions, important methodological principles, interpretation boundaries,
and concise next analyses. Put detailed thresholds, metrics, tested alternatives,
negative/superseded runs, scripts, output paths, and reusable assets in
`CHANGELOG.md`.

```markdown
## Topic Name

- Current conclusion: ...
- Evidence: ...
- Interpretation boundary: ...
- Recommended next step: ...
```

Keep `Evidence` to one short anchor when it is essential. Link to the relevant
`CHANGELOG.md` entry for the full quantitative comparison.

Good uses:
- A DE result shows weak or absent transcriptome separation.
- A module is better interpreted as a downstream phenotype than a causal repair module.
- A classifier works as a ranking signal but fails calibration.
- A label is missing or incomplete and must be regenerated before analysis.

Do not use it for:
- one section per run or per date;
- model-size ladders and full metric tables;
- script/output inventories;
- reusable asset catalogs;
- superseded candidates whose only value is audit history.

## Negative Result Pattern

Negative results are useful when they narrow the research path.

```markdown
- Current result does not support ...
- Evidence: ...
- This should not be interpreted as ...
- Follow-up needed to revisit this conclusion: ...
```

Avoid writing only "no significant results." Include the threshold, sample scope, and why the result changes the next decision.

## Changelog Pattern

Use `CHANGELOG.md` for reproducible project-state changes and the dated experimental
evidence needed to audit them.

```markdown
## Unreleased

- Changed expression filter to `counts > 10` in at least 30% of selected samples and reran edgeR/DESeq2 outputs.
- Added domain-vs-non-domain classification audit derived from BRCA functional region coordinates.
- Compared frozen 80/110/150-gene panels across the predefined endpoints; record
  the complete metric deltas, negative results, scripts, and canonical output paths.
```

Write what changed, what was tested, the quantitative result, and why it affects
future reruns. Keep only the durable scientific or methodological interpretation in
`INSIGHTS.md`.

## Research Note Pattern

Use `RESEARCH_NOTE.md` or `RESEARCH_NOTES.md` when the reasoning is too detailed for `INSIGHTS.md`.

```markdown
## YYYY-MM-DD - Short Topic

Question:
...

Current evidence:
...

Decision:
...

Open caveats:
...
```

Use this for multi-step synthesis, competing interpretations, and handoff notes across sessions.

## README Pattern

Use `README.md` for navigation and rerun contracts:
- analysis scope
- input file paths
- script entry points
- output directories
- current status of the latest run

Do not put long biological arguments in README.
