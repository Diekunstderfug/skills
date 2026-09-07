#!/usr/bin/env python3
"""Audit a source-separated public_data-style repository.

Checks:
- config/sources.yaml parses and has unique source IDs.
- source local_path entries exist.
- top-level data source folders are registered, ignoring generic warehouse dirs.
- source IDs appear in docs/sources.md and INDEX.md when those files exist.
- GDC download_status.tsv files have no error statuses.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment-specific
    raise SystemExit("PyYAML is required: install pyyaml or run inside the repo environment") from exc


GENERIC_DATA_DIRS = {"raw", "interim", "processed", "releases"}
OK_DOWNLOAD_STATUSES = {"skipped_verified", "downloaded_verified"}


def load_sources(repo: Path) -> list[dict]:
    path = repo / "config" / "sources.yaml"
    if not path.exists():
        raise SystemExit(f"missing {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    sources = data.get("sources") if isinstance(data, dict) else None
    if not isinstance(sources, list):
        raise SystemExit(f"{path} does not contain a top-level sources list")
    return sources


def read_text_if_exists(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def audit(repo: Path) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    sources = load_sources(repo)
    ids = [str(source.get("id", "")) for source in sources]
    empty_ids = [i for i, source_id in enumerate(ids, start=1) if not source_id]
    if empty_ids:
        errors.append(f"sources missing id at rows {empty_ids}")

    counts = Counter(ids)
    duplicates = sorted(source_id for source_id, count in counts.items() if source_id and count > 1)
    if duplicates:
        errors.append(f"duplicate source ids: {duplicates}")

    data_root = repo / "data"
    data_dirs = set()
    if data_root.exists():
        data_dirs = {
            path.name
            for path in data_root.iterdir()
            if path.is_dir() and path.name not in GENERIC_DATA_DIRS
        }
    else:
        errors.append("missing data/ directory")

    id_set = set(ids)
    missing_data_dirs = []
    for source in sources:
        source_id = source.get("id")
        local_path = source.get("local_path")
        if not source_id or not local_path:
            continue
        local = repo / str(local_path)
        if not local.exists():
            missing_data_dirs.append(f"{source_id}:{local_path}")
    if missing_data_dirs:
        errors.append(f"registered local_path missing: {missing_data_dirs}")

    unregistered_dirs = sorted(data_dirs - id_set)
    registered_without_top_dir = sorted(
        source_id
        for source_id in id_set
        if source_id and source_id not in data_dirs and (repo / "data" / source_id).exists() is False
    )
    if unregistered_dirs:
        errors.append(f"data dirs missing from registry: {unregistered_dirs}")
    if registered_without_top_dir:
        errors.append(f"registry ids without data dir: {registered_without_top_dir}")

    docs_sources = read_text_if_exists(repo / "docs" / "sources.md")
    index = read_text_if_exists(repo / "INDEX.md")
    if docs_sources:
        missing_docs = [source_id for source_id in ids if source_id and source_id not in docs_sources]
        if missing_docs:
            warnings.append(f"source ids missing from docs/sources.md: {missing_docs}")
    else:
        warnings.append("docs/sources.md not found")
    if index:
        missing_index = [source_id for source_id in ids if source_id and source_id not in index]
        if missing_index:
            warnings.append(f"source ids missing from INDEX.md: {missing_index}")
    else:
        warnings.append("INDEX.md not found")

    for source in sources:
        source_id = str(source.get("id", ""))
        status_path = source.get("download_status")
        if not status_path and source_id.startswith("gdc-tcga-"):
            candidate = repo / "manifests" / "downloads" / source_id / "download_status.tsv"
            status_path = str(candidate.relative_to(repo)) if candidate.exists() else None
        if not status_path:
            continue
        path = repo / str(status_path)
        if not path.exists():
            warnings.append(f"{source_id} download_status missing: {status_path}")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        status_counts = Counter(row.get("status", "") for row in rows)
        bad = {status: count for status, count in status_counts.items() if status not in OK_DOWNLOAD_STATUSES}
        if bad:
            errors.append(f"{source_id} bad download statuses: {bad}")
        print(f"{source_id}\tdownload_status_rows={len(rows)}\tstatuses={dict(status_counts)}")

    print(f"source_count={len(ids)}")
    print(f"data_source_dir_count={len(data_dirs)}")
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK: registry, data directories, docs coverage, and GDC download statuses passed audited checks")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".", help="Path to a public_data-style repository")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    raise SystemExit(audit(repo))


if __name__ == "__main__":
    main()
