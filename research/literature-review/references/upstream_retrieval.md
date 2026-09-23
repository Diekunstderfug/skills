# Paper Lookup Retrieval Utilities

Keep `paper-lookup` as a separately maintained local skill. Its SKILL.md metadata
records the upstream source, base commit and selective-merge policy. Read that
skill and its provider reference before invoking a utility. Do not copy its code
into the custom literature-review API implementation; use the installed helper.
Resolve the paper-lookup skill directory from the active skill catalogue, rather
than hard-coding one client's installation path.

## Available capabilities

`paper-lookup/scripts/paginate.py` supports bioRxiv, medRxiv, Europe PMC, OpenAlex
and Crossref. Run `--list-apis` for supported query formats and `--dry-run` before
retrieval. PubMed is not covered by this helper; use the direct Entrez workflow.

The helper handles provider-specific pagination, serialized pacing and count
reconciliation. Defaults cap the total export at 1,000 records and each invocation
at 50 HTTP attempts, including retries. Choose bounds appropriate to the authorized
task and inspect `reconciliation.complete` and
`stopped_at_limit`; exit success alone does not mean the export is complete. If
an endpoint reports no total, `complete` is null and status is `unverified`.
Unexplained count shortfalls exit 4.

Use `--output` to retain the JSON envelope with query, provider records, redacted
request URLs and reconciliation. Keep that envelope before normalizing records
for `search_databases.py`; the processor expects a record array, not the envelope.
The envelope includes timestamps, status, request history and events, but is not
an archive of every original HTTP response. Preserve the exit status and stderr
alongside it when recording a research search.

Execute and report sources separately. Distinguish successful zero hits from an
HTTP failure or partial retrieval. The helper writes atomic checkpoints after
pages and on failure. `--resume FILE` restores records, buffered page remainder
and the next cursor. Without `--output`, a timestamped JSON file is created in
the working directory. `--max-records` is a total export bound; `--max-calls` is
a new request budget for each invocation. Transient failures get bounded retries
with backoff and Retry-After; saved cooldowns also apply to resumed runs. Duplicate
IDs, persistently malformed responses, changing totals and unexplained shortfalls
remain explicit failures. Expired Crossref cursors require a fresh retrieval.

The upstream `search_databases.py`, already present locally, offers DOI-based and
fallback title-based deduplication. It is not full DOI/PMID canonicalization, merged
source-provenance handling, or preprint-to-publication relationship resolution.

## Source coverage record

For every relevant source record: provider, query, execution date, status, total
hits if available, retrieved count, limits, errors and result/log paths. Use statuses
such as complete, zero_hits, partial, failed, unavailable or not_attempted with a
reason. A successful zero-hit source remains in the report. Search as many relevant
sources as practicable, rather than stopping once a few providers yield papers.

## Follow-up policy

Maintain paper-lookup locally and selectively merge reviewed upstream changes.
Record the upstream reference in its SKILL.md metadata; keep capability gaps
explicit until the corresponding implementation is verified. Single-provider
checkpoint/resume is available; cross-provider incremental updates and Zotero
import reconciliation are not supplied by these helpers. Existing custom APIs
remain available.

Skillshare distributes the local source. Do not reinstall paper-lookup directly
from upstream with `skillshare update paper-lookup -g`. Follow the user's requested
synchronization scope; a source edit does not require global synchronization.
The custom literature-review continues selective integration.
