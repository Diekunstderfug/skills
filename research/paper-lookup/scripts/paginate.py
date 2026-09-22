#!/usr/bin/env python3
"""Bounded, rate-limited, count-reconciling pagination for this skill's APIs.

The five supported APIs paginate differently -- absolute record offsets,
opaque cursors, continuation tokens, 1-based pages -- and each reports totals its
own way. Re-deriving the walk per query is how records get silently dropped. The
worst case is bioRxiv: `cursor` is an absolute offset, `/details/` returns 30 per
page but `/pubs/` returns 100, and an out-of-step cursor returns **HTTP 200**, so
stepping by 100 skips records 30-99 of every hundred and looks successful.

Every walk here:

- steps by the page size the response actually reported, never an assumed one
- stops on this API's real terminator (Europe PMC echoes your cursor back rather
  than sending null; bioRxiv just returns an empty collection)
- reconciles retrieved against the expected total and **exits 4 on a shortfall**
- refuses to exceed --max-records / --max-calls, and says so rather than
  truncating quietly

    python3 paginate.py --api biorxiv --query 2024-01-01/2024-01-03
    python3 paginate.py --api europepmc --query 'SRC:"PPR" AND "organoid"' --max-records 200
    python3 paginate.py --api openalex --query 'filter=publication_year:2024' --dry-run

Needs network access. No credentials required for bioRxiv, medRxiv, Europe PMC,
Crossref, or OpenAlex; NCBI_API_KEY and S2_API_KEY raise limits where relevant.
"""

from __future__ import annotations

import argparse
import http.client
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import Reconciliation, emit, fail, redact_url  # noqa: E402
from _pagination_state import Progress  # noqa: E402

USER_AGENT = "paper-lookup-skill/2.2.1 (+https://github.com/Diekunstderfug/skills)"
DEFAULT_MAX_RECORDS = 1000
DEFAULT_MAX_CALLS = 50
REQUEST_TIMEOUT = 60


@dataclass
class Page:
    """One response, normalized."""

    records: list[Any]
    total: int | None = None
    #: The next cursor/token/offset, or None when this API says it is done.
    next_state: Any = None
    #: Anything the caller must be told that is not a record.
    notes: list[str] | None = None


@dataclass
class Api:
    name: str
    #: Seconds to wait between requests. Serialized: never parallelize one host.
    delay: float
    build_url: Callable[[str, Any, int], str]
    parse: Callable[[Any, Any], Page]
    initial_state: Any = 0
    note: str = ""


class FetchError(RuntimeError):
    def __init__(self, message: str, *, retryable: bool = False, retry_after: float | None = None):
        super().__init__(message)
        self.retryable = retryable
        self.retry_after = retry_after


class PaginationShortfall(RuntimeError):
    """An empty terminator arrived before the advertised records were retrieved."""


@dataclass
class Fetched:
    payload: Any
    delay: float = 0.0


def retry_seconds(value: str | None) -> float | None:
    if not value:
        return None
    try:
        seconds = float(value)
    except ValueError:
        try:
            date = parsedate_to_datetime(value)
            seconds = date.replace(tzinfo=date.tzinfo or timezone.utc).timestamp() - time.time()
        except (TypeError, ValueError, OverflowError):
            return None
    return max(0.0, seconds) if math.isfinite(seconds) else None


def fetch(url: str, *, headers: dict[str, str] | None = None) -> Fetched:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            body = response.read().decode("utf-8", errors="replace")
            try:
                interval = float(response.headers.get("x-rate-limit-interval", "0").removesuffix("s"))
                limit = float(response.headers.get("x-rate-limit-limit", "1"))
                delay = interval / limit * 1.05 if limit > 0 else 0.0
                if not math.isfinite(delay) or delay < 0:
                    delay = 0.0
            except (ValueError, TypeError):
                delay = 0.0
    except urllib.error.HTTPError as error:
        wait = retry_seconds(error.headers.get("Retry-After") if error.headers else None)
        error.close()
        raise FetchError(f"HTTP {error.code} from {redact_url(url)}",
                         retryable=error.code in (429, 500, 502, 503, 504), retry_after=wait) from error
    except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
        raise FetchError(f"could not reach {redact_url(url)} ({type(error).__name__})",
                         retryable=True) from error
    except (http.client.HTTPException, UnicodeError, ValueError) as error:
        raise FetchError(f"invalid URL or HTTP response from {redact_url(url)} ({type(error).__name__})") from error
    try:
        return Fetched(json.loads(body), delay)
    except json.JSONDecodeError as error:
        raise FetchError(f"response from {redact_url(url)} was not JSON", retryable=True) from error


def object_response(payload: Any) -> dict:
    if not isinstance(payload, dict):
        raise FetchError("API returned an invalid response object", retryable=True)
    if payload.get("error") or payload.get("errors"):
        raise RuntimeError("API returned an error or an invalid response object")
    return payload


def record_list(container: Any, key: str) -> list[dict]:
    if not isinstance(container, dict) or not isinstance(container.get(key), list):
        # Europe PMC has returned HTTP 200 with only {"version": "6.9"} for a
        # valid cursor. Retry within the same request budget; never count this
        # incomplete response as an empty page or advance the saved cursor.
        raise FetchError(f"API response is missing the {key} record list", retryable=True)
    rows = container[key]
    if not all(isinstance(row, dict) for row in rows):
        raise RuntimeError(f"API response has invalid records in {key}")
    return rows


def count_value(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, str) and value.isdigit():
        value = int(value)
    if type(value) is not int or value < 0:
        raise RuntimeError("API returned an invalid total count")
    return value


# --- bioRxiv / medRxiv ------------------------------------------------------
#
# `cursor` is an absolute record offset. The page size is 30 on /details/ and 100
# on /pubs/, and an out-of-step cursor is accepted with HTTP 200 -- so the step
# comes from the response's own `count`, never from a constant.


def _rxiv_url(server: str) -> Callable[[str, Any, int], str]:
    def build(query: str, state: Any, _limit: int) -> str:
        endpoint = "pubs" if query.startswith("pubs:") else "details"
        interval = query[5:] if query.startswith("pubs:") else query
        return f"https://api.biorxiv.org/{endpoint}/{server}/{interval}/{int(state)}/json"

    return build


def _rxiv_parse(payload: Any, state: Any) -> Page:
    payload = object_response(payload)
    messages = record_list(payload, "messages")
    if not messages:
        raise RuntimeError("bioRxiv/medRxiv response has no status message")
    message = messages[0]
    status = message.get("status")
    records = record_list(payload, "collection")
    notes: list[str] = []

    if status == "no articles found" and not records:
        # "no articles found" arrives with HTTP 200 and an empty collection, which
        # is indistinguishable from a genuine no-match unless status is read.
        notes.append(f"server status: {status!r} (HTTP 200 with an empty collection)")
        return Page(records=[], total=0, next_state=None, notes=notes)
    if status != "ok":
        raise RuntimeError("bioRxiv/medRxiv returned an unsuccessful or missing status")

    total = message.get("total")
    total = count_value(total)

    new_papers = message.get("count_new_papers")
    if new_papers is not None:
        notes.append(
            f"count_new_papers={new_papers} counts distinct first-posting preprints while "
            f"total={total} counts every version record; deduplicate by DOI to compare against "
            "count_new_papers"
        )

    reported = message.get("count")
    step = int(reported) if isinstance(reported, int) and reported > 0 else len(records)
    if not records:
        return Page(records=[], total=total, next_state=None, notes=notes)

    if step != len(records):
        notes.append(f"response reported count={step} but returned {len(records)} records")
        step = len(records)

    next_state = int(state) + step
    if total is not None and next_state >= total:
        next_state = None
    return Page(records=records, total=total, next_state=next_state, notes=notes)


# --- Europe PMC ------------------------------------------------------------
#
# cursorMark. At exhaustion it returns an empty result list and echoes back the
# cursor you sent, rather than a null -- so detecting the end costs one extra
# empty request.


def _europepmc_url(query: str, state: Any, limit: int) -> str:
    params = {
        "query": query,
        "format": "json",
        "pageSize": str(min(limit, 1000)),
        "cursorMark": str(state),
        "resultType": "lite",
    }
    return "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(params)


def _europepmc_parse(payload: Any, state: Any) -> Page:
    payload = object_response(payload)
    # Europe PMC reports errors with HTTP 200 and an errCode in the body.
    if "errCode" in payload:
        raise RuntimeError(
            f"Europe PMC errCode {payload['errCode']}: {payload.get('errMsg', 'no message')}"
        )

    total = count_value(payload.get("hitCount"))
    # Europe PMC may serialize an empty resultList as {} instead of {"result": []}.
    # A missing container is still an invalid response; counts remain reconciled.
    records = (
        [] if payload.get("resultList") == {} and total is not None
        else record_list(payload.get("resultList"), "result")
    )
    next_cursor = payload.get("nextCursorMark")
    notes: list[str] = []

    echoed = (payload.get("request") or {}).get("queryString")
    if echoed:
        notes.append(f"query as parsed by Europe PMC: {echoed!r}")

    if not records or next_cursor in (None, state):
        next_cursor = None
    return Page(
        records=records,
        total=int(total) if isinstance(total, int) else None,
        next_state=next_cursor,
        notes=notes,
    )


# --- OpenAlex --------------------------------------------------------------


def _openalex_url(query: str, state: Any, limit: int) -> str:
    # `query` is a raw parameter string, e.g. `search=crispr` or
    # `filter=publication_year:2024`, so both forms work without a second flag.
    base = "https://api.openalex.org/works?"
    params = {"per-page": str(min(limit, 100)), "cursor": str(state)}
    mail = os.environ.get("OPENALEX_EMAIL")
    if mail:
        params["mailto"] = mail
    key = os.environ.get("OPENALEX_API_KEY")
    if key:
        params["api_key"] = key
    return base + query + "&" + urllib.parse.urlencode(params)


def _openalex_parse(payload: Any, _state: Any) -> Page:
    payload = object_response(payload)
    meta = payload.get("meta")
    if not isinstance(meta, dict):
        raise FetchError("OpenAlex response is missing meta", retryable=True)
    records = record_list(payload, "results")
    notes = []
    if meta.get("cost_usd") is not None:
        notes.append(f"OpenAlex reported cost_usd={meta['cost_usd']} for this call")
    next_cursor = meta.get("next_cursor")
    if not records:
        next_cursor = None
    return Page(
        records=records,
        total=count_value(meta.get("count")),
        next_state=next_cursor,
        notes=notes,
    )


# --- Crossref --------------------------------------------------------------


def _crossref_url(query: str, state: Any, limit: int) -> str:
    params = {"rows": str(min(limit, 1000)), "cursor": str(state)}
    mail = os.environ.get("CROSSREF_MAILTO")
    if mail:
        params["mailto"] = mail
    return "https://api.crossref.org/works?" + query + "&" + urllib.parse.urlencode(params)


def _crossref_parse(payload: Any, _state: Any) -> Page:
    payload = object_response(payload)
    if payload.get("status", "ok") != "ok":
        raise RuntimeError("Crossref returned an unsuccessful status")
    message = payload.get("message")
    records = record_list(message, "items")
    next_cursor = message.get("next-cursor")
    if not records:
        next_cursor = None
    total = message.get("total-results")
    notes = ["Crossref cursors expire after 5 minutes; a long walk must keep moving"]
    return Page(
        records=records,
        total=count_value(total),
        next_state=next_cursor,
        notes=notes,
    )


APIS: dict[str, Api] = {
    "biorxiv": Api(
        name="biorxiv",
        delay=1.0,
        build_url=_rxiv_url("biorxiv"),
        parse=_rxiv_parse,
        initial_state=0,
        note=(
            "query is an interval (2024-01-01/2024-01-03), Nd, N, or a DOI. "
            "Prefix with 'pubs:' to walk /pubs/ instead of /details/."
        ),
    ),
    "medrxiv": Api(
        name="medrxiv",
        delay=1.0,
        build_url=_rxiv_url("medrxiv"),
        parse=_rxiv_parse,
        initial_state=0,
        note="same as biorxiv; always via api.biorxiv.org, never api.medrxiv.org",
    ),
    "europepmc": Api(
        name="europepmc",
        delay=0.5,
        build_url=_europepmc_url,
        parse=_europepmc_parse,
        initial_state="*",
        note="query is Europe PMC query syntax, e.g. 'SRC:\"PPR\" AND \"organoid\"'",
    ),
    "openalex": Api(
        name="openalex",
        delay=0.2,
        build_url=_openalex_url,
        parse=_openalex_parse,
        initial_state="*",
        note="query is a raw parameter string, e.g. 'search=crispr' or 'filter=publication_year:2024'",
    ),
    "crossref": Api(
        name="crossref",
        delay=1.05,
        build_url=_crossref_url,
        parse=_crossref_parse,
        initial_state="*",
        note="query is a raw parameter string, e.g. 'query.bibliographic=attention+is+all+you+need'",
    ),
}


def validate_query(api: str, query: str) -> None:
    if not isinstance(query, str) or not query.strip():
        raise RuntimeError("query must not be empty")
    if api in ("openalex", "crossref"):
        if not query.isascii() or any(c.isspace() or ord(c) < 32 for c in query):
            raise RuntimeError("raw query parameters must be URL-encoded")
        reserved = {"api_key", "apikey", "key", "email", "mailto", "tool", "cursor",
                    "page", "per_page", "per-page", "rows", "offset"}
        keys = {k.lower() for k, _ in urllib.parse.parse_qsl(query, keep_blank_values=True)}
        if keys & reserved:
            raise RuntimeError("query contains reserved paging/contact/credential parameters; use CLI options and environment variables")


def record_key(api: str, row: dict) -> tuple:
    if not isinstance(row, dict):
        raise RuntimeError("API returned a non-object record")
    if api in ("biorxiv", "medrxiv"):
        identifier = row.get("doi") or row.get("preprint_doi")
        suffix = (str(row.get("version", row.get("preprint_version", ""))),
                  str(row.get("published_doi", "")).lower())
    elif api == "europepmc":
        identifier = row.get("id")
        source = row.get("source")
        if not isinstance(source, str) or not source:
            raise RuntimeError("Europe PMC record has no source identifier")
        suffix = (source,)
    else:
        identifier = row.get("DOI") if api == "crossref" else row.get("id")
        suffix = ()
    if not isinstance(identifier, str) or not identifier.strip():
        raise RuntimeError("API record has no stable identifier")
    return (identifier.strip().lower(), *suffix)


def walk(
    api: Api,
    query: str,
    *,
    page_size: int,
    max_records: int,
    max_calls: int,
    verbose: bool,
    progress: Progress | None = None,
    destination: str | Path | None = None,
    max_retries: int = 2,
    max_retry_wait: float = 60.0,
) -> tuple[list[Any], Reconciliation, list[str]]:
    p = progress if progress is not None else Progress(api.name, query, api.initial_state)
    rec = p.reconciliation
    p.delay = max(p.delay, api.delay)
    known = {record_key(api.name, r) for r in p.records + p.buffered}
    if len(known) != len(p.records) + len(p.buffered):
        raise RuntimeError("checkpoint contains duplicate identifiers")
    calls = 0
    rec.error = None
    rec.stopped_at_limit = False
    p.status = "running"
    p.event("run", max_records=max_records, max_calls=max_calls, max_retries=max_retries)
    p.save(destination)

    def bound(reason: str) -> None:
        rec.stopped_at_limit = True
        p.event("limit", reason=reason)

    try:
        while True:
            take = max_records - len(p.records)
            p.records.extend(p.buffered[:take])
            p.buffered = p.buffered[take:]
            rec.retrieved = len(p.records)
            # The final page may be larger than the caller's remaining quota.
            # Its unexported records stay in the checkpoint even if the API ended.
            if p.exhausted and not p.buffered:
                break
            if len(p.records) >= max_records:
                bound(f"stopped at --max-records={max_records}; resume with a larger total bound")
                break
            if calls >= max_calls:
                bound(f"stopped at --max-calls={max_calls}, including retries; resume to continue")
                break
            if p.api == "crossref" and p.last_page_at is not None and time.time() - p.last_page_at >= 300:
                raise RuntimeError("Crossref cursor expired after 5 minutes; keep this partial file and start a fresh retrieval")
            wait = max(0.0, (p.retry_not_before or 0) - time.time())
            if wait > max_retry_wait:
                raise RuntimeError(f"server cooldown requires another {math.ceil(wait)} seconds; resume after that time")
            if p.urls or wait:
                time.sleep(max(p.delay, wait))
            page = None
            url = api.build_url(query, p.next_state, min(page_size, max_records - len(p.records)))
            for attempt in range(max_retries + 1):
                if calls >= max_calls:
                    bound(f"stopped at --max-calls={max_calls}, including retries; resume to continue")
                    break
                safe_url = redact_url(url)
                p.urls.append(safe_url)
                calls += 1
                if verbose:
                    sys.stderr.write(f"  request {calls}, page {rec.pages + 1}: {safe_url}\n")
                p.save(destination)
                try:
                    response = fetch(url)
                    if isinstance(response, Fetched):
                        p.delay = max(p.delay, response.delay)
                        response = response.payload
                    page = api.parse(response, p.next_state)
                    p.retry_not_before = None
                    break
                except FetchError as error:
                    delay = max(p.delay, 2.0 ** attempt, error.retry_after or 0.0)
                    if error.retryable:
                        p.retry_not_before = time.time() + delay
                        p.event("retryable_error", error=str(error), wait_seconds=delay)
                        p.save(destination)
                    if not error.retryable or attempt == max_retries or delay > max_retry_wait:
                        raise
                    if calls < max_calls:
                        time.sleep(delay)
            if page is None:
                break
            page_keys = [record_key(api.name, r) for r in page.records]
            if len(set(page_keys)) != len(page_keys) or known.intersection(page_keys):
                raise RuntimeError("duplicate record identifiers in a page; page rejected, completeness is unverified")
            if page.total is not None and rec.expected is not None and page.total != rec.expected:
                raise RuntimeError("API total changed during retrieval; keep this partial result and start a fresh query")
            expected = page.total if page.total is not None else rec.expected
            if not page.records and expected is not None and len(known) < expected:
                raise PaginationShortfall("API ended early with an empty page before the advertised total; cursor retained for retry")
            if page.total is not None:
                rec.expected = page.total
            for note in page.notes or []:
                if note not in rec.notes:
                    rec.note(note)
            known.update(page_keys)
            p.buffered.extend(page.records)
            p.next_state = page.next_state
            p.exhausted = page.next_state is None
            p.last_page_at = time.time()
            rec.pages += 1
            p.save(destination)
    except (Exception, KeyboardInterrupt) as error:
        p.status = "interrupted" if isinstance(error, KeyboardInterrupt) else "failed"
        rec.error = "interrupted by user" if isinstance(error, KeyboardInterrupt) else str(error)
        p.event(p.status, error=rec.error)
        p.save(destination)
        raise

    if rec.stopped_at_limit:
        p.status = "partial"
    elif rec.expected is None:
        p.status = "unverified"
    elif rec.complete:
        p.status = "complete" if p.records else "zero_hits"
    else:
        p.status = "failed"
    p.event("finished", status=p.status, retrieved=len(p.records))
    p.save(destination)
    return p.records, rec, p.urls


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Paginate one of this skill's APIs with the correct step, the correct stop "
            "condition, and count reconciliation. Exits 4 on a reconciliation shortfall."
        ),
        epilog="python3 %(prog)s --api biorxiv --query 2024-01-01/2024-01-03",
    )
    # Not `required=True`: --list-apis is the flag you reach for when you do not yet
    # know what to pass for either of these.
    parser.add_argument("--api", choices=sorted(APIS), help="which API to walk")
    parser.add_argument("--query", help="see --list-apis for the per-API format")
    parser.add_argument("--page-size", type=int, default=100, help="requested page size (default 100)")
    parser.add_argument(
        "--max-records",
        type=int,
        default=DEFAULT_MAX_RECORDS,
        help=f"stop after this many records (default {DEFAULT_MAX_RECORDS})",
    )
    parser.add_argument(
        "--max-calls",
        type=int,
        default=DEFAULT_MAX_CALLS,
        help=f"request budget per invocation, including retries (default {DEFAULT_MAX_CALLS})",
    )
    parser.add_argument("-o", "--output", help="JSON result and checkpoint; saved atomically after each page")
    parser.add_argument("--resume", help="resume a checkpoint; API and query are inferred unless supplied")
    parser.add_argument("--max-retries", type=int, default=2, help="retries per request after transient failures (default 2)")
    parser.add_argument("--max-retry-wait", type=float, default=60.0,
                        help="stop and save if a required retry wait exceeds this many seconds (default 60)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the first URL that would be requested and exit without fetching",
    )
    parser.add_argument("--list-apis", action="store_true", help="describe each API's query format")
    parser.add_argument("-v", "--verbose", action="store_true", help="log each URL to stderr")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.list_apis:
        emit({name: {"delay_seconds": api.delay, "query_format": api.note}
              for name, api in sorted(APIS.items())}, args.output)
        return 0
    for name in ("page_size", "max_records", "max_calls"):
        if getattr(args, name) < 1:
            fail(f"--{name.replace('_', '-')} must be at least 1")
    if args.max_retries < 0 or not math.isfinite(args.max_retry_wait) or args.max_retry_wait <= 0:
        fail("--max-retries must be nonnegative and --max-retry-wait must be finite and positive")
    try:
        progress = Progress.load(args.resume) if args.resume else None
        if progress:
            if args.api is not None and args.api != progress.api:
                raise RuntimeError("resume API does not match checkpoint")
            if args.query is not None and args.query != progress.query:
                raise RuntimeError("resume query does not match checkpoint")
            args.api, args.query = progress.api, progress.query
        if not args.api or not args.query:
            raise RuntimeError("--api and --query are both required (use --list-apis); or supply --resume")
        if args.api not in APIS:
            raise RuntimeError("checkpoint names an unsupported API")
        validate_query(args.api, args.query)
        api = APIS[args.api]
        if progress is None:
            progress = Progress(api.name, args.query, api.initial_state)
        if len(progress.records) > args.max_records:
            raise RuntimeError("resume --max-records cannot be smaller than the already exported record count")
        state = progress.next_state
        if state is not None:
            if isinstance(api.initial_state, int):
                if type(state) is not int or state < 0:
                    raise RuntimeError("checkpoint offset must be a nonnegative integer")
            elif not isinstance(state, str) or not state:
                raise RuntimeError("checkpoint cursor must be a nonempty string")
        identities = [record_key(api.name, row) for row in progress.records + progress.buffered]
        if len(set(identities)) != len(identities):
            raise RuntimeError("checkpoint contains duplicate identifiers")
        progress.urls = [redact_url(url) for url in progress.urls]
        destination = Path(args.output or args.resume or
            f"paper-lookup-{api.name}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}.json")
        if destination.exists() and (not args.resume or destination.resolve() != Path(args.resume).resolve()):
            raise RuntimeError("output already exists; use --resume or choose a new output path")
    except (RuntimeError, OSError, ValueError, TypeError) as error:
        fail(str(error), code=2)
    if args.dry_run:
        will_fetch = not progress.exhausted and len(progress.records) + len(progress.buffered) < args.max_records
        emit({"api": api.name, "first_url": redact_url(api.build_url(args.query, progress.next_state,
              min(args.page_size, args.max_records - len(progress.records)))) if will_fetch else None,
              "delay_seconds": api.delay, "query_format": api.note, "output": str(destination),
              "will_fetch": will_fetch, "buffered_records": len(progress.buffered)}, None)
        return 0
    try:
        records, reconciliation, urls = walk(api, args.query, page_size=args.page_size,
            max_records=args.max_records, max_calls=args.max_calls, verbose=args.verbose,
            progress=progress, destination=destination, max_retries=args.max_retries,
            max_retry_wait=args.max_retry_wait)
    except (Exception, KeyboardInterrupt) as error:
        if not args.output and not args.resume:
            emit(progress.envelope(), None)
        message = "interrupted" if isinstance(error, KeyboardInterrupt) else str(error)
        code = 130 if isinstance(error, KeyboardInterrupt) else 4 if isinstance(error, PaginationShortfall) else 1
        fail(f"{message}; inspect progress at {destination}", code=code)
    if not args.output and not args.resume:
        emit(progress.envelope(), None)
    sys.stderr.write(f"progress saved to {destination} ({progress.status})\n")
    if not reconciliation.ok:
        fail(f"reconciliation failed: retrieved {len(records)} of {reconciliation.expected}; "
             f"inspect {destination} before using these results", code=4)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
