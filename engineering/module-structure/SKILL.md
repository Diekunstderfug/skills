---
name: module-structure
description: Route module-structure work to cohesion-locality or modularity-review. User-invoked.
disable-model-invocation: true
metadata:
  targets: [claude, cursor, codex, agents]
---

# Module Structure

One entry for the two first-party module-structure skills. They are orthogonal and maintained together. Matt's `codebase-design` / `improve-codebase-architecture` stay outside: invoke those by name when you want an open-ended deepening workshop or a visual architecture survey.

## Pick

| The user is asking | Use |
| --- | --- |
| Stay together or split? Change axis? Over-split, shrinking files, one-class-per-file, extract a helper, catch-all utils/helpers/common, Manager/Helper | `cohesion-locality` |
| Messy, over-abstraction, scattered error mapping, hard-to-test handlers/components, same change in many files, PR structure, cross-module refactor, shallow, leakage, cosplay | `modularity-review` |
| Adopt Clean / hexagonal / DDD layering? Add ports, interfaces, DI? | `modularity-review` (default: no, unless it solves present complexity) |
| Open-ended deepening workshop / visual architecture survey | Matt, by slash command |
| Deepen a chosen candidate / design its public surface | `modularity-review` Mode C |

If both of the first two rows match (e.g. "this file does too much"), start with `cohesion-locality` — the cut decision comes before structuring the cut. If no row matches (bug fix, formatting, rename), say so; do not force a structural frame.

## Handoff (one way, once)

1. `cohesion-locality` decides the cut (or that there is no cut).
2. If a surface must shrink, leakage must move, or code must change: `modularity-review` Mode C or D.
3. If `modularity-review` hits "stacked axes / no one-sentence responsibility": **stop**, do not invent a boundary, use `cohesion-locality`.

Do not fire both from the same trigger sentence. Do not loop.

## Maintenance

Upstream is `_reviewing-code-modularity-skill` (tracked copy — do not edit; update via `skillshare update`, then port diffs by hand, see `modularity-review/README.md`). The routing regression set lives in `evals/routing-queries.json` (ported from upstream `evals/trigger-queries.json`, annotated with the expected skill): every `should_route` query names exactly one route. Re-run it whenever the Pick table changes.
