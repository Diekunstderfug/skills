# Selective upstream integration

## 2026-09-22 — local version 1.3.1

Reviewed upstream K-Dense-AI/scientific-agent-skills commit
`49c6e97775eaa18ba791bebe23162a70ae601c18` (literature-review 1.8).
This is a selective integration, not a full upgrade to upstream 1.8.

- Imported 31 offline result-processing tests; see tests/README.md for provenance.
- Added local guidance distinguishing the custom five-source lit_search.py,
  the separately followed paper-lookup skill, and exhaustive direct API retrieval.
- Replaced legacy gget literature-search examples with the existing local CLI
  and direct API guidance.
- Removed the pre-existing mandatory AI figure requirement in favor of useful,
  reproducible figures, consistent with the user's workflow preferences.
- Preserved all existing runtime scripts, references, templates, and research outputs.

Deferred: upstream workflow document splitting, a detailed search-query review
checklist, and independent improvements to pagination/error reporting/deduplication.
Excluded: commercial search/image dependencies and journal/author-prestige filters.

## 2026-09-22 — local version 1.3.2

Adopted upstream's three-reference document organization using the existing local
content: core_workflow.md, search_and_citation.md, and example_workflow.md.
The main skill retains routing limitations, figure policy, essential methodological
rules, resources, dependencies, and explicit instructions on when to read each guide.
Corrected legacy script paths and the remaining gget literature-search example.
Replaced the obsolete integration catalogue (including internal-comms/branding)
with relevant academic skill routing. Runtime scripts and test bodies are unchanged.
This reorganization does not implement the deferred detailed query audit or API fixes.

## 2026-09-22 — local version 1.3.3

Added a locally authored search audit and reusable record template covering controlled
vocabulary, free text, syntax, independent seed checks, and retrieval completeness.
Linked it from the entry point and both workflow/search guides. This is a methodology
extension, not an upstream import or a completed live topic search. Runtime unchanged.

## 2026-09-22 — local version 1.3.4

Preserved broad multi-database searching, including zero-hit source reporting.
Routed supported retrieval to the separately followed upstream paper-lookup
paginator; documented actual limits and unsupported resume/incremental/Zotero
features. Further runtime improvements should follow upstream when available.

## 2026-09-22 — local version 1.3.5

Added routing to the independently authored systematic-search-strategy skill.
It uses the seven steps selectively, gives concise ordinary MeSH/query responses,
and preserves broad multi-source retrieval with a persistent progress/gap log.
Formal review verification/reporting expands only when called for. Runtime unchanged.
