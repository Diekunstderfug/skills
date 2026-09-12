# Review Report

The candidate report format for **Mode B** architecture friction scans, plus [parallel review](#parallel-review) guidance for delegated **Mode A/B** reviews. Read that section when delegating; it does not require candidate cards in Mode A. Markdown is the default. HTML is opt-in. Use the vocabulary in `language.md` (public surface, leakage, shallow module, locality, change amplification, recommendation strength).

**When to use candidate cards:**

- Mode B architecture friction scans.
- Broad structure-advice requests.
- When the user explicitly asks for candidates or a top recommendation.

**Do not use candidate cards for ordinary Mode A fast reviews unless the user asks.** A fast review of a file, diff, PR, or small area returns concise findings ordered by risk — not cards.

A report is only as good as its restraint. A "Top recommendation" plus one or two strong candidates beats a long list of speculative ones. Do not pad the report to look thorough, and ground every candidate in the actual code — no generic architecture advice.

## Default: Markdown candidate report

Present candidates ordered by strength, with the single most important action surfaced first.

````md
# Modularity Review

## Top recommendation
[One direct, behavior-preserving action. The single highest-leverage change. If nothing rises to "Strong," say so plainly and explain why the area is fine.]

## Candidate 1: [short title]
**Strength:** Strong | Worth exploring | Speculative
**Files:** `path/one`, `path/two`

**Current friction:**
[What hurts today, grounded in the actual code. Not a generic concern.]

**Why it increases complexity:**
[Name the mechanism using shared vocabulary: change amplification, leakage, shallow module, low locality, reversed dependency.]

**Smallest useful fix:**
[The minimal behavior-preserving change that removes the friction. Not a rewrite.]

**Before**
```txt
[small dependency / call sketch of the current shape]
```

**After**
```txt
[small sketch of the proposed shape]
```

**Testing impact:**
[How tests get simpler, more meaningful, or possible at all.]

**What not to change:**
[Explicit guardrail against over-refactor — the layers/interfaces/abstractions NOT to add.]

## Candidate 2: [short title]
[...same structure...]
````

Guidance:

- Present candidates worth raising; the example is a flexible format, not a quota or required set of fields.
- The before/after sketches are dependency or call-shape sketches, not full diffs. Keep them small enough to read at a glance.
- Include scope guardrails when there is a concrete risk of unnecessary refactoring; omit empty template fields.
- If a candidate depends on a hypothetical future, label the assumption. Give it the depth warranted by the user's requested exploration, without presenting it as a verified defect.

## Optional: HTML report

Use when the user requests HTML output. A broad scan alone does not require an HTML artifact.

Rules:

- Markdown stays the default. HTML is never the default for a normal review.
- Write a single self-contained `.html` file to a temp directory (e.g. `/tmp` or the OS temp dir), **not** into the repo. Report the path.
- Reuse the candidate-card structure above: top recommendation, then cards with strength, files, friction, before/after, testing impact, and what-not-to-change.
- Before/after diagrams can be simple boxes-and-arrows. Do not require Tailwind, Mermaid, or a build step. Inline minimal CSS is enough.
- Do not let visual polish become the work. The findings are the product; the HTML is a wrapper.

Minimal skeleton:

```html
<!doctype html>
<html>
<head><meta charset="utf-8"><title>Modularity Review</title>
<style>
  body{font:16px/1.5 system-ui;margin:2rem auto;max-width:60rem;padding:0 1rem}
  .card{border:1px solid #ddd;border-radius:8px;padding:1rem 1.25rem;margin:1rem 0}
  .strong{color:#1a7f37}.exploring{color:#9a6700}.speculative{color:#6e7781}
  pre{background:#f6f8fa;padding:.75rem;border-radius:6px;overflow:auto}
</style></head>
<body>
  <h1>Modularity Review</h1>
  <section><h2>Top recommendation</h2><p>...</p></section>
  <section class="card">
    <h2>Candidate 1: ...</h2>
    <p><strong class="strong">Strong</strong> · <code>files</code></p>
    <!-- friction, why, smallest fix, before/after, testing impact, what not to change -->
  </section>
</body>
</html>
```

## Parallel review

Use this branch only for delegated review work. Review subagents inspect and report without editing target code; the main retains the original task scope and any authorization for subsequent implementation. Use the host's available subagent tools. When they are unavailable or delegation would duplicate tightly coupled work, the main reviews directly and reports any remaining coverage limits. External reviewer processes require an explicit user request; do not build a runner or start nested model CLIs merely to obtain parallelism.

### Main: scope and independent assignments

Read applicable project skills and authoritative rules before assigning work. Required domain specialists receive their own fresh-context assignment alongside structural reviewers; one medical reviewer, for example, applies all dimensions of the project's medical safety skill. Reuse the same domain assignment across the suite. Send relevant tasks, contracts, and exact rule/skill paths rather than session history; reviewers independently read those source files. Respect project privacy rules in both inputs and reports.

Resolve the repository, paths, and review revision once. Provide actual base and target revisions for diffs, or a captured snapshot/record of uncommitted input changes. Assign cohesive areas or concrete public-contract questions, with relevant callers and dependencies accessible. Avoid assigning disconnected principles to separate reviewers; each reviewer needs the full contract and related knowledge, even across directories.

Give each reviewer the task kind and mode, exact scope, project instructions, known contracts and accepted boundary decisions, and exact skill locations. Require the complete entrypoint and `principles.md`; ownership questions use the complete cohesion-locality entrypoint when available. Other references remain on demand. Use fresh contexts without tentative main/peer findings on the first pass. Reviewers inspect relevant neighboring code, report coverage, and return to the same main without recursive delegation. Launch independent assignments together while the main checks cross-area dependencies.

### Reviewer: findings and coverage

Return file/line locations and symbols, source/contract evidence, the complexity mechanism and practical impact, the smallest useful change, and counterevidence or uncertainty. Keep impact and recommendation strength separate from confidence. A boundary finding can use its own ownership evidence without being forced into an interface score. No findings is acceptable; report inspected scope and unresolved or uninspected areas. Verify claims about handling elsewhere or test coverage against actual code or named tests. Short structured prose is sufficient; no numeric confidence scale or JSON schema is required.

### Main: evidence and one report

Account for all assignments; recover failed, timed-out, or malformed output, inspect the gap directly, or state missing coverage. Missing coverage is distinct from a completed review with no findings. Retain attribution and merge duplicates by underlying mechanism, contract, and affected symbols. Agreement alone does not raise confidence; resolve disagreements by inspecting evidence.

Before including a material finding, read its motivating code, relevant callers, and claimed contracts, and challenge the proposed change with its strongest counterargument. Confirm that a thin interface is redundant before deleting it, and that a proposed seam reduces caller knowledge rather than adding it. Keep unverified claims conditional; recheck affected findings if input changed and identify any stale coverage.

Inspect relationships between assignments: dependency direction, leaked knowledge and error contracts, caller sequencing, shared state, and lifetime/transaction obligations. Consult cohesion-locality when unresolved ownership affects a recommendation. A focused follow-up reviewer may investigate a specific gap with earlier results supplied as follow-up context; another full pass is optional. Produce one Mode A or B report, separating demonstrated defects, supported improvements, exploratory suggestions, and coverage limits. Finding counts are not a quality score, and review findings do not authorize automatic fixes.
