---
name: cohesion-locality
description: >-
  Evaluates whether code should stay together, split, join, or move to
  a better owner, using cohesion, change locality, and shared invariants.
  Use for responsibility/change-axis boundaries, over-splitting, shrinking
  files, one-class-per-file, helper extraction, catch-all modules,
  Manager/Helper classes, or misplaced knowledge. For public-surface complexity
  and dependency review, modularity-review is complementary.
metadata:
  targets: [claude, cursor, codex, agents]
---

# Cohesion and Locality

Help the user find boundaries that make code easier to understand, change, and debug. Prefer cohesive units over merely small units. Keep knowledge and behavior together when they share a meaningful invariant, contract, lifecycle, or reason to change; consider separating independent responsibilities when that improves locality.

These are design principles, not a prescribed architecture. Adapt their application to the code, language, project constraints, and requested depth. Exploration can use tentative scenarios and alternative boundaries; a confident recommendation needs stronger support than an exploratory idea.

## Choose the useful detail

Start with the requested unit and enough code context to understand its role. Use the following references when their detail helps; read the relevant section rather than loading the whole reference set. A straightforward judgment can finish from this entrypoint. For a nontrivial case, start with the most relevant reference; another is useful only if a different question remains. The review checklist is optional, not a prerequisite for every review.

| Current question | Reference |
| --- | --- |
| How to inspect, explore alternatives, challenge a cut, or report a finding? | [Review and exploration](references/review-checklist.md) |
| Does this function mix concerns, or is it cohesive orchestration? | [Function design](references/unit-boundaries.md#function-design) |
| Do this class's state, collaborators, and lifecycle belong together? | [Class design](references/unit-boundaries.md#class-design) |
| Split this file, move helpers, or reorganize a package? | [File design](references/unit-boundaries.md#file-design) and [package boundaries](references/unit-boundaries.md#module-and-package-boundaries) |
| Who determines a rule, or do same-named concepts mean the same thing? | [Rules and meaning](references/ownership-locality.md#rules-and-meaning) |
| Who owns state, copies, tasks, cleanup, or synchronization? | [State and consistency](references/ownership-locality.md#state-and-consistency), [lifetimes](references/ownership-locality.md#work-and-resource-lifetimes), or [synchronization](references/ownership-locality.md#shared-state-and-synchronization) in the same reference |
| Will a proposed boundary improve change/failure locality enough to justify its cost? | [Locality](references/ownership-locality.md#change-and-failure-locality) and [boundary cost](references/ownership-locality.md#boundary-cost) |

These routes can combine when the question crosses levels. To locate detail cheaply, list headings with `rg '^##' references/*.md` or search the relevant concept. References supply judgment aids, not another set of independently invoked skills. [Examples](references/examples.md) are a separate optional lookup: use a matching section when a concrete contrast helps, rather than loading them by default.

## Default approach

A useful path is **inspect → hypothesize → challenge → recommend**; adapt or revisit it as needed. Anchor a material finding in code and its contract, consider the most relevant counterevidence, and explain the practical benefit and cost of the proposed boundary. Distinguish facts, inferences, and exploratory ideas. Hypothetical changes are welcome as probes, not proof that a refactor is required.

Lead with the useful conclusion, including keep-together when appropriate. Optional priorities are **Required** for demonstrated correctness or hard-rule violations, **Recommended** for supported maintenance improvements, and **Explore** for promising conditional alternatives. Use only the report detail the decision needs; uncertainty need not prevent useful exploration.

## Judgment aids

- **Size and naming:** long functions, many methods, `Manager`, `helpers`, or “and” in a description are inspection clues, not verdicts. A cohesive file can remain large; a tiny helper can still belong elsewhere.
- **Thin boundaries:** a one-use pass-through may add nothing, or may protect an actual compatibility contract or test boundary. Evaluate what it isolates and what removing it would expose.
- **Ownership:** distinguish rule meaning, authoritative state, intentional copies, and the owner of work or cleanup; the same entity name does not settle these questions.
- **Lifecycle and sequence:** grouping only by `init/process/finish` often hides ownership. A lifecycle with legal states, resource ownership, and cleanup obligations can itself be a cohesive responsibility.
- **Orchestration:** coordinating validation, storage, and notifications can be one use case. Examine whether it also owns unrelated policy or protocol internals, and whether that causes friction.
- **Duplication:** identical text can encode different rules. Conversely, different-looking code can repeat one contract. Judge shared knowledge and its owner before joining or extracting.
- **Boundary cost:** consider moving knowledge to an existing owner or removing a redundant facade before adding new machinery; favor changes whose benefit exceeds their new names, imports, public contracts, coordination, and testing cost. Small edits are a good default, not a prohibition on a broader design when the problem or user calls for it.

## Scope and continuation

This skill is independently usable. `modularity-review` complements it for surface design and implementation, and the optional `module-structure` entrypoint coordinates combined work. If a boundary decision answers the request, finish here. Otherwise carry ownership, reasoning, constraints, and the remaining question into the relevant next step. When installed, the router's continuation guidance is in `../module-structure/SKILL.md`.

If a companion is unavailable, continue supported work and identify the limitation without claiming an invocation occurred. A missing skill does not prevent useful boundary reasoning or explicitly labeled design exploration.

Respect the user's requested scope and applicable hard project rules. A review or exploration does not authorize code edits. Existing implementation authorization remains valid through continuation. Preserve behavior and public contracts unless the user authorizes changing them, and report evidence and validation honestly. If implementation is requested, check relevant callers and behavior tests, choose validation appropriate to the change, and report any checks that could not run.

## Maintenance

Keep shared scope and core judgment principles here; maintain detailed criteria and examples in the routed references. Consolidate repeated guidance without discarding useful detail merely to shorten this file. Behavioral evaluation cases and instructions live in [evals/README.md](evals/README.md); they are not review-time reference material.
