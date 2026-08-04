---
name: agent-ticket-executor
description: Execute one assigned agent ticket with repository provenance, real-interface tests, and a DoD evidence ledger. Use when an executor must implement exactly one planner ticket and hand it to an independent verifier without self-declaring completion.
---

# Execute Agent Ticket

Apply the one-ticket rule:

```text
Assignment → Snapshot → Dependency gate → Evidence ledger → Scope lock
→ Tracer bullet → Evidence gate → Closure audit → Handoff
```

Use four rules throughout:

- **Snapshot rule:** preserve the exact repository state seen before editing.
- **Evidence-first rule:** decide how each DoD item will be proven before implementation.
- **Real-interface rule:** test through the highest interface that owns the claimed behavior.
- **Fresh-evidence rule:** evidence must identify the current code, configuration, input, and run.

The executor may recommend completion as `ready-for-verification`. Only an independent verifier
or the user may set `completed`.

## 1. Assignment

Resolve and read completely:

- one initiative `spec.md`;
- exactly one assigned ticket;
- the execution map;
- every dependency artifact named by the ticket;
- repository instructions, relevant implementation, configuration, tests, and test instructions.

Ask for the ticket path only when multiple assignments remain plausible.

**Complete when:** one ticket is selected and every authoritative or referenced input has been
read.

## 2. Snapshot

Before editing, record verbatim in the owned handoff artifact:

```text
git rev-parse HEAD
git status --short
git diff --stat HEAD
```

Classify every changed or untracked path as pre-existing user state. If the repository state
changes unexpectedly during execution, record both snapshots and stop when attribution or safe
isolation is uncertain.

**Complete when:** HEAD, initial dirty paths, and initial diff summary are preserved in an exact,
timestamped snapshot.

## 3. Dependency gate

Verify every preceding source, interface, decision, report, manifest, fixture, integrity gate,
and provenance field named by the ticket.

Use `blocked` when a required dependency is absent, stale, malformed, or unusable. Preserve the
acceptance criteria and report the exact gap rather than recreating authoritative inputs.

**Complete when:** every dependency exists, passes its integrity gate, matches expected
provenance, and is usable.

## 4. Evidence ledger

Before implementation, create a table:

| DoD item | Claimed level | Production interface | Required evidence | State |
|---|---|---|---|---|

Use levels such as contract, unit, component, engine, replay, UI, device, and performance.
Compilation proves only compilation; a lower-level test cannot prove a higher-level claim.

For contracts, state machines, lifecycle, routing, or error semantics, also create a state matrix:

| Input/state | Legal? | Expected transition/output | Evidence |
|---|---|---|---|

Classify each applicable category or mark it `N/A` with a reason: null/missing, empty,
minimum/maximum, equality boundary, below/above boundary, non-finite, out-of-range,
stale/generation mismatch, unavailable/warm-up, contradictory fields, lifecycle transition, and
repeated/idempotent input. Declare the real production interface that each test must drive.

When a required test seam is missing, implement it only when authorized by the current ticket.
Otherwise treat the owning dependency as incomplete and return `blocked`; never assign work
retroactively to a completed ticket.

**Complete when:** every DoD item has a proof method and every state category has an expected
result or justified `N/A`.

## 5. Scope lock

Build a working contract covering the global objective, current behavior, preserved contracts,
authorized seams/files, non-goals, deterministic boundaries, and agent- versus user-owned tests.

Keep edits within the ticket and preserve snapshot paths. Route adjacent cleanup, redesign,
migration, tuning, and later-ticket work to the handoff.

Preserve user work and external state: leave reset/checkout/clean/stash, unrelated file moves,
commits, pushes, deployments, installations, hardware operation, and user-owned builds untouched
unless explicitly authorized. Stop when an authorized edit cannot be isolated.

**Complete when:** intended edits map one-to-one to the ticket and can be isolated from the
snapshot.

### C++ invariant gate (when applicable)

Apply this gate whenever a Ticket claims an immutable value object, a canonical invalid state, or
a type-enforced invariant. Prefer ordinary C++ encapsulation: private primitive storage, const
accessors, a private constructor where needed, and an explicit public factory/builder.

Do not invent proxy-field/template tricks merely to retain legacy `object.field` syntax
(`ReadOnlyProperty`, magic-field proxies, implicit conversion wrappers, or similar). Such code is
allowed only when the Ticket explicitly requires it and its copy/move semantics are independently
specified and tested.

Before implementation, trace every direct reader and writer of the changed type. If safe standard
encapsulation requires adapting direct consumers outside the authorized files, stop with
`needs-split` or `incomplete`; do not bypass the conflict with friends or a proxy. A planner must
then either authorize one **atomic contract-and-direct-consumer migration** (so the tree never
intentionally stops compiling) or move the invariant to a seam that can be isolated.

For a type that is meant to reject contradictory states, add an adversarial compile-time matrix
against its actual public API. Cover, when applicable:

| Attack | Required verdict |
|---|---|
| aggregate initialization with contradictory fields | rejected, or explicitly documented as impossible by construction |
| default construction | canonical valid state or explicitly unavailable |
| direct primitive field assignment | rejected |
| property-to-property copy and move assignment | rejected |
| copy/move construction and assignment of the value object | permitted or intentionally deleted, with state preserved |
| casts, implicit conversions, and public test-only/friend seams | cannot bypass the invariant |

Use `static_assert`/`type_traits` and at least one separate negative compilation probe where the
language feature cannot be expressed truthfully with traits. Tests must use the real public
interface; do not add a test-only friend or factory that production callers cannot rely on.

All temporary source and binary outputs go under `/tmp` (or the repository's approved build
directory), never under a product source tree. Record any pre-existing generated artifact but do
not delete it without authorization.

**Complete when:** the chosen representation, every direct caller, and the adversarial matrix are
compatible with the Ticket's authorized atomic boundary.

## 6. Tracer bullet

Implement the smallest behavior satisfying the ticket:

1. establish a failing boundary or real-interface test when behavior is testable;
2. change the smallest production seam;
3. preserve external interfaces unless the ticket changes them;
4. refactor touched code only while meaningful tests remain green.

Share the production seam across real-time and replay when required. Keep real-time work bounded
and reuse preallocated storage. Add compatibility, fallback, configuration, diagnostics, or
abstractions only when the ticket requires them.

**Complete when:** the observable behavior works through the declared interface without
introducing adjacent behavior.

## 7. Evidence gate

Run every authorized runnable test and record its exact command, exit code, result, environment,
and fixture. Update the ledger with direct links to code, tests, reports, or observed evidence.

Apply the **Real-interface rule**:

- exercise the actual state machine instead of a local boolean simulation;
- toggle the actual control interface instead of changing unrelated inputs;
- test production logic instead of copying its loop or formula;
- treat identical pure-function calls as unit evidence, not integration evidence.

For replay, calibration, performance, or device tickets, apply the **Fresh-evidence rule**:
record code state, configuration hash, input hash, parameters, ground truth, and integrity
results. Pass parse, sequence, and completeness gates before interpreting metrics. Change one
tuning variable or restore one module per experiment.

Mark user-owned Gradle, device, credential, or hardware tests `awaiting-user-verification` with an
exact protocol. Mark an unexecuted runnable test `NOT RUN`; it keeps the ticket `incomplete`.

For C++ invariant work, compile both the contract tests and every direct production consumer
identified at the Scope lock. A header-only test does not prove an interface migration is buildable.

**Complete when:** every runnable test has a result, every DoD row has evidence or an explicit
open state, and every behavioral claim matches its evidence level.

## 8. Closure audit

Re-read the original ticket, not the implementation plan or draft summary. For every DoD row,
assign exactly one result:

- `PASS` with evidence;
- `FAIL` with the observed mismatch;
- `NOT RUN` with owner and reason.

Compare final `HEAD`, `git status --short`, and relevant diffs with the Snapshot. Check required
outputs, interface drift, unrelated edits, hidden fallbacks, weak tests, missing provenance,
unbounded real-time work, and consistency between Ticket and handoff.

Also run `git status --ignored --short` and scan authorized source roots for new object files,
executables, and temporary test artifacts. New generated outputs inside a product source tree are
a scope failure unless the Ticket explicitly owns them.

Choose status:

- `ready-for-verification`: every executor-owned DoD is `PASS`;
- `awaiting-user-verification`: only required user-owned tests remain;
- `incomplete`: any runnable evidence is `FAIL` or `NOT RUN`;
- `blocked`: dependency or safe-isolation failure prevents progress.

Keep the next ticket blocked until an independent verifier or user promotes this ticket to
`completed`.

**Complete when:** status follows the ledger mechanically and Ticket, artifacts, and final
repository snapshot agree.

## 9. Handoff

Update only the assigned Ticket and artifacts it owns. Include:

- recommended status and verifier decision still required;
- initial and final repository snapshots;
- changed files and owned artifacts;
- behavior delivered and complete DoD ledger;
- commands, exit codes, results, and `NOT RUN` tests;
- KPI/calibration results with integrity and provenance when owned by the ticket;
- residual risks, adjacent findings, and preserved user paths;
- whether the ticket is ready for verification; never self-unblock the next ticket.

Lead the response with the ticket outcome. Describe the initiative as complete only when its
spec has no remaining work.

**Complete when:** every handoff claim resolves to fresh evidence and an independent verifier can
accept or reject the ticket without relying on the executor's narrative.
