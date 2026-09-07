---
name: module-structure
description: Route module-structure work to cohesion-locality or modularity-review. User-invoked.
disable-model-invocation: true
metadata:
  targets: [claude, cursor, codex, agents]
---

# Module Structure

One entry for the two first-party module-structure skills. They are orthogonal and maintained together. Matt's `codebase-design` / `improve-codebase-architecture` stay outside: invoke those by name when you want a deepening workshop or a visual survey.

## Pick

| The user is asking | Use |
| --- | --- |
| Stay together or split? Change axis? Over-split, shrinking files, one-class-per-file, extract a helper, catch-all utils/helpers/common, Manager/Helper | `cohesion-locality` |
| Messy, over-abstraction, scattered error mapping, hard-to-test handlers/components, same change in many files, PR structure, cross-module refactor, shallow, leakage, cosplay | `modularity-review` |
| Deepen this / where does the seam go / visual architecture survey | Matt, by slash command |

## Handoff (one way, once)

1. `cohesion-locality` decides the cut (or that there is no cut).
2. If a surface must shrink, leakage must move, or code must change: `modularity-review` Mode C or D.
3. If `modularity-review` hits "stacked axes / no one-sentence responsibility": **stop**, do not invent a boundary, use `cohesion-locality`.

Do not fire both from the same trigger sentence. Do not loop.
