---
name: agent-ticket-verifier
description: Independently verify one ready-for-verification agent ticket against its scope, repository state, real-interface tests, and fresh evidence. Use after agent-ticket-executor hands off a ticket and before any dependent ticket is unlocked.
---

# Verify Agent Ticket

Verify; do not implement:

```text
Assignment → Independent snapshot → Scope audit → Evidence replay
→ DoD verdict → State transition
```

Treat the executor handoff as claims to attack, not facts. Read raw code, tests, reports, and
repository state before reading the executor's conclusions. Your job is to find a counterexample
to every claimed invariant, not to confirm the executor's preferred test seam.

## 1. Assignment

Resolve one `spec.md`, one ticket in `ready-for-verification` or
`awaiting-user-verification`, its execution map, dependencies, required outputs, and repository
instructions. Record the expected starting commit or snapshot from the handoff.

Return `blocked` when the assignment is ambiguous or required raw artifacts are missing.

**Complete when:** exactly one ticket and every authority/artifact it names resolve.

## 2. Independent snapshot

Capture:

```text
git rev-parse HEAD
git status --short
git diff --stat HEAD
```

Compare this state with the executor's initial and final snapshots. Classify every path as
pre-existing, executor-owned, verifier-created, or unattributed. Stop on unattributed overlap
that prevents a safe verdict.

For every manifest/hash claim, mechanically recompute the hash and compare the labeled expected
and actual values using a command, not visual inspection. On macOS use `shasum -a 256`; use
`sha256sum` where available. Never describe a final hash as an initial hash, and never infer an
untracked file's pre-execution content from current state.

Run `git status --ignored --short` and inspect authorized product source roots for new `.o`, test
executables, or temporary generated files. A newly created binary/object under a source tree is a
scope violation unless the assigned Ticket explicitly owns that exact path; `/tmp` is preferred
for verifier probes.

An absent initial snapshot cannot be reconstructed from the current workspace or executor prose.
When dirty or untracked paths overlap the ticket and the original snapshot is missing, return
`blocked` because scope attribution is no longer reproducible.

**Complete when:** repository provenance is reproduced from contemporaneous evidence and every
changed path has an owner without inference.

## 3. Scope audit

Reconstruct authorized behavior, seams, outputs, non-goals, preserved contracts, and dependency
boundaries from the ticket. Inspect the actual diff rather than its changed-file list.

Report missing/partial requirements, scope creep, implemented-but-wrong behavior, and interface,
lifecycle, performance, or user-work regressions.

Trace every new normative API statement or invariant back to the ticket or preserved spec.
Explicitly check units, cadence, lifecycle, range, nullability, and boundary language for
conflicts with preserved contracts.

Keep verification read-only. Return failures to the same ticket; create a follow-up only for a
genuinely adjacent finding.

**Complete when:** every changed hunk maps to an authorized requirement or finding, and every
requirement maps to implementation or missing work.

## 4. Evidence replay

Rebuild the DoD ledger from the ticket. Identify each claim's level: contract, compilation, unit,
component, engine, replay, UI, device, or performance.

Run every safe executor-owned command independently. Verify that tests drive the production
interface owning the claim. Reject local state simulations, copied implementation logic,
identical pure-function calls presented as integration, stale/renamed reports, and unexecuted
tests presented as passing.

For reports, match code state, configuration, input, parameters, ground truth, and integrity.
For user-owned tests, validate the protocol and preserve `awaiting-user-verification`.

### Adversarial C++ type audit (when applicable)

When a Ticket claims an immutable type, canonical invalid state, or type-enforced invariant, do
not merely rerun the executor's contract test. Independently create a disposable `/tmp` hacker
probe against the public headers and try to compile a violation. Rebuild the relevant matrix:

- aggregate initialization and default construction;
- primitive field assignment;
- property-to-property copy assignment and move assignment;
- copy/move construction and assignment of the value object;
- casts/implicit conversions and any public test-only or friend seam;
- every direct production reader/writer discovered by repository search.

Use `std::is_constructible`, `std::is_assignable`, `std::is_convertible`, and negative compilation
probes as appropriate. A passing executor test is insufficient if an independently written probe
can construct or mutate a contradictory object. Compile the actual direct consumers as well as the
contract test; a header-only test cannot prove the migration works.

**Complete when:** every claimed PASS is independently reproduced at the claimed level or
converted to FAIL/NOT RUN with evidence.

## 5. DoD verdict

Assign every DoD item exactly one result:

- `PASS`: independently reproduced evidence satisfies the claimed level;
- `FAIL`: behavior or evidence is incorrect;
- `NOT RUN`: required evidence was not executed, with owner and reason.

Check that required outputs resolve, Ticket and handoff agree, state matrices cover every
applicable category or justified `N/A`, and lower-level evidence is not promoted upward.

For a contract, state-machine, lifecycle, routing, or error-semantics ticket, independently build
the state matrix rather than trusting the executor's. Classify or justify `N/A` for:
null/missing, empty, minimum/maximum, equality boundary, below/above boundary, non-finite,
out-of-range, stale/generation mismatch, unavailable/warm-up, contradictory fields, lifecycle
transition, and repeated/idempotent input.

**Complete when:** every DoD item has one verdict, every applicable state category is covered,
and no verdict or scope attribution relies only on executor prose or tests supplied by the
executor.

## 6. State transition

Choose exactly one:

- `completed`: every required DoD is PASS;
- `awaiting-user-verification`: only valid user-owned tests remain;
- `incomplete`: any executor-runnable item is FAIL or NOT RUN;
- `blocked`: verification cannot proceed because authority, original provenance, or isolation is
  missing; never replace missing provenance with a later snapshot.

Update only the assigned ticket, its verification artifact, and execution-map status. Unlock the
next ticket only when this ticket becomes `completed`. Keep product code unchanged.

Record verifier snapshot, commands, exit codes, verdict table, findings, residual risks, and
unlock decision in an owned verification artifact.

**Complete when:** Ticket, verification artifact, and execution map show the same state, and the
decision can be reproduced from raw evidence.
