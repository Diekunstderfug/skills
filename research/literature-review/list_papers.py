#!/usr/bin/env python3
import json
with open('/home/fuge/.openclaw/workspace/skills/literature-review/results_array.json', 'r') as f:
    results = json.load(f)

# Filter to last 3 years (2023-2026) and BRCAness/HRD relevant
relevant = []
for r in results:
    year = r.get('year')
    try:
        year = int(year)
    except:
        continue
    if year >= 2023 and year <= 2026:
        title = r.get('title', '') or ''
        abstract = r.get('abstract', '') or ''
        if ('BRCA' in title or 'HRD' in title or 'BRCAness' in title or 'BRCAlike' in title or 'homologous' in abstract.lower()):
            relevant.append(r)

print(f'Relevant papers from 2023-2026: {len(relevant)}')
for r in sorted(relevant, key=lambda x: str(x.get('year', '0')), reverse=True):
    year = r.get('year')
    doi = r.get('doi') or 'NO DOI'
    title = r.get('title', 'N/A')[:80]
    cites = r.get('citationCount', 0)
    src = r.get('source', 'N/A')
    print(f"[{year}] {doi}")
    print(f"  {title}")
    print(f"  cites={cites}, src={src}")
    print()
