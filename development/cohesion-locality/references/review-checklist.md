# Boundary review and exploration

Read the sections useful to a review, open-ended boundary exploration, or a difficult recommendation. Use it when evidence, counterarguments, or recommendation confidence need more structure; routine reviews need not load it. This is an adaptable reasoning guide, not a per-symbol checklist or fixed report template.

- [Working approach](#working-approach): inspection, hypotheses, counterevidence, and conclusions.
- [Evidence and ownership](#evidence-and-ownership): prompts for uncertain ownership.
- [Change and failure probes](#change-and-failure-probes): comparing practical effects.
- [Counterevidence and extraction cost](#counterevidence-and-extraction-cost): challenging a proposed cut.
- [Calibrating the conclusion](#calibrating-the-conclusion): confidence and alternatives.
- [Inspection signals](#inspection-signals): optional triage clues and their limits.
- [Parallel review](#parallel-review): read when delegating a review; independent inspection and main-agent verification.

## Working approach

A useful default is **inspect → hypothesize → challenge → recommend**. Combine, skip, or revisit steps when the task warrants it; this is not a checklist to fill out for every symbol.

### Inspect the relevant context

Start with the unit in question and enough callers, state, tests, and nearby conventions to understand its role. For a diff review, focus on changed responsibilities and affected boundaries rather than auditing every nested function. Follow dependencies when they clarify ownership; expand scope when the evidence points beyond the initial unit.

Look for the knowledge the code owns, not just its nouns or directory names. A short responsibility sentence is a useful starting hypothesis, not proof of cohesion. “User management” can conceal unrelated rules; an orchestrator can legitimately coordinate several operations.

### Form boundary hypotheses

Ask what change would affect this code and what other code would need attention. Current callers, contracts, tests, reported friction, and known requirements are useful anchors. Relevant history can help when readily available, but an exhaustive history search is not a prerequisite.

Hypothetical future requirements are useful probes: label them as such and explore their implications. Distinguish a change scenario from a forecast that the change will happen. A hypothetical alone usually supports an exploration suggestion rather than a demand to refactor.

Consider keeping the unit intact, moving knowledge to an existing owner, reorganizing within a file, joining a fragmented operation, or extracting a new boundary. Follow the promising options; there is no required number of designs.

### Challenge the promising boundary

Use the questions that matter for this case:

- What ties these operations together: shared mutable state, a transaction, an invariant, a resource lifecycle, or one external contract? Shared data types or similar code alone are weaker evidence.
- Are there independently owned rules or callers whose needs already diverge? Conversely, would splitting force them to coordinate state, sequencing, or error handling across more boundaries?
- Simulate one plausible change: which symbols would be edited, and which unrelated details would still need to be understood before and after the proposal?
- Simulate a failure when useful: can its owner be identified more locally, or has the proposal merely added navigation hops?
- Would a local rearrangement deliver the same benefit? Does the extraction hide meaningful knowledge, or just move lines?

Distinguish conceptual ownership, file organization, and runtime consistency. Different policies may have different owners while participating in one atomic operation. Separate files need not mean separate transactions or services.

If the counterevidence defeats the proposal, keeping the current structure is a useful result. If evidence is incomplete, explain what would change the judgment and continue whatever analysis remains useful.

### Recommend at the appropriate confidence

Lead with the most useful conclusion. For a material finding, connect the relevant location or symbols, the evidence, the maintenance or correctness mechanism, and the smallest useful adjustment. Include the main tradeoff or condition when it could change the decision. A short paragraph can carry all of this; a fixed report template is unnecessary.

Distinguish observed facts, inferences, and exploratory suggestions. Optional priority labels mean:

- **Required:** a demonstrated correctness risk or violation of a known contract or applicable hard project rule. Explain the consequence; a structural preference alone is insufficient.
- **Recommended:** evidence supports a meaningful improvement in maintenance or locality, with reasonable cost.
- **Explore:** a promising hypothesis or alternative whose assumptions still need validation. Especially useful when the user asks for open-ended design work.

Report priority and confidence separately when uncertainty matters. Avoid repeating the same finding in a second recommendations list unless an execution order adds value. When there is no material issue, say so; useful explorations can still follow without becoming invented defects.


## Evidence and ownership

- Which concrete symbol implements the rule? Who calls it, determines its meaning, and can change the contract?
- Does the code share a meaningful invariant, or merely an entity name and data shape?
- Do tests express one behavior contract or unrelated policies? Test layout itself is not proof of the right boundary.
- Does reported change history support the hypothesis? Mechanical edits, renames, and repository-wide formatting can create misleading co-change.

## Change and failure probes

Pick a scenario that helps discriminate between competing boundaries. A known requirement gives stronger support for action; a hypothetical can still reveal a tradeoff.

Trace the affected symbols and the unrelated knowledge a maintainer must load. Compare that path with the proposed organization. A change touching several files is not inherently bad: contracts may legitimately have multiple representations. Look for repeated ownership of one decision or coordination that adds avoidable risk.

For failures, consider whether the new boundary identifies the responsible concept more clearly. More logging stages or more files do not by themselves improve failure locality.

## Counterevidence and extraction cost

- Would moving code separate state from its update/consistency owner, a lock from protected state, cleanup from a task or resource owner, or writes from their transaction?
- Are copies intentional snapshots/caches, or conflicting writable truths? Is a longer-lived task supervised elsewhere? These distinctions can defeat an apparent defect.
- Can conceptual separation happen inside the existing atomic operation?
- Would the caller now need internal sequencing, extra mutable state, or knowledge previously hidden?
- Does a thin adapter protect a real stable contract? Would removing it expose volatile details to callers?
- Would joining similar functions couple policies with different owners or requirements?
- Is a new file useful, or would moving a helper beside its owner solve the problem?

## Calibrating the conclusion

A useful recommendation survives the most relevant counterargument. Explain the remaining uncertainty when it changes priority or scope. There is no need to manufacture competing designs or numerical cohesion scores.

Compare the practical options: keep, move, join, or split. These are possible outcomes, not a required four-way exercise. For open-ended exploration, prioritize ideas that would teach the user something useful even if they are not ready for implementation.

## Inspection signals

Long functions, many branches/local variables/arguments/public methods, generic names, disjoint injected dependencies, unrelated side effects, independently meaningful comment-delimited blocks, and little interaction between method groups can help select code to inspect. Mixing domain, database, HTTP, serialization, and telemetry details or scattering one change across unrelated files can also reveal ownership questions.

Static-analysis complexity measures can surface candidates; they do not establish a defect or a useful cut. Prefer semantic evidence over line/method/parameter thresholds, complexity scores, or generic SOLID/small-function preferences unless an applicable project rule explicitly requires otherwise. A large parameter list may express one cohesive contract; many branches may belong to one algorithm.

## Parallel review

Use this branch for delegated reviews, including review within a larger authorized task. Review subagents inspect and report without editing the target code; the main retains the user's original authorization for any subsequent implementation. Use the host's available subagent tools. When they are unavailable or delegation would duplicate tightly coupled work, the main reviews directly and states any remaining coverage limits. External reviewer processes require an explicit user request; do not build a runner or start nested model CLIs merely to obtain parallelism.

### Main: define the scope and dispatch

Read the applicable project skills and authoritative rules before assigning work. Give a required domain specialist its own fresh-context assignment alongside structural reviewers; for example, a project's medical safety skill can own one medical review covering all its dimensions. Reuse that assignment across this suite. Send only the relevant task, contracts, and exact rule/skill paths rather than the full conversation; reviewers independently read the applicable source files. Keep payloads and reports within project privacy rules.

Resolve the repository, relevant paths, and review revision once. For a diff, provide the actual base and target revisions; for uncommitted work, use a captured snapshot or record changes so results can be checked against the same input. Assign cohesive areas or concrete boundary questions, with needed callers and contracts available. All reviewers apply the complete principles; do not divide ownership, state, and lifecycle into isolated principle-specific reviewers.

Send each reviewer the task kind, exact scope, applicable project instructions, known contracts and accepted decisions, and the exact skill location. Require a full read of the entrypoint, with references only as needed. Use fresh contexts and withhold tentative main/peer findings on the first pass. Supply established user constraints without disguising hypotheses as facts. Allow related-code inspection beyond the assigned directory and require reviewers to report what they actually covered. Launch independent assignments together; the main can inspect cross-area relationships while they run. Reviewers return results to the same main and do not delegate recursively.

### Reviewer: return evidence, not a verdict quota

For each material finding, give the relevant symbols and file/line locations, the code or contract evidence, the ownership/invariant issue and its practical consequence, the smallest useful change, and the strongest counterevidence or unresolved assumption. Keep recommendation strength separate from confidence; a maintenance suggestion is not automatically a correctness defect. Short structured prose is sufficient. No findings is a valid outcome; include inspected scope and any unresolved or uninspected areas. Claims about protection elsewhere or test coverage need the actual handling code or named test, not a search miss or a guess.

### Main: verify and synthesize

Account for every assignment before closing the review. For failed, timed-out, or unusable output, recover it, inspect the gap directly, or report the missing coverage; none of those states means no findings. Retain source attribution and inspected scope. Merge duplicates by underlying rule or invariant and affected symbols, not line number alone. Repeated agreement is not additional evidence by itself and does not automatically raise confidence.

Read the motivating code, relevant callers, and contract evidence before promoting a finding. Test the strongest counterargument, including intentional snapshots, compatibility boundaries, or preserved atomicity. Resolve reviewer disagreements against that evidence; keep unsupported claims as conditional exploration or open questions. If the reviewed code changed, recheck affected findings and report any stale coverage.

Check relationships across assignments: shared state, transaction boundaries, work/cleanup lifetimes, and duplicated rule ownership. A focused follow-up reviewer can investigate a concrete gap and receive the earlier findings explicitly as follow-up context; another full pass is not mandatory. Finish with one coherent conclusion, distinguishing demonstrated violations, maintenance improvements, exploratory ideas, and coverage limits. Do not derive a quality score from finding counts or auto-apply fixes during a review.
