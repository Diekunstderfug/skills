# Ownership and locality

Use the section that answers the live ownership question. These criteria support boundary decisions; API shape, dependency direction, and surface design remain complementary work for `modularity-review`. No section requires another file to reach a useful judgment.

- [Rules and meaning](#rules-and-meaning): change authority, contracts, semantic differences.
- [State and consistency](#state-and-consistency): authoritative state, derived values, copies.
- [Work and resource lifetimes](#work-and-resource-lifetimes): tasks, subscriptions, cancellation, cleanup.
- [Shared state and synchronization](#shared-state-and-synchronization): protection and atomicity.
- [Change and failure locality](#change-and-failure-locality): evaluate a proposed boundary.
- [Boundary cost](#boundary-cost): compare separation with coordination.

## Rules and meaning

Prefer placing a rule's interpretation near its conceptual owner. Protocol details often belong near the external client, persistence knowledge near its query operation, serialization near its contract, and provider-specific retry behavior near that provider. These are possible homes, not required layers or classes.

To clarify a reason to change, ask **who or what determines the rule**: a business policy owner, external specification, or product requirement. Independently governed rules may deserve independent homes even when they use the same data. Team names and org charts are evidence, not instructions to split by department. This adapts the change-authority lens from [Robert C. Martin's SRP explanation](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html).

Before joining same-named concepts, compare their meaning, identity, valid states, units, and governing rules. Different contexts can legitimately model the same real-world entity differently. Conversely, different names need not imply different contracts. Semantic separation does not itself require DDD infrastructure, services, or a mapping layer. Source: [Fowler on Bounded Context](https://martinfowler.com/bliki/BoundedContext.html).

Co-locating behavior with the knowledge it uses can improve cohesion. Evaluate that benefit against other constraints; responsible queries and data transformations can still be appropriate. Avoid translating this into a ban on getters or a requirement to move every calculation into an object. Source: [Fowler on Tell-Don't-Ask](https://martinfowler.com/bliki/TellDontAsk.html).

## State and consistency

For state involved in the decision, identify its authoritative owner, allowed writers, derived values, and required consistency. If a value can be derived cheaply and reliably, consider computing it rather than maintaining another mutable copy. If fields must transition together to preserve a contract, examine whether their representation and update ownership prevent contradictory states.

Copies are not automatically defects. Caches, historical snapshots, drafts, replicas, and materialized views can have distinct purposes. Ask who refreshes or invalidates them, what staleness is allowed, and whether changes are meant to propagate. A snapshot that intentionally stops following its source differs from a stale live copy.

Shared ownership may be valid with an explicit coordination protocol; an authoritative source does not imply a global singleton. The issue is unclear synchronization responsibility, not the mere existence of multiple representations. This generalizes the state-structure questions in [React's official guidance](https://react.dev/learn/choosing-the-state-structure); React-specific storage choices are not universal prescriptions.

## Work and resource lifetimes

For a task, subscription, timer, handle, or stream, ask who starts it, needs its result, observes failure, and ends or releases it. Ownership is clearer when the lifetime matches the activity that needs the work and cleanup remains associated with that owner.

A task may legitimately outlive its caller: application services, supervisors, or durable job systems can own longer work. Look for an explicit transfer of responsibility rather than requiring every child task to end with a function call. Request- or screen-scoped work deserves inspection if it continues after its owner is gone without another owner.

Acquisition, legal states, cancellation, and release can form one cohesive lifecycle despite phase-shaped names. Preserve actual failure and delivery contracts when considering movement. This is an ownership lens inspired by [Kotlin's CoroutineScope documentation](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope/), not a requirement to adopt its APIs or a particular concurrency model.

## Shared state and synchronization

Apply when the code actually has concurrency or a synchronization contract. Examine whether protected state, the mechanism guarding it, and operations preserving its invariant have clear shared ownership. Moving state away from its lock, or separating reads and writes that must be atomic, can distribute obligations callers may miss.

Co-location is a useful aid, not a substitute for verifying the relevant protection protocol. Message passing, transactions, immutable snapshots, and other synchronization models can be appropriate; encountering shared data does not automatically call for adding locks. Source: [C++ Core Guidelines CP.50](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rconc-mutex), applied here to ownership rather than a general concurrency audit.

Conceptual, file, and runtime consistency boundaries need not coincide. Different policy owners may participate in one transaction. Preserve required atomicity and resource guarantees when evaluating the proposed separation; flag a concrete violation without expanding every boundary review into a full correctness audit.

## Change and failure locality

Probe a plausible change: which symbols need editing, and what unrelated knowledge must a maintainer load? Prefer known requirements when available; hypothetical scenarios can expose tradeoffs if labeled as such. Multiple possible changes do not alone prove multiple responsibilities.

Candidate axes include domain policy, storage, transport, schema mapping, configuration, retry, authentication/authorization, telemetry, presentation, and SDK behavior. Check whether these are separately governed contracts or aspects of one contract; they are not a layer checklist.

For a failure, ask whether the responsible conceptual area can be identified without understanding unrelated details. Clear inputs and outputs can support diagnosis without turning every diagnostic stage into its own module. More files and logging stages are not proof of better locality.

A change touching many files can reflect necessary contract representations. Look for duplicated decisions and avoidable coordination rather than file count alone. Co-change history can inform a hypothesis; mechanical rewrites and formatting can create misleading evidence.

## Boundary cost

Compare the practical improvement with new names, imports, interfaces, call indirection, shared state, lifecycle coordination, glue code, and reader context switches. A cohesive unit can hide substantial complexity; a split is useful when its benefit exceeds the coordination it introduces.

Transformations, policies, validation rules, persistence operations, adapters, serialization contracts, side effects, lifecycle transitions, and algorithms can be meaningful extraction targets. A one-use wrapper may protect a real contract, while a reusable-looking abstraction may bind unrelated policies. Keep, move, join, and split are options rather than a required comparison set.

When a concrete contrast would help, consult the matching section of [examples.md](examples.md). The examples are optional and need not be loaded for routine ownership judgments.
