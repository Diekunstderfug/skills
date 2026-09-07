# Review aids

Load this file when running a review pass. The checklist is applied per materially changed function, class, file, or module; the heuristics are warning signals, not automatic violations. Semantic cohesion decides whether refactoring is appropriate — never the signals alone.

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
