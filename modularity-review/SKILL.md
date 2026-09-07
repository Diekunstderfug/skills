---
name: modularity-review
description: >-
  Reviews and reduces structural complexity: shallow layers, leakage,
  public-surface size, reversed dependencies, over-abstraction,
  scattered error mapping, hard-to-test handlers or components, and
  architecture cosplay. Use when a file or module is a mess, hard to
  test, or the same change lands in many places; for a PR/diff
  structure review; or for a refactor that moves code across modules.
  Do not use to decide whether units should stay together or split —
  that is cohesion-locality. Do not use for ordinary bug fixes,
  formatting, naming-only cleanup, or local edits that do not affect
  structure.
metadata:
  targets: [claude, cursor, codex, agents]
---

# Modularity Review

This skill owns **complexity at the public surface**: depth, leakage, dependency direction, testable seams, and architecture cosplay. Maintained with `cohesion-locality` (what stays together). User-invoked router: `module-structure`.

Complement, do not duplicate: if the live question is "should these stay together or split?", **stop and use cohesion-locality**. Do not invent a cut here.

## Goal

Reduce code complexity without architecture cosplay. Prefer a deep module: small, stable public surface, large hidden payoff, clear dependency direction. Use the smallest restructuring that makes code easier to understand, change, and test — never more.

## Non-negotiables

1. Inspect the actual code and nearby conventions before recommending structure. Advice given sight-unseen is usually wrong.
2. If ownership or change axes are unclear — several independent reasons to change, or no one-sentence responsibility — **stop**. Use cohesion-locality. Do not split by line count, and do not invent a boundary here.
3. Do not create Clean Architecture, DDD, hexagonal layering, SOLID-heavy layering, repositories, factories, adapters, dependency injection, ports, or interfaces unless they solve present complexity in this codebase.
4. Do not introduce interfaces, factories, or DI for a single implementation unless there is real test-seam or coupling pressure.
5. Do not propose a broad rewrite when a local restructuring solves the problem.
6. Preserve behavior unless the user explicitly asks for a behavior change.
7. Do not create or edit ADRs or other docs unless the user asks.
8. Default fix: move knowledge to its owner or delete a leftover facade. Do not add types, files, or wrappers as the first move.

## Core vocabulary

When terminology matters or you produce a report, use: module, public surface, implementation, depth, shallow module, seam, leakage, change amplification, architecture cosplay, recommendation strength. Definitions in `references/language.md`. Prefer the repo's own word when it has one.

**Responsibility**, **cohesion**, and **change axis** are defined and decided by cohesion-locality. Here they are only a stop condition.

## Before any mode

1. If the user is asking whether to split, join, or keep units together, or names a change axis: use cohesion-locality first. Resume here only after that cut is decided (Mode C/D).
2. Inspect first: folder layout, naming, import direction, nearby similar features, test style, public exports, and existing error/validation conventions.
3. For each module in scope, ask: What does it own? What should it hide? What is its public surface? Who imports it? What does it import? Can it be tested without booting the whole app? If "what does it own?" has several unrelated answers, stop and use cohesion-locality.
4. Read project context when a recommendation is broad or moves code across modules — see `references/decision-records.md`.

Judge complexity by whether future changes get harder: change amplification, cognitive load, unknown unknowns, obscurity. Load `references/red-flags.md` or `references/principles.md` by section — do not recite them. Skip stay-together / change-axis / temporal-decomposition sections; those are cohesion-locality.

## Mode selection

| Mode | Use when | Output |
| --- | --- | --- |
| **A — Fast review** | Review a file, diff, PR, module, route, component, or small area. | Findings ordered by risk. No candidate cards. |
| **B — Friction scan** | Scan for shallow layers, leakage, reversed deps, or a top recommendation. | Candidate cards + top recommendation. |
| **C — Candidate deepening** | A candidate is chosen, or the user asks to design a public surface. | Owns/hides/surface + design comparison. |
| **D — Implementation** | The user asks the agent to actually refactor. | Smallest behavior-preserving change + validation. |

Default to the smallest mode that fits. Modes chain when the task is broad: B → C → D. After cohesion-locality decides a split or join, enter at C or D.

### Mode A: Fast modularity review

Inspect the code and report findings ordered by risk. For each finding:

- **Severity** — high (change amplification or hidden bugs now: leaked decisions, reversed dependencies, side-effectful imports), medium (will bite as the feature grows: shallow layers, overexposed surface), or low (safe to defer: naming, small duplication, cosmetic).
- **File/line** if available.
- **Why it increases complexity** — name the mechanism (leakage, shallow module, reversed dependency, architecture cosplay). If the mechanism is mixed change axes or "should this be one unit?", do not score it — hand off to cohesion-locality.
- **Smallest useful fix** — behavior-preserving; prefer move-to-owner or delete facade.
- **What not to change** — only when there is a real over-refactor risk.

Do not use candidate cards and do not write an HTML report in this mode unless the user asks. Concise findings are the product.

### Mode B: Architecture friction scan

Explore the area for surface/leakage/shallow friction, then produce a candidate report using `references/review-report.md`:

- A single **top recommendation** first.
- **1–4 candidates**, each with: current friction (grounded in real code), why complexity increases, smallest useful fix, before/after sketch, testing impact, what not to change, and recommendation strength (Strong | Worth exploring | Speculative).

If a candidate's only problem is stacked change axes, drop it from this report and name cohesion-locality instead.

Markdown is the default. HTML is opt-in. After presenting candidates, ask which one to explore, unless the user already requested implementation.

### Mode C: Candidate deepening design

Use after the user selects a candidate, after cohesion-locality has chosen a cut, or when asked to design a public surface. Produce:

1. What the module **owns**.
2. What it **hides**.
3. The **public surface**.
4. **Example caller code** — the smallest realistic call site.
5. The **tests that should survive** unchanged (the behavior contract).
6. What **not** to refactor.
7. **2–4 materially different designs**, only when the decision is nontrivial.
8. **One strong recommendation**, with a one-line reason.

Load `references/interface-design.md` for the comparison. Comparing designs is not a license to add interfaces — the minimal surface often wins.

### Mode D: Behavior-preserving implementation

- Make the **smallest behavior-preserving change** that realizes the chosen design.
- Do not silently change public APIs.
- Update imports carefully; do not move code without checking callers.
- Keep unrelated cleanup out of the change.
- Carry the "what not to change" guardrail through.
- Then validate.

Close with: what changed, why the structure is better, what checks were run, and remaining risk. For tiny changes, collapse this into a short paragraph.

## Validation

After edits:

1. Run the smallest relevant tests.
2. Run typecheck if available.
3. Run lint if available.
4. Run import or dependency-boundary checks if available.
5. Inspect the final diff; confirm no unrelated refactor crept in.
6. If validation cannot run, state that clearly.

## Reference loading

Use progressive disclosure. Reach for `rg` (or the Grep tool / `grep`); if the right section is not obvious, list headings first with `rg '^## ' references/*.md`, then read only the matching range. Do not recite references — apply them to the code at hand.

- `references/principles.md` — depth, information hiding, dependency direction, abstraction discipline. Not stay-together.
- `references/red-flags.md` — suspected surface/leakage/cosplay problems; skip change-axis ownership flags.
- `references/examples.md` — concrete restructurings when no nearby project pattern is enough.
- `references/language.md` — vocabulary for reports.
- `references/review-report.md` — Mode B candidate format.
- `references/interface-design.md` — Mode C design comparison.
- `references/decision-records.md` — project context before broad recommendations.
