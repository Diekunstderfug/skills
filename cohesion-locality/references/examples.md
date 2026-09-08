# Optional boundary examples

Consult a matching example only when it clarifies an uncertain distinction. These sketches illustrate reasoning, not a recommended stack or a fixed answer for similar-looking code. They are not default reading. Evaluation fixtures and answer criteria remain separate in `../evals/`.

- [Responsibility sentences](#responsibility-sentences)
- [Orchestration](#orchestration)
- [Package organization](#package-organization)
- [Provider change axes](#provider-change-axes)
- [State copies](#state-copies)
- [Task ownership](#task-ownership)
- [Same name and different meaning](#same-name-and-different-meaning)
- [Synchronization ownership](#synchronization-ownership)
- [Failure localization](#failure-localization)

## Responsibility sentences

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


## Orchestration

A cohesive orchestration shape:

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

This can be cohesive even though several operations occur. The sketch illustrates delegation, not a required validator/repository/event-bus stack; transaction and delivery guarantees still need to match the actual contract.

A shape worth inspecting when unrelated implementation knowledge has accumulated:

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

If these details have independently owned contracts and create maintenance friction, the concern is their mixed ownership rather than length. A small direct implementation may still be appropriate; the comments alone do not prove that extraction would help.

## Package organization

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

## Provider change axes

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

These changes can belong to one provider contract. Contrast them with unrelated routing or billing policy; the number of possible changes alone does not determine cohesion.

## State copies

```python
class Cart:
    def __init__(self):
        self.items = []
        self.item_count = 0

    def remove(self, item):
        self.items.remove(item)  # item_count now disagrees
```

If count means the current list length, deriving it or centralizing both updates removes an avoidable consistency obligation. Contrast a receipt that captures purchase-time prices: updating that snapshot whenever the catalog changes would violate its purpose. A cache can also retain a copy when its owner and invalidation policy are clear.

## Task ownership

```python
def open_screen(poller):
    poller.start()  # inspect who keeps the handle and stops it
```

This fragment raises a question, not a verified leak. If the screen owns the work but discards the handle and performs no cleanup, investigate its lifecycle. If an application supervisor owns the poller, observes failure, and stops it at shutdown, a longer lifetime may be intentional. The goal is explicit ownership, not moving all task creation into the UI.

## Same name and different meaning

A sales customer's status may mean prospect/active/lapsed; a support customer's status may mean open/escalated/resolved. One shared `status` field could couple different meanings despite a shared customer identifier. Separate contextual models may help; sharing the identifier or an actually common contract can still be correct. Different team names alone would not establish this distinction.

## Synchronization ownership

```python
with account.lock:
    if account.balance >= amount:
        account.balance -= amount
```

Extracting the check and debit into helpers can preserve this protected operation. Making each helper acquire and release the lock separately may allow the balance to change between them. Judge the actual atomicity contract, not helper count. An actor or transaction may provide the protection instead of this lock.

## Failure localization

```text
request → validation → domain operation → persistence → external adapter
```

This is a possible diagnostic path, not a required architecture or execution order. At relevant checkpoints, understandable inputs and outputs help locate the responsible area without loading unrelated details. These checkpoints can remain within one cohesive unit; creating a file for every step would not itself improve failure locality.
