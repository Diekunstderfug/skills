# Data Rules for Research Analysis Projects

Read when establishing or changing a research project’s data-access, input-source, or human-review workflow. These are working defaults to adapt to the actual project, not a recurring full audit.

## Basic data rules

These defaults are self-contained. Apply them to the actual data and task; the project's `AGENTS.md` supplies specific access boundaries, input locations, and correction rules.

- Preserve original data and human-maintained annotations. Write transformations to derived outputs unless an edit is explicitly authorized; do not overwrite human corrections by regenerating files.
- Use declared current inputs and preserve their provenance. Do not guess authority from timestamps, silently substitute older data, or change validation records to conceal a mismatch.
- Separate permission to compute locally from permission to expose data. Authorized programs may process necessary records locally; private individual-level records, identifying clinical associations, and sensitive free text must stay out of agent context, logs, Git, and external services. Authorized local detail files may be produced for the user without echoing their contents.
- For exploration of sensitive data, limit reads to the needed sheets and fields and return permitted metadata or non-identifying summaries. This does not prohibit authorized full local computation. Do not impose patient-data preview restrictions on genuinely non-sensitive data merely because it is called raw.
- Judge disclosure by content, not file labels. Cleaned data, review files, audits, temporary files, backups, identifying row names, and deduplicated text can still expose individuals. Public availability alone is not evidence that personal records are safe to disclose.
- Apply the same boundary to normal output and errors. Use aggregate diagnostics and paths rather than record dumps; keep private data and secrets out of tracked or externally shared artifacts.

## Adapt data rules to the project

Read the applicable `AGENTS.md` and linked detail only as needed. Keep essential project-specific boundaries directly in the agent entry even when they repeat these short defaults; maintain detailed procedures in one place.

Assess fit only when the data or task makes it relevant: restrictions may be too strict if they block permitted local computation or safe summaries, and too loose if sensitive records can leak through derived files or outputs. Raise concrete mismatches with a brief reason and a narrow adjustment. Continue allowed work; do not silently relax explicit restrictions or invent broad prohibitions. Clarify only a material unresolved boundary before the affected action. No recurring compliance report or full reassessment is required for an unchanged boundary.

For source spreadsheets with ambiguous or repaired labels, read [tabular-input-contract.md](tabular-input-contract.md). Other formats should follow their declared schema.
