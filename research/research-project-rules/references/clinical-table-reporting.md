# Clinical Table Reporting

Use this reference for clinical Table 1 and clinicopathological subgroup tables produced by R. These retained table conventions are conditional guidance, not universal project rules. Preserve an existing working implementation; package and typography preferences are not reasons to rewrite it. A presentation or export task does not authorize changing statistical methods or denominators.

## Freeze the comparison contract

Before building the table, write down:

- the analysis unit and eligible population;
- the top-level groups and any nested subgroups;
- the two columns or levels compared by each P value;
- whether an `All` column is descriptive or inferential;
- variables omitted from testing because they define the strata.

Let the header encode that contract. For nested comparisons, use group spanners such as `Group A -> subgroup 1 / subgroup 2 / P value`. Place the P-value column beside the columns it compares. Report one variable-level P value per comparison, normally on the variable's first row; do not create a detached P-value row beneath the variable.

Treat `All` as descriptive when it contains the comparison groups. Do not use it as an independent comparison arm.

## Adapt literature templates semantically

Use a reference article to recover hierarchy, comparison meaning, labels, and statistical footnotes. Do not copy unavailable cohorts or columns merely to reproduce its geometry. Remove inapplicable arms and rename the remaining subgroups to match the current estimand.

When a prior publication from the same research program defines a presentation category, its mapping may be reused for comparability. Implement that mapping in the table presentation layer unless the analysis data contract itself has formally changed. Preserve the cleaned categories, document the display mapping and source, and regenerate every table that shares the helper.

## Prefer semantic table builders

- Use `gtsummary` to own variable labels, category rows, missing rows, summary statistics, tests, and P-value placement.
- Use `tbl_merge()` or `tbl_strata()` for nested subgroup comparisons, and `add_variable_group_header()` for clinical section rows.
- Convert the same semantic table to `gt` for HTML and `flextable` for editable Word output; keep format-specific styling after conversion.
- Hand-build table rows only when the package model cannot express the prespecified estimand or presentation contract. Do not manually concatenate variable labels, category levels, and P values merely to reproduce a visual layout.

## Present variables and missingness

- Use domain-standard labels; keep established biomarkers and abbreviations such as ER, PR, HER2, and TNBC recognizable.
- Keep section and variable labels visually distinct from category levels. Avoid bolding every category.
- Show missing values as their own row when the journal or project requires it.
- Calculate categorical percentages from non-missing observations unless the SAP specifies another denominator; show the missing count separately.
- Keep internal workflow rationale, implementation notes, and agent-facing explanations out of the publication table. Record them in project documentation.

## Match tests to the displayed comparison

Compute every P value from the exact population and grouping shown by its adjacent columns. For a table stratified by a higher-level group, subset to that group before comparing its nested subgroups.

Follow the established analysis and SAP. The retained examples below describe possible test families; this project-rules skill does not select them as new defaults. Consider method changes only as part of a separately requested statistical task:

- continuous variables: a prespecified parametric test or Wilcoxon rank-sum test consistent with the summary statistic and distribution;
- categorical variables: Pearson chi-squared when expected-count assumptions are adequate, otherwise Fisher's exact test;
- missing observations: exclude from the variable-level test unless missingness is explicitly part of the estimand.

Unless the target journal specifies otherwise, use the shared NEJM/JAMA-style P-value display rule: format values below 0.001 as `<0.001`; use three decimal places from 0.001 to below 0.01; use two decimal places from 0.01 through 0.99; and display values above 0.99 as `>0.99`. Always select the display branch and determine statistical significance from the unrounded value. See the official [NEJM manuscript guidance](https://www.nejm.org/author-center/new-manuscripts), [JAMA instructions for authors](https://jamanetwork.com/journals/jama/pages/instructions-for-authors), and [JAMA table-creation guidance](https://jamanetwork.com/DocumentLibrary/InstructionsForAuthors/InstructionsForTableCreation.pdf). Do not infer the comparison direction from column position alone; verify it against an aggregate contingency table or group summary.

## Validate the released table

Use integer font sizes for publication-table typography. Keep them explicit in the rendering code so exports do not inherit fractional defaults; for example, use 11 pt body, 9 pt notes, and 12 pt title in Word, and integer CSS sizes in HTML.

Choose checks relevant to the changed table content or rendering; do not repeat unaffected checks or rerun an analysis solely to satisfy this list:

1. Check subgroup counts against aggregate cohort counts.
2. Check affected summaries against existing independent aggregates where useful.
3. Confirm every P-value column compares the intended adjacent groups.
4. Confirm missing rows and percentage denominators follow the table contract.
5. Inspect the affected deliverable when layout changes warrant it: HTML in a browser, or DOCX rendered to PDF/images. Check relevant headers, page breaks, fonts, and widths; do not generate unrequested formats solely for validation.
6. Check entry-script startup only when initialization or execution changes warrant it; no duplicate full run is required.
