#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import gzip
import re
from pathlib import Path


REFERENCE_COLUMNS = ["accession", "ref_type", "identifier", "url", "note"]


def parse_geo_references(soft_path: Path | str) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    series = ""
    sample = ""

    with gzip.open(soft_path, "rt", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            if line.startswith("^SERIES = "):
                series = line.removeprefix("^SERIES = ").strip()
                sample = ""
                continue
            if line.startswith("^SAMPLE = "):
                sample = line.removeprefix("^SAMPLE = ").strip()
                continue

            if line.startswith("!Series_pubmed_id = "):
                pmid = line.removeprefix("!Series_pubmed_id = ").strip()
                _append_once(
                    refs,
                    seen,
                    series,
                    "PubMed",
                    pmid,
                    f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    "GEO Series citation",
                )
            elif line.startswith("!Series_relation = BioProject: "):
                url = line.removeprefix("!Series_relation = BioProject: ").strip()
                identifier = _last_token(url)
                _append_once(refs, seen, series, "BioProject", identifier, url, "GEO Series relation")
            elif line.startswith("!Series_relation = SRA: "):
                url = line.removeprefix("!Series_relation = SRA: ").strip()
                identifier = _extract_srx(url) or _last_token(url)
                _append_once(refs, seen, series, "SRA", identifier, url, "GEO Series relation")
            elif line.startswith("!Sample_relation = SRA: "):
                url = line.removeprefix("!Sample_relation = SRA: ").strip()
                identifier = _extract_srx(url) or _last_token(url)
                _append_once(refs, seen, sample, "SRA", identifier, url, "GEO Sample relation")
            elif line.startswith("!Sample_relation = BioSample: "):
                url = line.removeprefix("!Sample_relation = BioSample: ").strip()
                identifier = _last_token(url)
                _append_once(refs, seen, sample, "BioSample", identifier, url, "GEO Sample relation")

    return refs


def write_references_tsv(refs: list[dict[str, str]], output_path: Path | str) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=REFERENCE_COLUMNS,
            delimiter="\t",
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for ref in refs:
            writer.writerow(ref)


def _append_once(
    refs: list[dict[str, str]],
    seen: set[tuple[str, str, str]],
    accession: str,
    ref_type: str,
    identifier: str,
    url: str,
    note: str,
) -> None:
    key = (accession, ref_type, identifier)
    if key in seen:
        return
    seen.add(key)
    refs.append(
        {
            "accession": accession,
            "ref_type": ref_type,
            "identifier": identifier,
            "url": url,
            "note": note,
        }
    )


def _extract_srx(text: str) -> str:
    match = re.search(r"SRX\d+", text)
    return match.group(0) if match else ""


def _last_token(url: str) -> str:
    return url.rstrip("/").rsplit("/", 1)[-1].split("=", 1)[-1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Parse GEO family SOFT publication and repository links into references.tsv.",
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Dataset directory containing raw/GSE*_family.soft.gz, or SOFT file path.",
    )
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        help="Output references.tsv path. Required when input is a SOFT file.",
    )
    args = parser.parse_args(argv)

    soft_path, output_path = _resolve_input_output(args.input, args.output, parser)
    write_references_tsv(parse_geo_references(soft_path), output_path)
    return 0


def _resolve_input_output(
    input_path: Path,
    output_path: Path | None,
    parser: argparse.ArgumentParser,
) -> tuple[Path, Path]:
    if input_path.is_dir():
        candidates = sorted(input_path.glob("raw/GSE*_family.soft.gz"))
        if not candidates:
            parser.error(f"no raw/GSE*_family.soft.gz found under {input_path}")
        if len(candidates) > 1:
            parser.error(f"multiple GSE family SOFT files found under {input_path}")
        return candidates[0], output_path or input_path / "references.tsv"

    if output_path is None:
        parser.error("output is required when input is a SOFT file")
    return input_path, output_path


if __name__ == "__main__":
    raise SystemExit(main())
