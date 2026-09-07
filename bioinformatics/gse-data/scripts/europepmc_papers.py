#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import urllib.parse
import subprocess
from pathlib import Path


OUT_COLUMNS = [
    "pmid",
    "pmcid",
    "doi",
    "title",
    "is_open_access",
    "has_pdf",
    "pdf_path",
    "status",
    "source_url",
]


def read_pubmed_ids(references_tsv: Path) -> list[str]:
    pmids: list[str] = []
    with references_tsv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            if row.get("ref_type") == "PubMed" and row.get("identifier"):
                pmids.append(row["identifier"])
    return pmids


def query_europepmc(pmid: str) -> dict[str, str]:
    query = urllib.parse.quote(f"EXT_ID:{pmid} AND SRC:MED")
    url = (
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        f"?query={query}&format=json&pageSize=1"
    )
    data = _fetch_bytes(url)
    if data is None:
        return {"pmid": pmid, "query_status": "query_error"}
    parsed = json.loads(data.decode("utf-8"))
    results = parsed.get("resultList", {}).get("result", [])
    return results[0] if results else {}


def download_papers(dataset_dir: Path) -> list[dict[str, str]]:
    references_tsv = dataset_dir / "references.tsv"
    papers_dir = dataset_dir / "papers"
    papers_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []

    for pmid in read_pubmed_ids(references_tsv):
        meta = query_europepmc(pmid)
        row = _base_row(pmid, meta)
        if meta.get("query_status") == "query_error":
            row["status"] = "query_error"
            rows.append(row)
            continue
        if meta.get("isOpenAccess") != "Y" or meta.get("hasPDF") != "Y":
            row["status"] = "no_open_pdf"
            rows.append(row)
            continue

        filename = _paper_filename(pmid, meta)
        output = papers_dir / filename
        candidates = _pdf_candidates(meta)
        for url in candidates:
            status = _try_download_pdf(url, output)
            row["source_url"] = url
            if status == "downloaded":
                row["pdf_path"] = str(output.relative_to(dataset_dir))
                row["status"] = status
                break
            row["status"] = status
        rows.append(row)

    return rows


def write_manifest(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=OUT_COLUMNS,
            delimiter="\t",
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def _base_row(pmid: str, meta: dict[str, str]) -> dict[str, str]:
    return {
        "pmid": pmid,
        "pmcid": meta.get("pmcid", ""),
        "doi": meta.get("doi", ""),
        "title": meta.get("title", ""),
        "is_open_access": meta.get("isOpenAccess", ""),
        "has_pdf": meta.get("hasPDF", ""),
        "pdf_path": "",
        "status": "not_attempted",
        "source_url": "",
    }


def _paper_filename(pmid: str, meta: dict[str, str]) -> str:
    pmcid = meta.get("pmcid") or "no-pmcid"
    return f"PMID{pmid}_{pmcid}.pdf"


def _pdf_candidates(meta: dict[str, str]) -> list[str]:
    urls: list[str] = []
    pmcid = meta.get("pmcid", "")
    if pmcid:
        urls.append(f"https://europepmc.org/articles/{pmcid}?pdf=render")
    doi = meta.get("doi", "")
    if doi.startswith("10.1038/"):
        article = doi.rsplit("/", 1)[-1]
        urls.append(f"https://www.nature.com/articles/{article}.pdf")
    return urls


def _try_download_pdf(url: str, output: Path) -> str:
    data = _fetch_bytes(url)
    if data is None:
        return "download_error"
    if not data.startswith(b"%PDF"):
        if output.exists():
            output.unlink()
        return "non_pdf_response"
    output.write_bytes(data)
    return "downloaded"


def _fetch_bytes(url: str) -> bytes | None:
    result = subprocess.run(
        ["curl", "-L", "--max-time", "180", "-A", "gse-data-skill/1.0", url],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Download open-access paper PDFs for PubMed rows in references.tsv.",
    )
    parser.add_argument("dataset_dir", type=Path, help="Dataset directory with references.tsv")
    args = parser.parse_args(argv)

    rows = download_papers(args.dataset_dir)
    write_manifest(rows, args.dataset_dir / "papers" / "paper_downloads.tsv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
