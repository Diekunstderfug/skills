#!/bin/bash
cd /home/fuge/.openclaw/workspace/skills/literature-review
python3 -c "
import json
with open('results_array.json', 'r') as f:
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
for r in sorted(relevant, key=lambda x: x.get('year', 0), reverse=True):
    print(f\"Year: {r.get('year')}, DOI: {r.get('doi')}, Title: {r.get('title', 'N/A')[:80]}\")
    print(f'  Citations: {r.get(\"citationCount\", 0)}, Source: {r.get(\"source\", \"N/A\")}')
" 2>&1
