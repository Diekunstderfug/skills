---
name: cohesion-locality
description: >-
  Designs and reviews code for cohesion, responsibility, and locality:
  keep together what changes together, separate independent change axes,
  prefer cohesive units over small files or tiny functions. Use when
  splitting files or classes, extracting helpers, refactoring, reviewing
  SRP or SOLID, shrinking files, one-class-per-file, or when the user
  mentions cohesion, locality, responsibility boundaries, over-splitting,
  catch-all utils/helpers/common, Manager, or Helper classes. Also use
  when the user asks to evaluate, review, inspect, or audit a unit:
  report material findings and ranked improvement recommendations.
metadata:
  targets: [claude, cursor, codex, agents]
---

# Cohesion, Responsibility, and Locality

Language, runtime, and product domain do not change these rules. Examples below illustrate shape, not a required stack.

Complement, do not duplicate: **this skill owns what stays together**. Interface depth (small surface, large behavior) is a different question.

## Apply

Before extracting, splitting a file, or introducing a class/interface/wrapper:

1. Name the unit's current responsibilities in one short sentence each.
2. Ask: **what future requirement would cause this code to change?**
3. Separate only responsibilities with independent reasons to change.
4. Keep together behavior that shares purpose, knowledge, invariant, or change axis.
5. If the extracted unit would be a one-use pass-through, do not extract.

When the user asks to evaluate, review, inspect, or audit a unit, do both:

1. Report findings that have real maintenance cost. Format: current responsibility → why mixed → proposed boundary → split or not.
2. Give ranked improvement recommendations (next action, not a restatement of the diagnosis). Order: required, then recommended, then consider. Prefer delete leftover facade / move knowledge to its owner over new types, files, or wrappers.

If there are no material findings, say so. Optional consider-level notes come after that, never as fake required work.

Do not require a split because a function is long, a file is large, or a unit has many parameters or methods.

---

Design code for **local understanding, local change, and local failure**.

Prefer cohesive units over merely small units.

> **Keep together what changes together; separate what changes independently.**

A function, class, module, or service should represent one cohesive responsibility, concept, invariant, lifecycle, policy, transformation, adapter boundary, or closely related family of operations.

Do not interpret this as "every function must do only one tiny action."
Do not split code merely to reduce line count.

### Core principles

1. **Optimize for cohesion, not size**

   * Closely related behavior should stay together.
   * Code that operates on the same concept, invariant, state, knowledge, or reason to change usually belongs together.
   * A larger cohesive unit is preferable to several shallow wrappers with no meaningful independent responsibility.

2. **Separate independent reasons to change**

   * If different parts of a unit are likely to change because of unrelated requirements, they should normally be separated.
   * Examples of independent change axes include:

     * business/domain policy
     * persistence/storage
     * transport/API protocol
     * serialization/schema mapping
     * infrastructure configuration
     * retry/backoff behavior
     * authentication/authorization
     * observability/telemetry
     * presentation/formatting
     * external-provider SDK behavior

3. **Design for locality**

   * A change in one responsibility should require understanding as little unrelated code as practical.
   * A failure should be traceable to a reasonably narrow conceptual boundary.
   * Implementation details that are likely to change should be hidden behind the unit that owns that knowledge.
   * Avoid designs where debugging one failure requires reasoning about many unrelated concerns at once.

4. **Preserve abstraction levels**

   * A function should normally work at one main abstraction level.
   * High-level orchestration may coordinate lower-level operations, but should not also implement all of their internal details.
   * Domain decisions should not be interleaved unnecessarily with SQL construction, HTTP details, serialization internals, retry loops, logging plumbing, or other unrelated infrastructure mechanics.

5. **Prefer meaningful boundaries over mechanical decomposition**

   * Extract code when the extracted unit has a recognizable responsibility.
   * Good extraction targets include:

     * a domain policy
     * a transformation
     * a validation rule
     * a persistence operation
     * a protocol adapter
     * a serialization boundary
     * an external side effect
     * a lifecycle transition
     * a reusable algorithm
   * Do not create one-use pass-through helpers merely to make the original function shorter.
   * Do not introduce classes, interfaces, factories, strategies, managers, or wrappers without a concrete responsibility or variation they isolate.

---

## Function design

A function should normally be describable with **one short responsibility sentence**.

Healthy examples:

* "Validate an inbound request."
* "Translate a domain object into an external payload."
* "Persist a task state transition."
* "Calculate a score."
* "Orchestrate record creation."

Investigate a function when its natural description becomes:

* "validate **and** persist **and** serialize **and** send"
* "parse **and** authorize **and** cache"
* "load configuration **and** apply business policy"
* "transform records **and** perform retry handling **and** update database state"

The word **and** is only a heuristic. Several operations may legitimately belong together when they implement one cohesive responsibility.

### A function is likely too broad when

* separate regions have independent reasons to change;
* unrelated groups of local variables or dependencies appear;
* domain logic and infrastructure mechanics are substantially interleaved;
* the function contains several independently meaningful side effects;
* the function name hides substantially more responsibility than it suggests;
* modifying one concern requires understanding unrelated concerns;
* debugging one step requires tracing through unrelated implementation details;
* the function acts as an orchestrator while also implementing the internals of every step.

### Orchestration is allowed

Application services, workflows, command handlers, and use-case functions may coordinate multiple collaborators and still have one responsibility.

Healthy orchestration:

```python
async def create_case(command: CreateCase) -> Case:
    request = validator.validate(command)
    case = case_factory.create(request)
    await repository.save(case)
    await event_bus.publish(CaseCreated(case.id))
    return case
```

Its responsibility is:

> Orchestrate the case-creation use case.

This is cohesive even though several operations occur.

Less desirable:

```python
async def create_case(command):
    # inline validation rules
    ...
    # normalize domain fields
    ...
    # construct SQL
    ...
    # update database
    ...
    # manually construct external JSON
    ...
    # execute HTTP request
    ...
    # implement retry/backoff
    ...
    # update metrics
    ...
```

The issue is not length.
The issue is that several independently changing responsibilities are implemented inside the same unit.

---

## Class design

A class should represent one cohesive concept.

Good class boundaries commonly correspond to:

* domain entity or aggregate behavior;
* lifecycle management;
* repository/persistence boundary;
* adapter to an external system;
* policy or strategy;
* parser or transformer;
* client/provider implementation;
* application use case;
* resource ownership;
* state machine or invariant.

### Investigate a class when

* its public methods naturally divide into unrelated conceptual groups;
* different method groups depend on largely disjoint collaborators or state;
* different method groups would change for unrelated reasons;
* one subset is domain behavior while another subset is infrastructure behavior;
* callers use the class for several unrelated purposes;
* understanding one method requires knowledge of unrelated class responsibilities;
* the class name becomes a vague container such as:

  * `Manager`
  * `Utils`
  * `Helper`
  * `Processor`
  * `Service`
  * `Common`
  * `Misc`
* the generic name is hiding multiple unrelated concepts.

Generic names are not automatically wrong. They are a signal to inspect cohesion.

### Do not split cohesive classes mechanically

A class with many methods can still be well designed if those methods:

* operate on the same concept;
* preserve the same invariant;
* use the same underlying knowledge;
* participate in the same lifecycle;
* change for the same reason.

Method count and line count are **smells**, not architecture rules.

---

## File design

A file should organize code around one domain concept, component, or closely related family of duties.

If the file cannot be described in one sentence, or the sentence needs several unrelated "ands", inspect mixed responsibility. Check that functions, classes, constants, and types in the file serve that same duty. Code gathered only because it was convenient should be re-homed.

Keep in the same file code that is frequently read together, changed together, and shares the same implementation knowledge. Split when parts change independently or sit on different domain or infrastructure boundaries.

Do not mechanically apply "one class per file" or "one function per file".

Catch-all files (`utils.py`, `helpers.py`, `common.py`, `misc.py`, `manager.py`) that keep absorbing unrelated features: assign each symbol to the module that owns it. Keep only tools that are genuinely generic and have no business owner.

Split a file only when the extracted file has a clear name, stable responsibility, or clear ownership. Do not split only to cut line count or add a navigation hop.

Apply the change-locality and failure-locality tests below to the file as a unit: if changing or debugging one duty requires loading unrelated code, the file boundary is likely wrong.

---

## Module and package boundaries

The same rules apply above the file. A package should group files that belong to the same conceptual area.

Prefer:

```text
llm/
├── providers/
├── routing/
├── contracts/
├── structured_output/
└── service.py
```

when these pieces belong to one LLM subsystem but represent distinct internal responsibilities.

Do not create extra packages solely to obtain smaller files. A package boundary should make the system easier to reason about, not merely increase file count. Catch-all packages follow the same rule as catch-all files.

---

## Information ownership

Place knowledge where it belongs.

A component that owns a rule or external contract should normally own the code that interprets it.

Examples:

* External protocol details belong in that system's adapter/client.
* Database persistence details belong in repositories or persistence infrastructure.
* Domain validation belongs with the domain/application boundary that owns the rule.
* Provider-specific API behavior belongs inside the provider implementation.
* Serialization rules belong near the contract they serialize.
* Retry behavior that is specific to an external provider belongs close to that provider rather than leaking across unrelated business logic.

Avoid spreading one implementation decision across many unrelated modules.

If changing one protocol, schema, or policy requires editing many unrelated locations, reconsider the ownership boundary.

---

## Change locality

When reviewing architecture, ask:

> **What future requirement would cause this code to change?**

If one unit has many unrelated answers, its responsibility may be too broad.

For example, if `LLMService` must change because of:

* OpenAI SDK changes;
* provider routing changes;
* retry policy changes;
* structured-output schema changes;
* LangGraph runtime changes;
* billing/accounting changes;
* business workflow changes;

then inspect whether multiple responsibilities have accumulated in one class.

A healthy provider adapter might instead change primarily because of:

* provider API contract;
* provider streaming behavior;
* provider error semantics.

That is a more cohesive change axis.

---

## Failure locality and debuggability

Code boundaries should help narrow failures.

Prefer architectures where debugging can proceed through clear stages:

```text
request
  ↓
validation
  ↓
domain operation
  ↓
persistence
  ↓
external adapter
```

At each boundary, inputs and outputs should be understandable enough to determine whether the fault lies before or after that boundary.

Avoid implementations where a single function or object simultaneously owns enough unrelated behavior that an observed failure could plausibly originate from many independent concerns.

A useful question during review is:

> **If this operation fails, can an engineer identify the responsible conceptual area without understanding unrelated implementation details?**

If not, inspect the responsibility boundaries.

---

## Coupling

Prefer dependencies that follow conceptual ownership.

A cohesive unit may internally contain substantial complexity if it exposes a simple, stable interface.

Do not split a deep, cohesive module into many shallow modules when doing so introduces:

* additional interfaces;
* additional names;
* more call indirection;
* more lifecycle coordination;
* more cross-module state;
* more glue code;
* more context switching for readers.

Complexity hidden behind a good abstraction is often preferable to complexity distributed across many trivial abstractions.

---

## Refactoring rules

When a responsibility boundary is unclear:

1. Identify the unit's current responsibilities.
2. Identify their independent reasons to change.
3. Identify which responsibilities share the same knowledge or state.
4. Separate only the responsibilities that are meaningfully independent.
5. Preserve cohesive operations that naturally belong together.
6. Prefer moving behavior to the component that owns the relevant knowledge.
7. Avoid changing unrelated code during the same refactor.
8. Preserve behavior unless the task explicitly changes behavior.

Do not refactor only to satisfy:

* line-count limits;
* method-count limits;
* complexity metrics;
* generic SOLID rules;
* arbitrary "small function" preferences.

Metrics are signals for review, not automatic design decisions.

---

## Review checklist

For each materially changed function, class, file, or module, ask:

### Responsibility

* Can its responsibility be described clearly in one short sentence?
* Does that sentence describe one concept or several unrelated concepts?

### Cohesion

* Do its operations belong to the same purpose or invariant?
* Do they use related state, knowledge, or collaborators?
* Would they normally change together?

### Change axis

* What requirements could cause this unit to change?
* Are there several independent reasons?

### Abstraction

* Does the code stay at a coherent abstraction level?
* Is orchestration mixed with implementation details?

### Ownership

* Is knowledge implemented by the component that owns it?
* Are protocol, persistence, domain, and infrastructure details located appropriately?

### Locality

* Can this code be modified without loading large amounts of unrelated context?
* Can failures be narrowed to a clear conceptual boundary?

### Extraction quality

* Would an extracted unit have a meaningful name and responsibility?
* Or would the extraction merely create indirection?

### Coupling cost

* Does splitting reduce conceptual coupling?
* Or does it only introduce more interfaces, wrappers, files, and navigation?

---

## Review findings

On evaluate / review / inspect / audit, report material findings **and** ranked recommendations.

Each finding: current responsibility → why mixed → proposed boundary → split or not (required / recommended / consider).

Then **Recommendations**: next concrete edits, ordered required → recommended → consider. Name what to change and what not to add. Prefer deleting leftover facades and moving knowledge to its owner over new types, files, or wrappers. No material findings: say so; consider-level notes come after, never as fake required work.

Do not report stylistic micro-splits, or require a refactor because a function is long, a file is large, or a unit has many parameters or methods. Do not propose abstractions without the responsibility or variation they isolate. Prefer a larger cohesive unit over fragmented indirection.

---

## Practical heuristics

These are warning signals, not automatic violations:

* very long functions;
* many branches;
* many local variables;
* many arguments;
* many public methods;
* generic `Manager` / `Utils` / `Helper` classes;
* several unrelated injected dependencies;
* several unrelated side effects;
* multiple independently meaningful blocks separated by comments;
* one function interacting directly with domain logic, database, HTTP, serialization, and telemetry;
* a class whose method groups barely interact;
* a change requiring edits across many unrelated files.

Static-analysis complexity limits may be used to surface these cases, but semantic cohesion determines whether refactoring is appropriate.

---

## Default decision rule

When deciding whether code belongs together:

> **Prefer cohesive units over merely small units. Keep together behavior that shares the same purpose, knowledge, invariant, or reason to change; separate responsibilities that can change independently. Design boundaries so that changes and failures remain local.**

When these principles conflict with making a function, class, or file smaller, **cohesion and locality take priority over size**.
