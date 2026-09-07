# GEO/GSE Dataset Layout

Use this as the default repository convention unless the active repo has a
stricter AGENTS.md.

## Dataset Directory

```text
data/<GSE>/
  README.md
  samples.tsv
  sample_characteristics.tsv
  references.tsv
  papers/
    <open-access paper files, when GEO exposes PubMed citations>
  raw/
    <downloaded GEO/SRA files>
    md5sums.txt
```

`raw/` is immutable after download. Derived manifests such as `samples.tsv`,
`sample_characteristics.tsv`, and `references.tsv` live beside `raw/`, not
inside it. Paper files go under `papers/`, never `raw/`.

## What To Download

Minimum provenance set:

- `<GSE>_family.soft.gz`
- `<GSE>_family.xml.tgz`
- `<GSE>_series_matrix.txt.gz`
- all files from `suppl/`
- relevant GPL SOFT/MINiML platform metadata
- `RunInfo.csv` when SRA/BioProject links exist

Default SRA policy: save run metadata, do not download FASTQ/SRA sequence files
unless the user explicitly asks or the project requires reprocessing from raw
reads.

## Sample Manifest

Generate `samples.tsv` from the GSE family SOFT file. Required stable columns:

```text
gsm
sample_title
source_name
platform_id
tissue
cell_type
genotype
sra_experiment
sample_group
sample_type_or_site
```

The `sample_group` and `sample_type_or_site` columns may be derived from GEO
titles when GEO lacks explicit characteristics. Treat those labels as
title-derived in documentation.

Also generate `sample_characteristics.tsv` from the same SOFT file when full
sample metadata is useful. It should include stable base columns
`gsm`, `sample_title`, `source_name`, `platform_id`, `sra_experiment`, and
`biosample`, followed by normalized `!Sample_characteristics_ch1` keys.

Always preserve `platform_id` from `!Sample_platform_id`. Summarize per-platform
sample counts in the dataset README, `docs/sources.md`, and machine-readable
`config/sources.yaml` when those files exist.

## Publication and Repository References

Generate `references.tsv` from the GSE family SOFT file. Required stable
columns:

```text
accession
ref_type
identifier
url
note
```

Expected rows include PubMed IDs from `!Series_pubmed_id`, BioProject links from
`!Series_relation = BioProject:`, and SRA links from `!Series_relation = SRA:`
or sample-level SRA relations. This file is the default paper lookup layer.
Use only resources exposed by GEO/SOFT by default; do not search for missing
citations when GEO does not expose PMID/citation information.

Default article policy: when GEO/SOFT exposes PubMed IDs, record PubMed links
and try to download clearly open-access article PDFs into `papers/`. Record
attempts in `papers/paper_downloads.tsv`. Do not bypass paywalls. Before using
the dataset scientifically, read the available paper itself, especially abstract,
methods/study design, sample definitions, data availability, and caveats. Use
PubMed/NCBI E-utilities for extra verification only when PMID metadata is
inconsistent or citation accuracy is high-stakes.

## Source Summaries

Keep `docs/sources.md` short. It should help a future agent answer "what is
this dataset, how many samples of each relevant type does it contain, and which
paper IDs should I check?"

Put detailed URLs, platform IDs, file lists, checksums, and download dates in
machine-readable config or dataset README files.
