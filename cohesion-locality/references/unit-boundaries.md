# Function, class, file, and package boundaries

Read the section matching the unit under review when finer-grained criteria would clarify the judgment. These are adaptable design aids, not mandatory decomposition rules or a preferred framework.

- [Function design](#function-design): responsibilities, abstraction levels, orchestration.
- [Class design](#class-design): state, collaborators, invariants, lifecycle.
- [File design](#file-design): co-location, catch-all helpers, extraction costs.
- [Module and package boundaries](#module-and-package-boundaries): subsystem organization.

## Function design

A function should normally be describable with **one short responsibility sentence**.

A responsibility sentence is a starting hypothesis; inspect independent rules and shared invariants rather than counting verbs.

Prefer a coherent main abstraction level: orchestration coordinates operations while lower-level units own their details. Interleaving policy with SQL, transport, serialization, retry, or telemetry internals is worth examining when it increases unrelated context. This is a reasoning aid, not a requirement to extract every level into a separate function.

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

Coordinating validation, persistence, and notification can be one use case. Inspect whether orchestration also owns unrelated protocol or policy internals, and whether separating those details would improve locality. A small direct implementation can remain appropriate. Transaction and delivery guarantees still need to match the contract.

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

If the file cannot be described in one sentence, or the sentence needs several unrelated "ands", inspect mixed responsibility. Check that functions, classes, constants, and types in the file serve that same duty. Code gathered only for convenience is a candidate to move closer to its owner, if doing so improves navigation or change locality.

Keep in the same file code that is frequently read together, changed together, and shares the same implementation knowledge. Consider splitting when parts change independently or sit on different domain or infrastructure boundaries, weighing the coordination cost.

Do not mechanically apply "one class per file" or "one function per file".

Catch-all files (`utils.py`, `helpers.py`, `common.py`, `misc.py`, `manager.py`) that keep absorbing unrelated features: look for the owner of the affected symbols. Domain-specific knowledge usually fits better near that owner; genuinely generic tools may remain shared. Avoid turning a focused review into an exhaustive reorganization.

Split a file only when the extracted file has a clear name, stable responsibility, or clear ownership. Do not split only to cut line count or add a navigation hop.

For the file as a unit, compare which unrelated details a change or failure forces the reader to understand before and after the proposed cut. Moving lines without reducing that burden offers little benefit.

---

## Module and package boundaries

The same rules apply above the file. A package should group files that belong to the same conceptual area.

Group a subsystem around its conceptual area, with internal divisions when they clarify distinct responsibilities. More packages are useful only when they improve understanding or ownership, not merely to shrink files. Catch-all packages deserve the same ownership questions as catch-all files.

## Optional examples

If the criteria leave the distinction unclear, consult the relevant section of [examples.md](examples.md): responsibility sentences, orchestration, or package organization. Examples are not a prerequisite for applying this reference.
