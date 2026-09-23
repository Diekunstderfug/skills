# Result-processing regression tests

Adapted from K-Dense-AI/scientific-agent-skills, commit
`49c6e97775eaa18ba791bebe23162a70ae601c18`,
[`tests/literature-review/test_scripts.py`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/49c6e97775eaa18ba791bebe23162a70ae601c18/tests/literature-review/test_scripts.py).
MIT license retained in LICENSE.upstream.md.

The 31 offline tests cover deduplication, ranking, year filtering, summaries,
JSON/Markdown/BibTeX formatting, and their combined pipeline. Test bodies are
unchanged. Import paths are adapted for this standalone skill; schematic contract
tests and the host-dependent PDF tooling check are omitted.

Run from the skill directory:

```sh
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

These tests do not verify live provider availability, query recall, or API pagination.
