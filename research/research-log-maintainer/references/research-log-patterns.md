# Research Documentation Patterns

Use only the pattern needed for the update. Paths below illustrate responsibilities, not mandatory filenames or a requirement to split a small note.

## Current conclusions

A synthesis note such as `docs/INSIGHTS.md` answers what the evidence currently supports:

- Current conclusion and the minimal quantitative anchor needed to interpret it.
- Evidence pointer to the dated run record or maintained result.
- Interpretation boundary, relevant uncertainty, and any next analysis that could change the conclusion.

Keep long metric tables, tested alternatives, script inventories, and superseded runs in the evidence/history record. When cleaning a legacy log, move needed historical detail once, avoid duplication, and update relative links. A negative finding should say what is unsupported, for which scope and threshold, and what would justify reconsidering it.

## Reproducibility history

A history note such as `docs/CHANGELOG.md` records substantive dated changes and the evidence needed to audit them. Include the affected method, input/configuration contract, actual execution and validation status, key aggregate results, and canonical output paths as relevant.

For example, a changed filter needs its exact definition, affected analysis scope, and whether dependent outputs were actually rerun. A code change with old outputs remains a pending rerun, not a new scientific result. Repeating an unchanged run does not require another entry unless it supplies important new validation evidence.

Keep history newest-first where that matches the existing convention; preserve prior evidence and correct factual errors. Update current conclusions separately when interpretation changes.

## Decisions and methods

Use an existing decision or method note under `docs/` when the reasoning is useful beyond the immediate task. A compact record may contain:

- Question/context and the choice made.
- Evidence, alternatives, and the reason the choice matters.
- Consequences, limitations, and conditions for revisiting it.
- Links to reusable assets or validation evidence that actually exist.

Omit empty elements. Revise the same evolving decision rather than creating a new document or entry for every conversation. Detailed methods and literature synthesis can use descriptive paths such as `docs/methods/endpoint-definition.md`.

## Research orientation and navigation

Root README is the human entry; agent instructions provide enough orientation to start safely without prior conversation. The core skill defines what to retain in that overview. For an agent-facing link, explain its relevance: "When changing endpoint definitions, read `docs/methods/endpoints.md`." Use actual verified paths and resolve them relative to the containing file.

Do not invent research context from repository names. If the methods or stage cannot be verified, make the uncertainty visible instead of converting a remembered plan into a completed analysis. Keep detailed status in its canonical record, with only decision-relevant status in the entry document.

## Design references

Consult these when revising the skill itself, not during each research-log update:

- [Agent Skills authoring practices](https://agentskills.io/skill-creation/best-practices): focused instructions and conditional reference loading.
- [OpenAI skill guidance](https://learn.chatgpt.com/docs/build-skills): explicit scope, inputs/outputs, and trigger checks.
- [Codex memories](https://learn.chatgpt.com/docs/customization/memories): memory supplements durable project guidance.
