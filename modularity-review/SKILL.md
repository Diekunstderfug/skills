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

Complement, do not duplicate: if the live question is "should these stay together or split?", consult cohesion-locality for that decision, then resume any remaining requested work. Treat unverified cuts as hypotheses until ownership has been examined. When the optional router is installed, follow its handoff and continuation rules in `../module-structure/SKILL.md`.

This skill can run independently; the router is optional. If a complementary skill is unavailable, finish work within this skill's scope, identify any remaining limitation, and do not claim to have invoked the missing skill. Preserve the user's review/design/implementation intent and existing authorization across any continuation.

## Goal

Reduce code complexity without architecture cosplay. Prefer a deep module: small, stable public surface, large hidden payoff, clear dependency direction. Prefer the smallest restructuring that materially improves understanding, change, and testing; consider broader designs when the task warrants them.

## Principles and boundaries

Use these as defaults, adjusting depth and sequence to the user's task. Exploration may compare speculative architectures or broader changes; distinguish those ideas from evidence-backed recommendations for this codebase.

- Inspect relevant code, callers, and conventions to ground findings. When code is unavailable, offer conditional guidance and identify assumptions instead of claiming a verified defect.
- If ownership is unclear, use cohesion-locality when available to test the boundary hypothesis, then continue. A one-sentence responsibility is a clue, not a gate that stops useful work.
- Prefer abstractions that hide meaningful knowledge or relieve coupling and testing pressure. Layers, interfaces, DI, and thin adapters are options whose value depends on their contract and cost, not on implementation count alone.
- Consider moving knowledge to its owner or removing a redundant facade before adding machinery. Prefer a local solution when it solves the problem; broader alternatives are useful when the evidence or requested exploration warrants them.

Respect user scope and applicable hard project rules. Review and design do not authorize implementation or unrelated documentation changes. Preserve behavior and public contracts unless their change is authorized. Existing authorization survives internal continuation. Report evidence and validation honestly.

## Core vocabulary

When terminology matters or you produce a report, use: module, public surface, implementation, depth, shallow module, seam, leakage, change amplification, architecture cosplay, recommendation strength. Definitions in `references/language.md`. Prefer the repo's own word when it has one.

**Responsibility**, **cohesion**, and **change axis** are defined and decided by cohesion-locality. Here uncertainty about them triggers a boundary consultation, not termination of the task.

## Orient the review

Use the following questions as a starting point, not a fixed inspection sequence.

1. For a live split/join decision, start with cohesion-locality when available. Resume after that boundary is decided, preserving the requested review (A/B), design (C), or implementation (D).
2. Inspect first: folder layout, naming, import direction, nearby similar features, test style, public exports, and existing error/validation conventions.
3. For relevant boundaries, consider: What does it own? What should it hide? What is its public surface? Who imports it? What does it import? Can it be tested without booting the whole app? If "what does it own?" has several unrelated answers, consult cohesion-locality and resume with the ownership decision.
4. Read project context when a recommendation is broad or moves code across modules — see `references/decision-records.md`.

Judge complexity by whether future changes get harder: change amplification, cognitive load, unknown unknowns, obscurity. Load `references/red-flags.md` or `references/principles.md` by section — do not recite them. For deeper boundary reasoning, prefer cohesion-locality; brief boundary observations may remain in the same review.

## Mode selection

| Mode | Use when | Output |
| --- | --- | --- |
| **A — Fast review** | Review a file, diff, PR, module, route, component, or small area. | Findings ordered by risk. No candidate cards. |
| **B — Friction scan** | Scan for shallow layers, leakage, reversed deps, or a top recommendation. | Candidate cards + top recommendation. |
| **C — Candidate deepening** | A candidate is chosen, or the user asks to design a public surface. | Owns/hides/surface + design comparison. |
| **D — Implementation** | The user asks the agent to actually refactor. | Smallest behavior-preserving change + validation. |

Default to the smallest mode that fits. Modes chain when the task is broad: B → C → D. After cohesion-locality decides split, join, or keep, resume the mode required by the original request; a review does not become implementation.

### Mode A: Fast modularity review

Inspect the code and report findings ordered by risk. A useful finding connects the following; adapt the format to the task:

- **Impact and confidence** — tie priority to an observed cost, demonstrated risk, or applicable contract. A possible future problem is an exploration hypothesis, not automatically a medium-severity defect. Keep confidence distinct from impact when evidence is incomplete.
- **File/line** if available.
- **Why it increases complexity** — name the mechanism (leakage, shallow module, reversed dependency, architecture cosplay). If the mechanism is mixed change axes or "should this be one unit?", consult cohesion-locality, then include its material boundary finding in the same review without inventing a surface-complexity score.
- **Smallest useful fix** — behavior-preserving; prefer move-to-owner or delete facade.
- **What not to change** — only when there is a real over-refactor risk.

Concise findings are the default. Use another format when requested or when it materially improves the explanation; HTML is opt-in.

### Mode B: Architecture friction scan

Explore the area for surface/leakage/shallow friction, then produce a candidate report using `references/review-report.md`:

- Lead with the most useful conclusion, including when no material change is warranted.
- Usually a few worthwhile candidates, connecting: current friction (grounded in real code), why complexity increases, smallest useful fix, before/after sketch, testing impact, what not to change, and recommendation strength (Strong | Worth exploring | Speculative).

If a candidate's problem is stacked change axes, consult cohesion-locality and carry its material finding into the requested report. Continue assessing other candidates; do not silently drop the boundary issue.

Markdown is the default. HTML is opt-in. If the request ends at a scan, present the recommendation. If it includes further design or implementation, continue within that scope; ask only when a consequential unresolved choice needs user input.

### Mode C: Candidate deepening design

Use after the user selects a candidate, after cohesion-locality has chosen a cut, or when asked to design a public surface. Useful elements, scaled to the decision:

1. What the module **owns**.
2. What it **hides**.
3. The **public surface**.
4. **Example caller code** — the smallest realistic call site.
5. The **tests that should survive** unchanged (the behavior contract).
6. What **not** to refactor.
7. **Materially different alternatives** when they clarify a nontrivial tradeoff; no quota.
8. **A recommendation**, with its reason and any consequential uncertainty.

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

After edits, run project-required checks and validation relevant to the affected behavior and boundaries. Depending on the change, that may include behavior tests, typecheck, lint, or import checks. Inspect the final diff for unintended scope or contract changes. State which checks ran and any validation limits; availability alone is not a reason to run every tool.

## Reference loading

Use progressive disclosure. Reach for `rg` (or the Grep tool / `grep`); if the right section is not obvious, list headings first with `rg '^## ' references/*.md`, then read only the matching range. Do not recite references — apply them to the code at hand.

- `references/principles.md` — depth, information hiding, dependency direction, abstraction discipline. Not stay-together.
- `references/red-flags.md` — suspected surface/leakage/cosplay problems; skip change-axis ownership flags.
- `references/examples.md` — concrete restructurings when no nearby project pattern is enough.
- `references/language.md` — vocabulary for reports.
- `references/review-report.md` — Mode B candidate format.
- `references/interface-design.md` — Mode C design comparison.
- `references/decision-records.md` — project context before broad recommendations.
