---
name: agent-ticket-planner
description: Decompose a large or failure-prone codebase change into an aligned specification and ordered, low-context agent tickets. Use when implementation will be delegated one checklist at a time or a previous plan overloaded its executors.
---

# Agent Ticket Planner

Create planning artifacts only:

```text
Inspection → Alignment gate → Behavior graph → Load gate → Ticket contract → Plan audit
```

Use four rules throughout:

- **One-question rule:** one ticket answers one behavior question through one production seam.
- **Untrusted-start rule:** dirty or agent-written work is input to verify, never completion evidence.
- **Real-interface rule:** tests drive the highest available production interface.
- **Fresh-evidence rule:** behavior claims come from the current code, configuration, and run.

Use one status protocol in `README.md` and every ticket:

```text
ready-for-agent → in-progress → ready-for-verification → completed
                         ↘ incomplete
                         ↘ awaiting-user-verification
                         ↘ blocked
```

Only an independent verifier or the user sets `completed`. Only `completed` unlocks the next
ticket.

## 1. Inspection

Read repository instructions, domain and architecture context, affected product paths,
configuration, tests, issue conventions, qualification assets, and working-tree status.

Create an inspection table mapping every changed behavior to:

- producer and consumer seams;
- preserved interface, lifecycle, format, and performance contracts;
- dirty or partial implementation paths;
- test surface and evidence source;
- host, build, device, and external-operation constraints.

For a C++ type/contract change, also map every direct reader, writer, aggregate initializer,
copy/move use, and build target. A contract change is not isolated merely because its header is
the only intended edit.

Classify evidence as tracked, untracked, missing, stale, or fresh.

Use the repository tracker convention. Otherwise use:

```text
.scratch/<initiative>/
├── spec.md
├── README.md
├── artifacts/
└── issues/
```

**Complete when:** every changed behavior has a complete row in the inspection table and every
dirty path, qualification asset, and operational constraint is assigned to at least one row.

## 2. Alignment gate

Report:

- global objective and terminal KPI;
- changed behavior;
- preserved behavior and interfaces;
- deterministic boundaries and tie-breaks;
- non-goals;
- ordered behavior slices.

Ask only questions that change the design and provide a recommended default. Apply corrections
to the report and any repository memory file that owns the terminology.

Hold planning-file creation until the user confirms every item above. Reopen the gate after a
correction.

**Complete when:** the user has explicitly confirmed the current alignment report.

## 3. Behavior graph

Give one owner to every contract, producer, composition seam, lifecycle transition, ownership
rule, downstream invariant, policy cutover, integration boundary, qualification stage, and
device/performance acceptance stage.

Separate contract, implementation, connection, replay qualification, and device acceptance when
they can fail independently. Add a baseline only when comparison lacks trustworthy evidence.
Add compatibility behavior only when confirmed or required for a safe cutover.

**Complete when:** the graph is acyclic, every observable behavior and artifact has one owner,
and every node consumes only outputs owned by earlier nodes.

## 4. Load gate

Apply the **One-question rule** for an isolated executor receiving only `spec.md`, one ticket,
and the dependency artifacts named in it.

Split a ticket when it:

- joins separately verifiable outcomes;
- owns multiple independently failing behaviors;
- crosses independent producers, routing, policy, UI, or performance seams;
- needs an interface that an earlier ticket has not created;
- combines host correctness, replay metrics, and device acceptance.

Default load is one production concept, its adjacent implementation files, one test surface, and
one agent session. Treat file count as a warning signal, not a quota. Keep a larger slice only
when splitting would create an artificial seam, and record that reason.

In particular, keep an interface contract and its direct-consumer migration in one atomic Ticket
when splitting them would leave the repository unable to compile. Do not compensate for an
over-narrow Ticket by inviting proxy/template compatibility hacks; instead enlarge the authorized
atomic boundary with an explicit non-algorithmic migration limit.

**Complete when:** each ticket can be executed from only its three declared inputs and a failure
identifies one behavior or seam.

## 5. Ticket contract

Repeat the terminal objective and critical constraints because each executor has isolated context.
Include these eight sections:

### Global objective

State the terminal product KPI.

### Dependencies

Name the preceding ticket or `none`, then list exact source files, interfaces, decisions,
reports, manifests, fixtures, completion evidence, and integrity gates to verify.

### Current subtask

State the behavior question, authorized seam and files, deterministic boundaries, performance
constraints, and dirty-worktree protection. Route adjacent findings to the handoff.

For C++ invariant tickets, state whether the type is immutable, canonical, or merely documented;
list every direct consumer that must migrate; require standard encapsulation over proxy-field
compatibility; and state the exact condition that requires `needs-split`.

### Required outputs

Assign exact source, test, report, manifest, and decision paths; keep one owner per artifact.

### Non-goals

Name adjacent tickets and the work intentionally left for them.

### Definition of Done

Use checkboxes tied to observable evidence at the claimed level. Compilation proves compilation;
unit tests prove their interface; replay and device claims require their own evidence.

### Tests and calibration

Require a **Real-interface** test and **Fresh evidence**. Specify boundary and invalid states,
lifecycle/error cases, integrity gates, same-input differential replay, provenance,
agent-runnable versus user-owned tests, and the effect of `NOT RUN`.

For calibration, change one tuning variable or restore one module per experiment.

Reject evidence substitutes: copied implementation logic, local state simulations, identical
pure-function calls presented as integration, renamed old reports, unexecuted tests presented as
passing, or compile success presented as runtime/UI/KPI success.

For a C++ type invariant, require an adversarial public-API test matrix, not only happy-path
factory tests. Cover aggregate/default construction, primitive assignment, property copy/move
assignment, value copy/move semantics, casts/implicit conversions, and contradictory fields as
applicable. Require actual direct consumers to compile, forbid test-only friends or proxy-field
workarounds unless explicitly justified, and require temporary binaries outside product source
trees. State that normal default construction may be allowed only when it yields the specified
canonical state.

### Handoff

Require recommended status, initial and final dirty paths, changed files, owned artifacts, exact
commands, exit codes, key output, `NOT RUN` tests, applicable KPI results, residual risks, and
adjacent findings. State that the executor leaves the next ticket blocked; the verifier records
the final decision and unlock state.

**Complete when:** all eight sections exist and every DoD item identifies evidence the executor
can obtain or a user-owned test that keeps the ticket incomplete until supplied.

## 6. Plan audit

Mechanically verify:

- required sections and links;
- acyclic dependencies and exact artifact-name matching;
- one owner per behavior and artifact;
- the four rules;
- separation of host, replay, and device evidence;
- identical status vocabulary across `spec.md`, `README.md`, and tickets;
- an explicit verifier gate before every dependency unlock;
- unchanged confirmed scope;
- untouched product code and prior planning directories.

For C++ contract Tickets, also verify that the direct-consumer graph is either fully inside the
authorized files or explicitly deferred before any header tightening begins; that no Ticket asks
for a knowingly non-compiling intermediate state; and that the verifier has an independent
adversarial probe plus mechanical hash/artifact checks.

Deliver links to `spec.md`, `README.md`, and every ticket.

**Complete when:** the audit finds no missing section, broken link, orphan artifact, dependency
mismatch, overloaded ticket, stale completion claim, or evidence-level mismatch.
