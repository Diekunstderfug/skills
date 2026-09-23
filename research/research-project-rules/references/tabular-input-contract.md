# Source Spreadsheet Fields

Use when resolving spreadsheet columns with repeated or importer-repaired labels.

## Exact Raw-Label Resolution

- Match source columns against the worksheet's original labels exactly; preserve unrepaired labels when reading the schema.
- Treat importer-generated suffixes such as `...372` as positional repair metadata, never as clinical meaning or a field contract.
- When original labels repeat, disambiguate them only inside semantic blocks whose boundaries are themselves anchored by exact, unique original labels.
- Resolve every contracted field to exactly one column. Stop with the standard name, expected label, semantic block, and match count when resolution returns zero or multiple columns.
- Column order may remain in a schema audit for traceability, but it must not select or define analysis fields.
