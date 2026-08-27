---
name: loopai
description: Start, inspect, resume, and advance a LoopAI spec-first ticket initiative through the installed `loopai` command-line tool, one single-ticket turn at a time. Use when the user asks to run LoopAI, execute or resume tickets, inspect progress, handle a handoff, or continue after LOOPAI_STATUS.md requests an external action.
---

# LoopAI

Control LoopAI through the installed `loopai` command-line tool. LoopAI owns the initiative
frontier, durable `.loopai/` state, and one single-ticket turn. The parent Codex owns the user
conversation, status interpretation, external actions, and resume decisions.

The public CLI is a foreground, one-ticket-per-invocation interface. It does not expose MCP tools,
`run`/`status`/`stop`/`resume` subcommands, a `wait=false` option, or a detached Worker
protocol. Do not invent those interfaces.

## Decision boundary

Classify every handoff before asking the user.

Treat a decision as agent-owned when all of these conditions hold:

- It is an objective pass/fail judgment required by the current ticket's Definition of Done.
- Fresh evidence directly answers it, with the command or procedure, exit status, and relevant
  artifact or output available for inspection.
- The user's request and the ticket scope already authorize the check and the in-scope work.
- Accepting it only records a technical result and unlocks the next in-scope ticket; it does not
  create an external side effect or choose product policy.
- It does not involve destructive or irreversible work, credentials, third-party access, deployment,
  financial/legal/security risk, or a product/scope/priority choice.

For an agent-owned decision, perform the requested safe check, record the facts, and resume LoopAI
with a concise factual `--answer`. Do not ask the user merely to confirm fresh objective evidence,
and do not claim that the user personally approved it. For example, after a successful browser
replay proves a display value, required controls, and no page error, accept that technical gate and
continue automatically.

Ask the user when the choice changes product behavior, scope, priority, or acceptance criteria;
requires authority that the user alone has; carries meaningful external or irreversible risk; has
ambiguous or insufficient evidence; conflicts with an explicit user instruction; or is explicitly
reserved for user approval. A recommended answer is guidance, not evidence or user consent. When
uncertain, preserve the handoff and ask the user.

## Start or resume

1. Resolve the intended working directory and `spec.md`. Prefer an explicitly named spec. The
   process working directory is LoopAI's project boundary; the `--spec` path is relative to it
   and must remain inside it. If there is exactly one `spec.md`, `--spec` may be omitted.
2. Check that the spec exists. If it is missing, report the exact path and stop.
3. Check that the command is available with `command -v loopai`. If it is unavailable, report the
   installation/PATH problem and stop.
4. Invoke the command from the target directory. Set the shell tool's `workdir` to that directory;
   do not pass an arbitrary workspace argument:

   ```text
   loopai --json --spec ".scratch/calculator-web/spec.md"
   ```

   Use the same command without `--spec` only when automatic discovery is unambiguous.
5. Use `--json` so stdout is machine-readable JSONL. If the shell tool returns a live session,
   poll that same session until it exits; never launch another LoopAI process while the first one
   is running.

The CLI is synchronous at the process level, but it streams progress while the Coordinator,
Executor, and Verifier work. There is no LoopAI-specific background or polling command.

## CLI parameter reference

The installed CLI currently reports version `0.2.0`. Supported public options are:

- `--help` — show help.
- `--version` — print the CLI version.
- `--spec PATH` — select an initiative spec relative to the process working directory; exactly
  one `spec.md` is auto-discovered when omitted.
- `--model MODEL` — override the model for all three roles.
- `--reasoning-effort LEVEL` — override reasoning effort for all three roles.
- `--coordinator-model MODEL`, `--executor-model MODEL`, `--verifier-model MODEL` — override
  one role's model.
- `--coordinator-reasoning-effort LEVEL`, `--executor-reasoning-effort LEVEL`,
  `--verifier-reasoning-effort LEVEL` — override one role's reasoning effort.
- `--max-rounds N` — limit Executor/Verifier rounds per ticket; default `3`.
- `--max-questions N` — limit Planner question rounds; default `20`.
- `--codex-binary PATH` — select the Codex executable; default `codex`.
- `--automatic-approval` / `--no-automatic-approval` — enable or disable Codex automatic
  approval; enabled by default.
- `--answer TEXT` — provide an outer-agent result for a pending Planner handoff. It is
  repeatable for scripted multi-round handoffs and must not be supplied when no answer is pending.
- `--json` — emit the complete event stream as JSONL instead of readable progress.

The first invocation creates `.loopai/config.toml` in the working directory when it is absent.
Role-specific CLI options override global CLI options, which override that configuration file.
Avoid putting credentials in `--answer`, prompts, or persisted LoopAI files.

## JSONL events and exit codes

With `--json`, every stdout line is a JSON object with `schema_version`, `kind`, `ticket`,
`role`, `round`, and `payload` fields. Important event kinds include:

- `initiative.started`
- `ticket.started`
- `agent.event` — raw Codex JSONL events.
- `agent.stderr`
- `agent.completed`
- `ticket.completed`
- `user.input.required` — a machine-readable request followed by a handoff when no answer
  provider is available.
- `initiative.ticket-completed` — one ticket completed; invoke LoopAI again for the next ticket.
- `initiative.completed`
- `initiative.handoff`

Treat unknown event kinds as forward-compatible progress events. The terminal event is
`initiative.ticket-completed`, `initiative.completed`, or `initiative.handoff`.

| Exit code | Meaning | Outer-agent action |
| --- | --- | --- |
| `0` | One ticket or the whole initiative completed and was persisted. | If the terminal event is `initiative.ticket-completed`, invoke LoopAI again without an answer. Stop when it is `initiative.completed`. |
| `1` | A safe handoff was persisted. | Read `LOOPAI_STATUS.md`, perform the requested safe action, then resume with `--answer`. |
| `2` | Initialization, configuration, or runtime error. | Inspect stderr and the repository state; report or repair the cause. Do not retry blindly. |
| `130` | The foreground process was interrupted. | Inspect durable state and repository changes before deciding whether a resume is safe. |

Exit code `1` is expected workflow control flow, not a process crash.

## Automatic advancement

Treat `initiative.ticket-completed` as a clean persisted boundary, not a request to return
control to the user. Immediately invoke the next turn from the same working directory:

```text
loopai --json --spec ".scratch/calculator-web/spec.md"
```

Repeat without `--answer` until the terminal event is `initiative.completed` or another terminal
state requires attention. Do not start a second process while the prior invocation is still
`starting` or running; the CLI's `.loopai/active.lock` protects the single active turn.

## Handoffs and resume

When the terminal event is `initiative.handoff` or the exit code is `1`:

1. Read `LOOPAI_STATUS.md` in the working directory.
2. Inspect every referenced spec, execution tracker, ticket, repository artifact, and evidence file.
3. Apply the Decision boundary above. Perform only the requested safe external action.
4. Resume with a concise factual result:

   ```text
   loopai --json --spec ".scratch/calculator-web/spec.md" \
     --answer "The external action is complete. Please re-check the repository and continue."
   ```

   Use the user's exact answer for a user-owned decision. For an agent-owned technical decision,
   use the verified result, not a claim that the user approved it.
5. Repeat the normal advancement loop after the resumed turn. If `--answer` was supplied but no
   pending handoff consumed it, treat the resulting error as a real protocol error.

`LOOPAI_STATUS.md` is the fast outer-agent entry point. Detailed state is under
`.loopai/`, including `conversation.json`, `sessions.json`, `execution.json`,
`runtime.json`, and `active.lock`. These files are evidence and state, not a replacement for
the CLI protocol. Do not edit `.loopai/` files manually unless the user explicitly requests
recovery and the required evidence is available.

## Inspecting, background execution, and stopping

The public CLI has no `loopai status`, `loopai stop`, or `loopai resume` commands. Inspect
progress from the live shell session and from the persisted status/state files described above.
There is also no public `wait=false` or detached Worker mode; do not promise MCP-style background
execution or status polling.

If the user explicitly asks to stop a foreground run, interrupt the active shell session through
the host's process-control mechanism. Expect an interrupted process (normally exit code `130`),
not a persisted `operator-stop` handoff. Re-read `LOOPAI_STATUS.md`, `.loopai/runtime.json`,
the execution tracker, and the repository diff before resuming. Do not invent a stop subcommand,
manually modify `.loopai/control.json`, or claim completion after an interruption.

## Safety and evidence

- Keep one LoopAI process per initiative; `.loopai/active.lock` is the single-instance guard.
- Require the persisted verifier/ticket result before claiming a ticket or initiative is complete.
- Automatic approval is enabled by default and permits model-driven Codex changes in the working
  directory. Review the repository, initiative files, and configuration before running; use
  `--no-automatic-approval` when that is the required safety boundary.
- Keep specs, answers, prompts, reports, and logs free of credentials and other secrets.
- Preserve the CLI's process working-directory boundary and do not use a separate workspace flag.
