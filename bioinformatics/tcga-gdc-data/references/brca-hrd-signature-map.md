# BRCA HRD and Signature Source Map

Load this reference when the user asks about TCGA-BRCA BRCAness datasets,
external validation, TNBC labels, mutational signatures, copy-number
signatures, HRD scores, Xena, cBioPortal, METABRIC, or matching computed
endpoints back to GDC samples.

For one-off external database summaries, prefer the curated
`life-science-research` skills such as cBioPortal, NCBI Entrez/GEO, PubMed/PMC,
or other database-specific tools. Use this reference when those external facts
must be stored, source-separated, registered, audited, or joined into a local
TCGA/BRCA warehouse workflow.

## TCGA-BRCA Currentness Checks

For current/lately/updated questions, verify live GDC metadata before answering:

- `https://api.gdc.cancer.gov/status`
- `cases` endpoint filtered to the GDC project ID
- `files` endpoint filtered per profile/layer
- Latest `updated_datetime`
- `analysis.workflow_type` and `analysis.workflow_version` for harmonized files

Interpretation rule: GDC release updates, workflow updates, or file metadata
updates do not automatically mean new TCGA cases or new clinical follow-up.
State exact dates and counts.

## TCGA-BRCA TNBC Labels

If reproducibility matters, rebuild TNBC labels from local GDC clinical XML
instead of trusting a publication supplement as the sole source.

Relevant TCGA-BRCA clinical XML fields include:

- `er_status_by_ihc`
- `pr_status_by_ihc`
- `her2_status_by_ihc`
- `her2_fish_status`
- `her2_cent17_ratio`

Record the HER2 rule explicitly, especially for IHC equivocal or FISH-negative
cases. If comparing against a publication TNBC set, keep that label as a
`legacy_reference` or `publication_label` and keep the local GDC-derived label
separate.

## Source Roles

Keep these source roles separate when they exist in a repo:

| Source type | Typical role | Boundary |
| --- | --- | --- |
| `gdc-tcga-brca` | Current GDC harmonized TCGA-BRCA open multi-omics | Primary GDC source; not publication supplement |
| `gdc-tcga-ov` | Current GDC harmonized TCGA-OV open multi-omics | Same GDC pattern as BRCA |
| GDC PanCan-DDR 2018 supplement | Fixed TCGA DDR/HRD score publication source | Canonical fixed `HRD_Score`; old `mutSig*` fields are not current COSMIC v3 SBS |
| GerkeLab TCGAhrd | Convenience mirror/clinical join of PanCan-DDR | Cross-check only; not a new HRD source |
| Synapse/PCAWG7 SBS table | TCGA WES SigProfiler SBS assignment source | Use for modern `SBS3` naming when available |
| Nature copy-number signatures | TCGA copy-number signature attributions | Use for `CN17`; do not invent CN17 from raw segments without a method |
| CHORD source | HRD probabilities/classes | Separate from LOH+TAI+LST scar `HRD_Score` |
| Nik-Zainal breast WGS | Breast WGS clinical/signature/HRD components | Not TCGA; useful external WGS validation |
| Smid breast WGS refit | SBS/DBS/ID/SV refit endpoints | Useful for `SBS3`, `SBS8`, `ID6`, `ID8`, `SV3`, `SV5` |
| cBioPortal/DataHub METABRIC | METABRIC clinical/expression/CNA/mutation | Microarray and targeted mutation; not RNA-seq TPM or genome-wide SBS extraction |
| Pereira METABRIC mutationalProfiles | METABRIC ASCAT and targeted mutation | Can provide scarHRD input; no score unless scarHRD is run and recorded |
| Xena TCGA-BRCA curated bundle | Curated mirror/supplement | Keep separate from GDC; record hub/dataset IDs and redirects |

## Endpoint Rules

- `HRD_Score`: use fixed PanCan-DDR/GDC supplement when registered; do not
  replace it with a mirror unless explicitly cross-checked.
- `SBS3`: prefer a registered SigProfiler/COSMIC-v3-compatible source. Do not
  equate old `mutSig3` with modern `SBS3` unless the analysis states why.
- `CN17`: use a registered CN-signature attribution source. Raw GDC CNV files
  are inputs, not CN17 calls.
- `ID6` and `ID8`: use a registered indel-signature/refit source. Standard GDC
  MAF files alone do not contain precomputed ID signatures.
- `CHORD p_hrd` and `hr_status`: probability/classification outputs, not
  LOH+TAI+LST scar scores.
- scarHRD from ASCAT/ASCN segments: only claim a scarHRD score if the package
  was actually run, versioned, and recorded. Otherwise call the table
  `scarHRD input`.

## Xena and Mirrors

Use Xena as a curated supplement, not as the primary raw authority replacing
GDC. Store as its own source, for example:

```text
data/xena-tcga-brca-curated/
  raw/
  metadata/
  processed/
  README.md
```

Record hub URL, dataset IDs, download URL, access date, checksums, and whether
the download URL redirected to another host such as S3.

## Public-Data Warehouse Boundary

This kind of repository should store:

- source-separated raw files
- manifests and checksums
- source-local parsed outputs
- reusable harmonized tables
- endpoint dictionaries

Downstream BRCAness/modeling projects should handle:

- cohort filters
- TNBC rule choices
- model training and calibration
- matching endpoint sources to analysis cohorts
- operating-point selection and threshold transport checks
