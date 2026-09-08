---
name: module-structure
description: Route module-structure work to cohesion-locality or modularity-review. User-invoked.
disable-model-invocation: true
metadata:
  targets: [claude, cursor, codex, agents]
---

# Module Structure

An optional composition entrypoint for two independently usable first-party skills. Select and apply only the capabilities the task needs; composition means the same agent reads and applies the relevant skills, not mandatory subagents or a fixed two-skill pipeline. Install both companion skills for the full workflow. If one is unavailable, identify the missing capability and complete supported work without claiming a handoff occurred. Matt's `codebase-design` / `improve-codebase-architecture` are optional external tools when explicitly requested and available; ordinary design exploration can stay within this workflow.

## Pick

Use these as starting points. Inspect the actual question and code when wording is ambiguous; keywords are clues rather than hard dispatch rules.

| The user is asking | Use |
| --- | --- |
| Stay together or split? Change axis? Over-split, shrinking files, one-class-per-file, extract a helper, catch-all utils/helpers/common, Manager/Helper | `cohesion-locality` |
| Messy, over-abstraction, scattered error mapping, hard-to-test handlers/components, same change in many files, PR structure, cross-module refactor, shallow, leakage, cosplay | `modularity-review` |
| Adopt Clean / hexagonal / DDD layering? Add ports, interfaces, DI? | `modularity-review` (compare the benefit and cost; distinguish exploration from an adoption recommendation) |
| Open-ended structure exploration / architecture survey | Relevant boundary or surface analysis; use external tools when explicitly requested and available. HTML alone is a format choice. |
| Deepen a chosen candidate / design its public surface | `modularity-review` Mode C |

If both of the first two rows match (e.g. "this file does too much"), usually start with `cohesion-locality` when ownership is the uncertainty; an already-established boundary need not be reconsidered. If no row matches (bug fix, formatting, rename), say so; do not force a structural frame.

## Handoff and continuation

Choose one initial skill. A handoff is a change of focus within the same task, not a new user request or a reason to stop the task.

- `cohesion-locality` determines ownership and whether to split, join, or keep the unit intact. If that answers the user's question, finish there. Otherwise carry the decision into `modularity-review` for the remaining surface, design, or implementation work.
- When `modularity-review` discovers unclear ownership or independent change axes, suspend only the affected structural recommendation and consult `cohesion-locality`. Then resume the original mode with the boundary decision. Do not repeat completed inspection or ask the user to restart the task.
- Reuse established boundary conclusions. Revisit them when new evidence, a useful counterexample, or an exploratory alternative could change the judgment. Repeating the same unresolved question without learning is usually unhelpful; state the uncertainty and continue useful work instead. Ask when missing user information materially blocks progress.

Retain the following context across continuation; a separate handoff form is unnecessary when it is already clear:

- **User intent and scope:** review, design, or implementation; the area and requested deliverable.
- **Boundary decision and evidence:** ownership, split/join/keep, why, and any unresolved uncertainty.
- **Constraints:** behavior/public contracts to preserve and relevant project or user limits.
- **Remaining work and return mode:** the unanswered question and the mode to resume.

Preserve the user's task kind. A review stays a review (Mode A/B); a requested surface design uses Mode C; Mode D requires an implementation request already present in the conversation. Finding code that should change does not authorize implementing it. Existing implementation authorization carries through the handoff without another confirmation. A keep-together decision does not prevent an authorized surface simplification within that boundary.

## Maintenance

Both skills are first-party (`modularity-review` is a full fork — provenance in its README; no upstream tracking). The routing regression set lives in `evals/routing-queries.json`. Run and score it using [evals/README.md](evals/README.md) whenever routing or handoff rules change. Each case names one initial route; contextual cases also check continuation, scope, and boundary outcomes.
