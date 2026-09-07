#!/bin/bash
cd /home/fuge/.openclaw/workspace/skills/literature-review
python3 scripts/lit_search.py search "BRCAness HRD" --limit 20 --source all > results.json 2>&1
