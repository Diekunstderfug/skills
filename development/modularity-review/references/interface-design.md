# Interface Design

Use only after a modularity candidate is selected, or when the user explicitly asks for public API / interface design. Use it only when the decision is nontrivial — a new public surface, a moved boundary, or a genuine choice between shapes. Do not use this to justify creating interfaces. Most candidates need one obvious design, not a design exploration.

The goal is to compare *materially different* shapes and recommend one. If the alternatives differ only cosmetically, you do not need this file — propose the one shape and move on. Never invent an artificial interface to fill out the comparison.

## Process

Explore shapes that differ meaningfully in surface or hidden knowledge. The options below are prompts, not a required set. Speculative options can be useful when labeled with their assumptions; recommend adoption according to current evidence and user goals.

### Design A: Minimal surface
- A small public surface appropriate to the callers; hide sequencing and implementation detail behind them.
- Prefer a boring, direct implementation.
- This is usually the right default.

### Design B: Caller-optimized
- Make the most common caller trivial; keep uncommon cases possible but not dominant.
- Optimize the surface for how the code is actually called today, not all callers equally.

### Design C: Extension-friendly
- Most useful when real variations exist or an explicit requirement motivates extensibility. Hypothetical variants can support exploration, with their cost made clear.
- Avoid speculative extension points. One variation is not a reason.

### Design D: Seam / adapters
Useful reasons to consider this shape include:
- Multiple implementations already exist.
- A seam would materially reduce brittle setup, nondeterminism, or coupling in tests.
- An external dependency's coupling is actively hurting the code.
- The public API is leaking implementation details that a seam would contain.

A single implementation with no testing pain does not justify this design.

## Output

For useful alternatives, explain the relevant parts of:

1. **Public surface** — the exact functions/types a caller sees.
2. **Example caller code** — the smallest realistic call site.
3. **What the implementation hides** — the decisions kept off the surface.
4. **Testing strategy** — what becomes testable and how.
5. **Tradeoffs** — what this shape costs.
6. **Why this might be wrong** — the honest failure mode.

Recommend a shape when the evidence supports it, explaining the decisive tradeoff. If a missing fact would change the choice, identify it instead of forcing certainty.

## Guardrail

Comparing designs is not a license to add abstraction. If, after the comparison, the minimal surface still wins, that is a successful design exploration — not a failure to be "architectural." Carry the chosen candidate's *what not to change* note through to implementation.
