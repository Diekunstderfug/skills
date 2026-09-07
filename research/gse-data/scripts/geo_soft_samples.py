#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import gzip
import re
from pathlib import Path
from typing import Iterable


SAMPLE_COLUMNS = [
    "gsm",
    "sample_title",
    "source_name",
    "platform_id",
    "tissue",
    "cell_type",
    "genotype",
    "sra_experiment",
    "sample_group",
    "sample_type_or_site",
]


def parse_geo_samples(soft_path: Path | str) -> list[dict[str, str]]:
    samples: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    with gzip.open(soft_path, "rt", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            if line.startswith("^SAMPLE = "):
                if current is not None:
                    _finalize_sample(current)
                    samples.append(current)
                current = _empty_sample(line.removeprefix("^SAMPLE = ").strip())
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
                key_value = line.removeprefix("!Sample_characteristics_ch1 = ").strip()
                key, value = _split_characteristic(key_value)
                if key == "tissue":
                    current["tissue"] = value
                elif key == "cell type":
                    current["cell_type"] = value
                elif key == "genotype":
                    current["genotype"] = value
            elif line.startswith("!Sample_relation = SRA: "):
                relation = line.removeprefix("!Sample_relation = SRA: ").strip()
                current["sra_experiment"] = _extract_srx(relation)

    if current is not None:
        _finalize_sample(current)
        samples.append(current)

    return samples


def write_samples_tsv(samples: Iterable[dict[str, str]], output_path: Path | str) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=SAMPLE_COLUMNS,
            delimiter="\t",
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for sample in samples:
            writer.writerow({column: sample.get(column, "") for column in SAMPLE_COLUMNS})


def _empty_sample(gsm: str) -> dict[str, str]:
    return {column: "" for column in SAMPLE_COLUMNS} | {"gsm": gsm}


def _split_characteristic(text: str) -> tuple[str, str]:
    if ":" not in text:
        return text.strip().lower(), ""
    key, value = text.split(":", 1)
    return key.strip().lower(), value.strip()


def _extract_srx(relation: str) -> str:
    match = re.search(r"SRX\d+", relation)
    return match.group(0) if match else relation


def _finalize_sample(sample: dict[str, str]) -> None:
    title = sample.get("sample_title", "")
    sample["sample_group"] = _infer_sample_group(title, sample.get("genotype", ""))
    sample["sample_type_or_site"] = _infer_sample_type_or_site(
        title,
        sample.get("cell_type", ""),
    )


def _infer_sample_group(title: str, genotype: str) -> str:
    lower = title.lower()
    if "brca1 pre-neoplastic" in lower:
        return "BRCA1 pre-neoplastic"
    if "triple negative brca1 tumour" in lower:
        return "triple negative BRCA1 tumour"
    if "triple negative tumour" in lower:
        return "triple negative tumour"
    if "her2+ tumour" in lower:
        return "HER2+ tumour"
    if "pr+ tumour" in lower:
        return "PR+ tumour"
    if "er+ tumour" in lower:
        return "ER+ tumour"
    if lower.startswith("normal "):
        return "normal"
    return genotype


def _infer_sample_type_or_site(title: str, cell_type: str) -> str:
    lower = title.lower()
    if "lymph-node cells" in lower:
        return "lymph-node cells"
    if "epithelial cells" in lower:
        return "epithelial cells"
    if "total cells" in lower:
        return "total cells"
    return cell_type


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Parse GEO family SOFT sample metadata into samples.tsv.",
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
        help="Output samples.tsv path. Required when input is a SOFT file.",
    )
    args = parser.parse_args(argv)

    soft_path, output_path = _resolve_input_output(args.input, args.output, parser)
    write_samples_tsv(parse_geo_samples(soft_path), output_path)
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
        return candidates[0], output_path or input_path / "samples.tsv"

    if output_path is None:
        parser.error("output is required when input is a SOFT file")
    return input_path, output_path


if __name__ == "__main__":
    raise SystemExit(main())
