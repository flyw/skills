---
name: loopai
description: Start, inspect, stop, and resume a LoopAI spec-first ticket initiative through its MCP tools and one single-ticket Worker, automatically advancing to the next dependency-ready ticket after each clean completion. Use when the user asks to run LoopAI, execute or resume tickets, poll progress, handle a handoff, or continue after LOOPAI_STATUS.md requests an external action.
---

# LoopAI

Control LoopAI through its registered MCP tools. LoopAI owns one Worker, durable `.loopai/` state,
the ticket frontier, and safe handoff. The parent Codex owns the user conversation, status
interpretation, external actions, and resume decisions. Run one ticket synchronously by default;
use detached execution only when the user explicitly requests background execution or polling.

## Decision boundary

Classify every handoff before asking the user.

Treat a decision as agent-owned when all of these conditions hold:

- It is an objective pass/fail judgment required by the current ticket's Definition of Done.
- Fresh evidence directly answers it, with the command or procedure, exit status, and relevant
  artifact or output available for inspection.
- The user's request and the ticket scope already authorize the check and the in-scope work.
- Accepting it only records a technical result and unlocks the next in-scope ticket; it does not
  create an external side effect or choose product policy.
- It does not involve destructive or irreversible work, credentials, third-party access,
  deployment, financial/legal/security risk, or a product/scope/priority choice.

For an agent-owned decision, perform the requested safe check, record the facts, and resume
LoopAI with a concise factual `answer`. Do not ask the user merely to confirm fresh objective
evidence, and do not claim that the user personally approved it. For example, after a successful
browser replay proves a display value, required controls, and no page error, accept that technical
gate and continue automatically.

Ask the user when the choice changes product behavior, scope, priority, or acceptance criteria;
requires authority that the user alone has; carries meaningful external or irreversible risk; has
ambiguous or insufficient evidence; conflicts with an explicit user instruction; or is explicitly
reserved for user approval. A recommended answer is guidance, not evidence or user consent. When
uncertain, preserve the handoff and ask the user.

## Start or resume

1. Confirm the project and resolve the intended `spec.md`. Prefer an explicitly named spec; for the
   calculator project use `.scratch/calculator-web/spec.md`.
2. Check that the spec exists. If it is missing, report the exact path and stop.
3. Use the MCP server's configured project `cwd`; do not pass an arbitrary directory argument.
4. Start or resume one ticket with the native MCP tool:

   ```text
   mcp__loopai__loopai_run(
     spec=".scratch/calculator-web/spec.md",
     wait=true
   )
   ```

   For an explicitly requested detached/background run, use `wait=false`:

   ```text
   mcp__loopai__loopai_run(
     spec=".scratch/calculator-web/spec.md",
     wait=false
   )
   ```

   For a handoff, include a concise factual answer and keep the default synchronous wait. Use the
   user's exact answer for a user-owned decision, or the verified technical result for an
   agent-owned decision:

   ```text
   mcp__loopai__loopai_run(
     spec=".scratch/calculator-web/spec.md",
     answer="<concise factual answer>",
     wait=true
   )
   ```

Use `wait=true` for the normal workflow. It waits for one resumable single-ticket turn to reach a
terminal orchestration result. When that result is `initiative.ticket-completed`, immediately call
`loopai_run` again without an answer to start the next dependency-ready ticket; repeat this
advancement loop until the initiative completes or LoopAI produces a handoff, stop, or error. This
does not bypass a handoff or other user decision. Use `wait=false` only when the user explicitly
requests detached/background execution, manual polling, or an immediate return. The MCP tool also
defaults to `wait=true` for compatibility with older callers.

## Automatic advancement

Treat `initiative.ticket-completed` as a clean persisted boundary, not a request to return control
to the user. In the synchronous workflow, invoke the next `loopai_run(spec=..., wait=true)` with no
`answer` immediately and continue until a terminal result other than `ticket-completed` appears.
This automatically starts the next dependency-ready ticket while preserving the one-Worker rule.

For a detached workflow, poll with `loopai_status`. When it reports `ticket-completed` and no stop
was requested, invoke `loopai_run(spec=..., wait=false)` without an answer to launch the next ticket,
then resume polling. Never launch another Worker while status is `starting` or `running`.

Stop automatic advancement when status is `stopped`, `error`, `interrupted`, `already-running`,
`accepted`, or `starting`; inspect the returned state and follow the corresponding recovery path.
For `handoff`, read the status and apply the Decision boundary. Resume immediately when the
handoff is agent-owned; pause for the user only when it is user-owned.

## Interpret start results

- `initiative.accepted`: one detached Worker has been accepted. This is expected for an explicit
  `wait=false` request; report its `worker_pid` and tell the user to poll `loopai_status`. If a
  synchronous call unexpectedly returns `accepted` or `starting`, report the PID and poll status;
  do not launch another Worker.
- `initiative.already-running`: do not start another Worker. Report the current PID and state.
- `initiative.already-completed`: report that the initiative is complete.
- `initiative.error`: report the exact error and stop; do not retry blindly.

LoopAI permits only one Worker for the project. Its atomic `.loopai/worker.lock` is the source of
single-instance protection; there is no public job id or task queue.

## Poll status

When the user asks for progress, or re-invokes this skill after a background start, call:

```text
mcp__loopai__loopai_status(
  spec=".scratch/calculator-web/spec.md"
)
```

Use the returned `status`, `lifecycle`, `phase`, `worker_pid`, `current_ticket_id`, `completed`,
`total`, `last_event`, `summary`, `heartbeat_at`, `stop_requested`, and `last_result` as the source
of truth. Treat `phase` as a safe checkpoint (`coordinator`, `executor`, `verifier`, or
`waiting-input`), not as a live model transcript.

- `starting`, `running`: report the current phase and heartbeat; do not call `loopai_run` again.
- `stop_requested`: report that graceful stopping is pending; do not launch another Worker.
- `ticket-completed`: report the completed ticket and evidence, then automatically call
  `loopai_run` without an answer to start the next dependency-ready ticket. Continue this loop until
  the initiative completes or another terminal state requires attention.
- `handoff` or `stopped`: read `LOOPAI_STATUS.md` and the referenced ticket/tracker files before
  deciding what to do. For a handoff, apply the Decision boundary; an objective technical gate
  may be resolved and resumed automatically, while a user-owned decision must remain a handoff.
- `completed`: report final completion and the persisted summary.
- `error`: report the cause and inspect the log before retrying.
- `interrupted`: inspect the runtime snapshot, repository, and `.loopai/worker.log` before resuming.

The `heartbeat_at` field shows whether the detached Worker is still making runtime updates. The
Worker log is diagnostic evidence; `runtime.json`, the durable tracker, and `LOOPAI_STATUS.md` are
authoritative state.

## Stop safely

If the user asks to stop, or status shows that execution has diverged from the ticket scope, call:

```text
mcp__loopai__loopai_stop(
  spec=".scratch/calculator-web/spec.md",
  reason="<specific reason>"
)
```

This writes `.loopai/control.json`. The current Codex call is allowed to reach a safe orchestration
boundary; LoopAI then persists a handoff, releases the Worker lock, and stops. Do not kill the MCP
server or the Codex child process. Poll `loopai_status` until the Worker reaches `stopped` or
`handoff`.

## Handle handoffs and resume

Read `LOOPAI_STATUS.md` before responding to a handoff and inspect every referenced ticket,
tracker, and evidence artifact. Perform only the requested safe external action. Then apply the
Decision boundary:

- For an agent-owned technical decision, verify the evidence, write a concise factual answer, and
  resume immediately with `wait=true`.
- For a user-owned decision, explain the evidence and the exact choice required, then ask the user
  in the parent conversation. Do not invent user consent or silently choose a product, risk, or
  authority decision.

For an agent-owned decision, invoke the default synchronous resume immediately with the verified
facts. For a user-owned decision, invoke it after the user supplies an answer, passing that answer
factually and concisely:

```text
mcp__loopai__loopai_run(
  spec=".scratch/calculator-web/spec.md",
  answer="<concise factual result or the user's exact answer>",
  wait=true
)
```

Use `wait=false` on this resume only if the user explicitly requests a detached/background run.

After a clean `initiative.ticket-completed` result, resume without an answer as described in
Automatic advancement; do not wait for another user message merely to unlock the next ticket.

Resume is state-checked: an active Worker returns `initiative.already-running`; handoff, stopped,
and pending-input states require `answer`; a completed initiative is not restarted.

## Safety and evidence

- Keep one Worker per project and never issue a second start while status is active.
- Require LoopAI's persisted verifier/ticket result before claiming completion.
- Let the agent own only objective, fresh, in-scope, low-risk technical acceptance; preserve every
  product, authority, risk, and ambiguity decision for the user.
- Preserve the MCP server's configured `cwd` boundary.
- Do not edit `.loopai/` files manually unless the user explicitly requests recovery and the
  required evidence is available.
- Keep specs, answers, ticket content, and reports free of credentials and other secrets.
