# Boundary judgment evaluation

These twenty small code fixtures contrast atomicity versus independent policy, shared versus independent contracts, useful versus redundant thin wrappers, lifecycle versus mechanical phase grouping, live copies versus snapshots, abandoned versus supervised tasks, semantic divergence versus shared value models, and broken versus preserved synchronization. Four further cases cover the skip path (an extraction the user already decided, a routine typo fix), design before code exists, and over-splitting; two of the four use English queries. They test reasoning, not preferred wording or a single directory layout.

## Running a behavioral evaluation

For each case in `cases.json`, provide a fresh evaluating context with this skill entrypoint, access to its `references/` directory, the `query`, `context`, and the indicated fixture. Let it choose relevant reference sections through the entrypoint; do not preload all references. Do not provide `criteria` or `failures` to the evaluated agent. The fixtures are small inspection inputs; dependency implementations are intentionally absent. Evaluate the supplied scope without inventing a working application.

Keep evaluation output and any edits in a disposable workspace. Save the response and record which assertions are supported by its code reasoning. A manual evaluation is acceptable; an agent evaluation is optional when available and authorized.

Evaluate separately:

- **Issue coverage:** Did it identify the meaningful ownership or contract issue?
- **False positives:** Did it demand a split, join, or abstraction unsupported by the context?
- **Evidence:** Did it connect actual code and supplied context, distinguishing inferences from observed facts?
- **Recommendation quality:** Would its suggestion preserve relevant contracts and improve the identified problem? Accept alternatives supported by sound tradeoffs.
- **Exploration and scope:** Could it offer conditional alternatives without misrepresenting them as required fixes or editing during a review?

Use the case criteria as anchors, not exact-answer matching. Record pass, partial, or fail with a transcript excerpt and reason for each relevant dimension. Do not turn the number of headings, alternatives, or tool calls into a quality score. A materially different but justified answer merits review rather than automatic failure.

The thin-wrapper fixtures intentionally have identical code and different contracts: the judgment should respond to context, not syntax. For exploratory cases, useful hypotheses should not be penalized merely because they are unproven; presenting them as verified defects should be.

## Fixture integrity check

From the repository root:

```sh
python3 - <<'PY'
import ast
import json
from pathlib import Path
base = Path('cohesion-locality/evals')
cases = json.loads((base / 'cases.json').read_text())
assert len({c['id'] for c in cases}) == len(cases)
for case in cases:
    ast.parse((base / case['fixture']).read_text())
    assert case['criteria'] and case['failures']
print(f'{len(cases)} fixtures parsed; behavioral judgments not evaluated')
PY
```

Parsing checks only the evaluation inputs. Report it separately from any actual behavioral runs and retain raw responses before claiming improvements in review accuracy.
