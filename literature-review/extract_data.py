#!/usr/bin/env python3
import json

# Load results
with open('/home/fuge/.openclaw/workspace/skills/literature-review/results.json', 'r') as f:
    data = json.load(f)

# Extract the data array
if isinstance(data, dict) and 'data' in data:
    results = data['data']
else:
    results = data

# Save as plain array
with open('/home/fuge/.openclaw/workspace/skills/literature-review/results_array.json', 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(results)} results")
