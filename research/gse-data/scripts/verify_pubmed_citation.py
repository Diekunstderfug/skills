#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
from pathlib import Path


COLUMNS = [
    "pmid",
    "ncbi_title",
    "ncbi_doi",
    "ncbi_pmcid",
    "epmc_title",
    "epmc_doi",
    "epmc_pmcid",
    "epmc_is_open_access",
    "epmc_has_pdf",
    "pmc_oa_status",
    "crossref_title",
    "crossref_doi",
    "crossref_score",
    "doi_handle_status",
    "primary_doi_match",
    "primary_title_match",
    "epmc_doi_match",
    "status",
]


def read_pmids(input_path: Path) -> list[str]:
    if input_path.is_dir():
        refs = input_path / "references.tsv"
        pmids: list[str] = []
        with refs.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                if row.get("ref_type") == "PubMed" and row.get("identifier"):
                    pmids.append(row["identifier"])
        return _unique(pmids)
    return _unique([line.strip() for line in input_path.read_text().splitlines() if line.strip()])


def verify_pmid(pmid: str) -> dict[str, str]:
    ncbi = query_ncbi(pmid)
    epmc = query_europepmc(pmid)
    doi = ncbi.get("doi") or epmc.get("doi", "")
    crossref = query_crossref(doi, ncbi.get("title") or epmc.get("title", ""))
    doi_handle_status = query_doi_handle(doi)
    pmc_oa_status = query_pmc_oa(ncbi.get("pmcid") or epmc.get("pmcid", ""))

    primary_doi_match = _doi_match([ncbi.get("doi", ""), crossref.get("doi", "")])
    primary_title_match = _title_match(
        ncbi.get("title", ""),
        crossref.get("title", ""),
    )
    epmc_doi_match = _doi_match([ncbi.get("doi", ""), epmc.get("doi", "")])
    status = (
        "ok"
        if doi_handle_status == "ok"
        and primary_doi_match == "true"
        and primary_title_match in {"true", "not_checked"}
        else "review"
    )

    return {
        "pmid": pmid,
        "ncbi_title": ncbi.get("title", ""),
        "ncbi_doi": ncbi.get("doi", ""),
        "ncbi_pmcid": ncbi.get("pmcid", ""),
        "epmc_title": epmc.get("title", ""),
        "epmc_doi": epmc.get("doi", ""),
        "epmc_pmcid": epmc.get("pmcid", ""),
        "epmc_is_open_access": epmc.get("isOpenAccess", ""),
        "epmc_has_pdf": epmc.get("hasPDF", ""),
        "pmc_oa_status": pmc_oa_status,
        "crossref_title": crossref.get("title", ""),
        "crossref_doi": crossref.get("doi", ""),
        "crossref_score": crossref.get("score", ""),
        "doi_handle_status": doi_handle_status,
        "primary_doi_match": primary_doi_match,
        "primary_title_match": primary_title_match,
        "epmc_doi_match": epmc_doi_match,
        "status": status,
    }


def query_ncbi(pmid: str) -> dict[str, str]:
    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        f"?db=pubmed&id={urllib.parse.quote(pmid)}&retmode=json"
    )
    parsed = _fetch_json(url)
    record = parsed.get("result", {}).get(pmid, {}) if parsed else {}
    ids = record.get("articleids", [])
    return {
        "title": record.get("title", ""),
        "doi": _article_id(ids, "doi"),
        "pmcid": _clean_pmcid(_article_id(ids, "pmc") or _article_id(ids, "pmcid")),
    }


def query_europepmc(pmid: str) -> dict[str, str]:
    query = urllib.parse.quote(f"EXT_ID:{pmid} AND SRC:MED")
    url = (
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        f"?query={query}&format=json&pageSize=1"
    )
    parsed = _fetch_json(url)
    results = parsed.get("resultList", {}).get("result", []) if parsed else []
    return results[0] if results else {}


def query_crossref(doi: str, title: str) -> dict[str, str]:
    if doi:
        parsed = _fetch_json(f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}")
        message = parsed.get("message", {}) if parsed else {}
        return _crossref_record(message)
    if title:
        query = urllib.parse.urlencode({"query.title": title, "rows": "1"})
        parsed = _fetch_json(f"https://api.crossref.org/works?{query}")
        items = parsed.get("message", {}).get("items", []) if parsed else []
        return _crossref_record(items[0]) if items else {}
    return {}


def query_doi_handle(doi: str) -> str:
    if not doi:
        return ""
    url = f"https://doi.org/api/handles/{urllib.parse.quote(doi, safe='')}"
    parsed = _fetch_json(url)
    if not parsed:
        return "query_error"
    if str(parsed.get("responseCode", "")) == "1":
        return "ok"
    return f"response_{parsed.get('responseCode', 'unknown')}"


def query_pmc_oa(pmcid: str) -> str:
    if not pmcid:
        return ""
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={urllib.parse.quote(pmcid)}"
    data = _fetch_bytes(url)
    if data is None:
        return "query_error"
    try:
        root = ET.fromstring(data.decode("utf-8", errors="replace"))
    except ET.ParseError:
        return "parse_error"
    error = root.find("error")
    if error is not None:
        return error.attrib.get("code", "not_open_access")
    return "open_access" if root.find(".//record") is not None else "unknown"


def write_rows(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _fetch_json(url: str) -> dict:
    data = _fetch_bytes(url)
    if data is None:
        return {}
    try:
        return json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


def _fetch_bytes(url: str) -> bytes | None:
    env = os.environ.copy()
    for key in (
        "http_proxy",
        "https_proxy",
        "all_proxy",
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
    ):
        env.pop(key, None)
    result = subprocess.run(
        ["curl", "-L", "--max-time", "60", "-A", "gse-data-skill/1.0", url],
        check=False,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return result.stdout if result.returncode == 0 else None


def _article_id(articleids: list[dict], idtype: str) -> str:
    for item in articleids:
        if item.get("idtype") == idtype:
            return item.get("value", "")
    return ""


def _crossref_record(message: dict) -> dict[str, str]:
    titles = message.get("title") or []
    return {
        "title": titles[0] if titles else "",
        "doi": message.get("DOI", ""),
        "score": str(message.get("score", "")),
    }


def _clean_pmcid(value: str) -> str:
    match = re.search(r"PMC\d+", value, flags=re.I)
    return match.group(0).upper() if match else value


def _normalize_doi(value: str) -> str:
    return value.lower().strip().removeprefix("doi:").strip()


def _normalize_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _doi_match(values: list[str]) -> str:
    normalized = [_normalize_doi(v) for v in values if v]
    if len(normalized) < 2:
        return "not_checked"
    return "true" if len(set(normalized)) == 1 else "false"


def _title_match(*values: str) -> str:
    titles = [_normalize_title(v) for v in values if v]
    if len(titles) < 2:
        return "not_checked"
    first = titles[0]
    return "true" if all(SequenceMatcher(None, first, other).ratio() >= 0.90 for other in titles[1:]) else "false"


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify PubMed citations against NCBI, Europe PMC, PMC OA, and Crossref.",
    )
    parser.add_argument("input", type=Path, help="Dataset directory with references.tsv, or a text file of PMIDs")
    parser.add_argument("--output", type=Path, help="Output TSV path")
    args = parser.parse_args(argv)

    rows = [verify_pmid(pmid) for pmid in read_pmids(args.input)]
    output = args.output
    if output is None:
        output = args.input / "papers" / "citation_verification.tsv" if args.input.is_dir() else Path("citation_verification.tsv")
    write_rows(rows, output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
