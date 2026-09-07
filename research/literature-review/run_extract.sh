#!/bin/bash
cd /home/fuge/.openclaw/workspace/skills/literature-review
python3 -c "
import json
with open('results.json', 'r') as f:
    data = json.load(f)
if isinstance(data, dict) and 'data' in data:
    results = data['data']
else:
    results = data
with open('results_array.json', 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f'Extracted {len(results)} results')
"
