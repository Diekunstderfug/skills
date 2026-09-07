#!/bin/bash
cd /home/fuge/.openclaw/workspace/skills/literature-review
python3 scripts/search_databases.py results_array.json --deduplicate --format markdown --summary > review.md 2>&1
echo "Exit code: $?"
