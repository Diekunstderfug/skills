# Routing and continuation evaluation

Run from the repository root:

```sh
python3 module-structure/evals/check.py
python3 module-structure/evals/check.py --results /tmp/module-structure-results.json
```

The first command validates the dataset, not model behavior. The second compares recorded observations with expectations. Neither command invokes an agent. Passing a JSON consistency check is not evidence that the skill behaves correctly.

## Behavioral procedure

Use a fresh evaluation context for each case. Supply the router, both downstream skills and accessible references, the case's `query`, and its optional `context`. Do not expose `expected`, `route`, `should_route`, or `note` to the evaluated agent. Contextual code snippets are inspection fixtures, not runnable application tests; do not invent missing implementation details. For implementation cases, use a disposable workspace and inspect whether the agent continues within existing authorization. If a fixture cannot support actual edits, assess continuation intent and record that limitation in the evidence.

Observe the initial route and, where expected, the skill consultation path, requested task kind, boundary decision, and scope. `edits_allowed` means whether the conversation authorizes target-code edits; verify that the response respects it. `repeat_approval` means asking again for implementation permission already supplied. A path records the initial skill and subsequent handoffs in this case, not consultations mentioned in prior-turn context. `none` means ordinary work without structural routing, not refusal to perform the task.

Record one result per case, backed by the actual response/transcript, in this shape:

```json
[
  {
    "id": "route-01",
    "observed": {"route": "modularity-review"},
    "evidence": "Transcript path or excerpt showing the observed route and behavior"
  }
]
```

For contextual cases, record every field listed in `expected`, based on observed behavior. The scorer reports missing cases/fields and mismatches; a pass requires all expected observations to match. Do not manufacture observations by copying expectations. Review transcript evidence manually: the scorer cannot verify its truth. Report dataset validation, scorer checks, and actual behavioral evaluation separately.

When adding cases, prefer ambiguous requests, Chinese phrasing, prior authorization, and concrete ownership evidence over more easy keyword matches. An HTML output request does not itself request an external visual architecture survey skill.
