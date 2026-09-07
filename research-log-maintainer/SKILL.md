---
name: research-log-maintainer
description: Use when finishing or reviewing bioinformatics or research work that produced durable conclusions, decisions, pitfalls, reusable principles, reusable scripts or contracts, validation gates, or reproducibility-relevant changes.
---

# Research Log Maintainer

Promote useful conclusions and assets from chat or terminal output into durable project notes.
Do not turn the logs into a command transcript.

## Workflow

1. Identify the target log files before editing.
   - Read the project-level `AGENTS.md` or equivalent first and derive the allowed root-document set from its documentation contract.
   - Prefer existing `INSIGHTS.md`, `CHANGELOG.md`, `DECISION_LOG.md`, and `README.md` for their defined project-record roles.
   - Every bioinformatics or research analysis subproject must have its own `INSIGHTS.md` and `CHANGELOG.md`. Create either file when it is missing before writing root-level summaries.
   - For subprojects, update the subproject-local `INSIGHTS.md` and `CHANGELOG.md` first, then the root project summary if the finding changes the project-level interpretation.
   - Treat root `INSIGHTS.md` as a cross-subproject synthesis surface, not a replacement for subproject-local conclusions.
   - Use root `DECISION_LOG.md` for cross-task decisions, reusable failure modes, and assets. Do not create one in every subproject unless local instructions require it.
   - If `DECISION_LOG.md` is absent, create it only when the task produced a durable decision, reusable lesson, or reusable asset.
   - Put long-form research reasoning, method notes, terminology reviews, literature evidence, and report-design notes under `docs/<domain>/` or the project's existing documentation directory. Register each maintained topic document in the documentation index, normally `docs/README.md`.
   - Create a root-level `RESEARCH_NOTE.md` or `RESEARCH_NOTES.md` only when the local project contract explicitly names it as a root document. Otherwise use a descriptive topic path under `docs/`.

2. Coordinate independent multi-log updates in parallel when useful.
   - When a single task needs updates to two or more independent log files, prefer lower-cost subagents working in parallel with one agent assigned to each file.
   - Typical file ownership is: `INSIGHTS.md` for scientific conclusions, `CHANGELOG.md` for reproducibility changes, and `DECISION_LOG.md` for durable decisions and reusable assets.
   - The main agent must first provide every writer one shared context package: task scope, sample/data conventions, verified facts, conclusions permitted for writing, file responsibilities, prohibited content, and canonical asset paths. Subagents must not independently expand the investigation.
   - The main agent must define the update boundaries, integrate the results, remove duplication, and finally recheck facts, cross-log consistency, and the existence of every recorded path.
   - Never let multiple agents edit the same file in parallel.
   - Do not parallelize merely for form: use a single writer for a small update or when only one log file needs changes.
   - Patient-data safeguards still apply during parallel work: only aggregate information may be recorded; never expose patient-level data or identifiers.

3. Separate file responsibilities.
   - `INSIGHTS.md`: only the current stable research conclusions, durable
     methodological principles, interpretation boundaries, and the few caveats or
     next analyses needed to apply those conclusions correctly.
   - `CHANGELOG.md`: all dated experiment/run history, tested alternatives,
     quantitative result details, negative or superseded routes, data contracts,
     scripts, model definitions, analysis scope, output structure, reusable asset
     paths, and rerun status.
   - When publication-compatible presentation collapses or relabels cleaned categories, record the source, exact display mapping, affected outputs, and that the cleaned-data categories remain intact. Treat a true cleaned-data recode as a separate data-contract change.
   - Do not use `INSIGHTS.md` as a chronological evidence ledger. Do not put dated
     run-by-run sections, long metric tables, script inventories, output manifests,
     or reusable-asset catalogs there. Move those details to `CHANGELOG.md`.
   - A metric may remain in `INSIGHTS.md` only when one compact anchor is necessary
     to define or bound a durable conclusion. Put the full comparison in
     `CHANGELOG.md` and link to it instead of duplicating it.
   - `DECISION_LOG.md`: lightweight ADR records explaining the task context, decision, consequences, lessons, and reusable assets.
   - `docs/<domain>/<topic>.md` or the project-specified equivalent: dated narrative notes for work-in-progress reasoning, decision history, method review, and evidence synthesis that is longer than `INSIGHTS.md`.
   - `README.md`: current entry points, input/output locations, how to rerun, and high-level scope.
   - Root Markdown is the project interface. Keep it limited to the files named by the local contract; topic notes belong behind the documentation index.

   Required subproject minimum:
   - `INSIGHTS.md` records current scientific conclusions, interpretation boundaries, and next analyses.
   - `CHANGELOG.md` records reproducibility-relevant changes to scripts, data contracts, analysis scope, outputs, or decisions that change rerun behavior.

4. Write evidence-backed conclusions, not command logs.
   - In `CHANGELOG.md`, include sample counts, tested feature counts, thresholds,
     model formulae, key metrics, and output paths needed to reproduce or audit the
     run.
   - In `INSIGHTS.md`, compress that evidence into the minimum statement needed to
     support the stable conclusion; omit operational paths and run inventories.
   - State whether evidence is strong, weak, negative, exploratory, method-sensitive, or blocked by missing data.
   - Record missingness and classification coverage when downstream interpretation depends on labels.

5. Preserve interpretation boundaries.
   - Distinguish biology from technical/data-contract limitations.
   - Do not overstate exploratory DE, enrichment, classifier, or module results.
   - Make negative results useful: say what the analysis does not support and what follow-up would be needed to overturn it.

6. Automatically summarize reusable assets before finishing every applicable task.
   - Review the full task, not only the last command or file changed.
   - Extract only assets that exist on disk or stable principles supported by the work.
   - Check these categories:
     - reusable principles and failure modes;
     - runnable entry scripts, functions, and analysis modules;
     - machine-readable contracts, configs, manifests, and frozen feature definitions;
     - validation gates, tests, QA tables, leakage audits, and resource-budget audits;
     - canonical frozen outputs, templates, or reports, including important usage caveats.
   - Record project-relative paths whenever possible. Prefer one canonical path over a list of transient intermediates.
   - Never include raw patient-level data, identifiers, secrets, temporary files, cache internals, or invalidated results.
   - If no reusable asset was created or changed, do not add an empty `Reusable assets` section.

7. Write or update a lightweight decision record when warranted.
   - Use newest-first order.
   - Prefer this shape and omit empty sections:

     ```markdown
     ## YYYY-MM-DD — Decision title

     ### Task
     ### Context
     ### Decision
     ### Consequences
     ### Lessons
     ### Reusable assets
     ```

   - Keep each section concise, normally 1–5 bullets.
   - Link or point to `INSIGHTS.md` and `CHANGELOG.md` rather than duplicating long scientific conclusions or release details.
   - Update an existing entry when the same decision evolves; add a new entry only for a distinct decision boundary.

8. Keep edits small and current.
   - Add concise entries near the top or in the most relevant existing section.
   - Keep `INSIGHTS.md` synthesis-oriented rather than append-only. When new evidence
     changes the current stance, update or replace the relevant conclusion instead
     of adding another dated section.
   - Keep `CHANGELOG.md` newest-first and append-only except for factual corrections.
   - When cleaning an oversized legacy `INSIGHTS.md`, move dated experimental detail
     to `CHANGELOG.md`; if the same facts are already present there, remove the
     duplicate from `INSIGHTS.md` without copying it again.
   - Do not paste raw sample-level rows or raw matrices into logs. Use aggregate counts, dimensions, and file paths.

## Completion check

Before reporting a research task complete:

1. Decide whether `INSIGHTS.md` needs a scientific conclusion update.
2. Decide whether `CHANGELOG.md` needs a reproducibility update.
3. Summarize reusable principles and assets into `DECISION_LOG.md` when warranted.
4. Verify every recorded asset path exists and every caveat still matches the current result.
5. Confirm no invalid, superseded, temporary, or patient-level artifact was promoted.
6. Confirm every new or updated topic note is in the permitted documentation directory, is reachable from its index, and did not expand the root Markdown surface outside the local contract.

## Style

- 默认使用中文撰写项目日志；代码符号、文件名、字段名、模型名和无可靠中文译名的
  专业术语保留英文。
- 如果项目已有明确语言规范，则服从项目规范；中英混排时保持同一术语前后一致。
- Use direct research language: conclusion first, evidence second, caveat third.
- Prefer bullets for reusable facts and short paragraphs for interpretation.
- Use exact thresholds and dates when the conclusion depends on them.
- Use terms like `exploratory`, `method-sensitive`, `negative evidence`, and `interpretation boundary` when appropriate.
- Describe why a decision was made and what can be reused; do not narrate every command.

## Reference

Read `references/research-log-patterns.md` when choosing how to structure a larger update or when adapting patterns from BRCAness-style projects.
