# Search Strategy Audit

Use this checklist before a systematic search and after substantive query changes.
Store the completed [audit template](../assets/search_audit_template.md) with the
research project. This is a local operational checklist, not a claim of formal
independent peer review or a guarantee that all relevant literature was found.

## 1. Scope and concept blocks

Define population, condition, interventions/exposures and eligible study designs.
Distinguish screening criteria from concepts that must appear in the query. Avoid
requiring every PICO element when outcomes or comparators are poorly reported.
Build OR groups for synonyms and AND only the necessary concept groups. Explain
any NOT exclusions and inspect what they remove. Never use prestige, citation
counts, or PDF availability as eligibility filters.

## 2. Controlled vocabulary and free text

Verify candidate MeSH descriptors in the current NLM MeSH Browser; record preferred
labels, identifiers and the date checked. Review narrower terms, entry terms and
whether explosion is appropriate. Do not invent a MeSH heading from a clinical
phrase. Justify major-topic restrictions, subheadings and disabled explosion.

Combine controlled vocabulary with title/abstract synonyms, spelling variants,
abbreviations and older terminology. This helps cover records without applicable
MeSH indexing. Use terms found in independently identified relevant articles.

## 3. Syntax and restrictions

Check parentheses, each term's field, Boolean grouping, phrases, truncation and
dates in the target database. Inspect PubMed Search Details/query translation and
warnings, including phrases not found. Field tags, quotes and wildcards can alter
automatic term mapping; do not assume the entered string is the executed strategy.
Check saved interface filters as well as explicit query filters.

Run concept blocks separately and combined; record counts and unexpected zeroes
or abrupt reductions. Review age, sex, species, language and study-type restrictions
for avoidable exclusions, especially for records lacking indexing. Translate the
strategy separately for every database; PubMed syntax is not portable unchanged.

## 4. Known-paper retrieval check

Before tuning the query, assemble an independent seed set from user-provided
papers, prior reviews, citation chasing or domain knowledge. Include varied years,
terminology and relevant subgroups. Record DOI/PMID, eligibility rationale and how
each paper was found. If possible, keep some seeds aside for final validation.

For each database, establish which seeds are indexed and inside the protocol's
scope. Check whether the topic query retrieves each seed, using identifier
membership in the result set or an identifier intersection with the topic query.
A direct DOI/title lookup alone does not demonstrate topic-query retrieval.

For every miss, identify the reason: not indexed, out of scope, vocabulary gap,
over-restrictive concept/filter, syntax issue, or incomplete download. Revise
scientifically justified terms, rerun all seed checks, and retain query versions.
Do not insert individual paper titles merely to make the check pass.

Report the fraction of eligible, indexed seeds retrieved with numerator and
denominator. Label this **seed-set retrieval**, not overall recall. A 100% seed
result does not establish exhaustive coverage. If no independent seeds exist,
mark this check unassessed rather than passed.

## 5. Retrieval and supplementary coverage

Separately reconcile database hit counts with downloaded unique identifiers for
the recorded query/snapshot. Log pagination, provider caps, errors, retries and any
unretrieved records. A successful first-page response is not a complete export.
If limits require partitioning, record partitions and deduplicate their overlaps.
Document changes in a live database that prevent exact count reconciliation.

Use complementary sources and backward/forward citation chasing appropriate to
the review. Screen newly discovered candidates and examine whether misses expose
query gaps. Preserve provider provenance and preprint/publication relationships.
Report remaining access, indexing, language and search-date limitations explicitly.

## 6. Decision and evidence

Save exact per-database queries, dates, translated queries/warnings, counts, seed
results and unresolved issues. Status is ready, revise, or blocked, with reasons.
Do not report checks as complete unless actually executed. Formal independent
search peer review should name the reviewer and method; an AI self-check is not
independent review. Repeat affected checks after changes and before final export.

## Application to very early-onset breast cancer

Treat age <=35 as an eligibility definition to verify in study populations or
reported subgroups. Do not assume an age filter, "young adult", "early onset", or
"very early onset" precisely encodes that threshold. Broad age terminology may
be useful for retrieval, followed by explicit age screening.

Keep the general early-onset breast cancer search independent of a mandatory BRCA
block when both hereditary and non-hereditary disease are eligible. Run a separate
BRCA-focused branch for the genetic subtopic and preserve its provenance. Check
mixed-age cohorts and relevant subgroup reports during screening. These are design
considerations, not a validated query or evidence that the topic has been searched.

## Methodological references

- [NLM PubMed User Guide](https://pubmed.ncbi.nlm.nih.gov/help/): query syntax,
  mapping, fields and filters. Checked 2026-09-22.
- [NLM MeSH Browser](https://meshb.nlm.nih.gov/search): verify current descriptors.
- [Cochrane Handbook, Chapter 4](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04): search design and study identification. Checked 2026-09-22.
