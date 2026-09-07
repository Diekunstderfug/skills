#!/usr/bin/env python3
"""Parse all GEO Sample_characteristics fields from a GSE family SOFT file."""

from __future__ import annotations

import argparse
import csv
import gzip
import re
from pathlib import Path


BASE_COLUMNS = [
    "gsm",
    "sample_title",
    "source_name",
    "platform_id",
    "sra_experiment",
    "biosample",
]


def parse_soft(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    characteristic_keys: list[str] = []

    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            if line.startswith("^SAMPLE = "):
                if current is not None:
                    rows.append(current)
                current = {key: "" for key in BASE_COLUMNS}
                current["gsm"] = line.removeprefix("^SAMPLE = ").strip()
                continue
            if current is None:
                continue
            if line.startswith("!Sample_title = "):
                current["sample_title"] = line.removeprefix("!Sample_title = ").strip()
            elif line.startswith("!Sample_source_name_ch1 = "):
                current["source_name"] = line.removeprefix("!Sample_source_name_ch1 = ").strip()
            elif line.startswith("!Sample_platform_id = "):
                current["platform_id"] = line.removeprefix("!Sample_platform_id = ").strip()
            elif line.startswith("!Sample_characteristics_ch1 = "):
                text = line.removeprefix("!Sample_characteristics_ch1 = ").strip()
                key, value = split_characteristic(text)
                if key and key not in characteristic_keys:
                    characteristic_keys.append(key)
                current[key] = value
            elif line.startswith("!Sample_relation = SRA: "):
                current["sra_experiment"] = extract_accession(line, "SRX")
            elif line.startswith("!Sample_relation = BioSample: "):
                current["biosample"] = extract_accession(line, "SAMN")

    if current is not None:
        rows.append(current)

    columns = BASE_COLUMNS + characteristic_keys
    for row in rows:
        for column in columns:
            row.setdefault(column, "")
    rows.insert(0, {"__columns__": "\t".join(columns)})
    return rows


def split_characteristic(text: str) -> tuple[str, str]:
    if ":" not in text:
        return clean_key(text), ""
    key, value = text.split(":", 1)
    return clean_key(key), value.strip()


def clean_key(key: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", key.strip().lower()).strip("_")


def extract_accession(text: str, prefix: str) -> str:
    match = re.search(prefix + r"\d+", text)
    return match.group(0) if match else ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "dataset",
        type=Path,
        help="Dataset directory containing raw/GSE*_family.soft.gz.",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    candidates = sorted(args.dataset.glob("raw/GSE*_family.soft.gz"))
    if len(candidates) != 1:
        parser.error(
            f"expected one raw/GSE*_family.soft.gz under {args.dataset}, "
            f"found {len(candidates)}"
        )

    rows = parse_soft(candidates[0])
    columns = rows.pop(0)["__columns__"].split("\t")
    output = args.output or args.dataset / "sample_characteristics.tsv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=columns,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
