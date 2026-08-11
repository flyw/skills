---
name: sync-project-summary
description: Synchronize conversation context into GEMINI.md, one source record per conversation under docs/project-records/, and a progressively disclosed PROJECT.md aggregate. Use when the user asks to summarize, update, or sync project rules, working styles, decisions, requirements, progress, or other important project context.
---

# Sync Project Summary

Preserve project context with per-conversation provenance. Store working rules in `./GEMINI.md`, create one detailed source record for each conversation under `./docs/project-records/`, and consolidate the current project view plus links to every record in `./PROJECT.md`.

## File Responsibilities

- **GEMINI.md — working contract only**: Store agent behavior, collaboration preferences, coding conventions, workflow rules, and interaction constraints. Never store project or feature descriptions here.
- **docs/project-records/*.md — conversation source records**: Store all durable, important context from one conversation in one file. Keep conversations separate so future readers can trace where decisions, requirements, and corrections came from.
- **PROJECT.md — project aggregate and disclosure entry point**: Consolidate the current state derived from all conversation records. Include concise topic summaries and links to source records so readers can progressively disclose the underlying details.

Treat the conversation records as provenance sources and `PROJECT.md` as the current cross-conversation synthesis.

## Constraints

- Limit `GEMINI.md` to at most 2 total edits per invocation. Count additions, modifications, and deletions together.
- Perform no disk writes until the user explicitly approves the proposed changes.
- Create exactly one source record for each distinct conversation being synchronized. Never combine separate conversations into one record.
- When this skill is invoked again in the same conversation, update that conversation's existing record instead of creating duplicates.
- Preserve every durable fact that could affect future work, but omit casual conversation, repetition, transient tool output, secrets, and unsupported inference. Do not save a verbatim transcript unless the user explicitly requests one.
- Mark confirmed facts, proposals, superseded decisions, and unresolved questions distinctly.
- Reconcile the aggregate with new information instead of appending contradictions. Keep historical or superseded information in its originating conversation record.
- Ensure `PROJECT.md` represents all important current project knowledge while keeping detailed evidence, rationale, and conversation-specific history in linked records.

## Conversation Record Convention

Store records in `./docs/project-records/` using:

```text
YYYY-MM-DD-HHmm-<short-topic-slug>.md
```

Use the user's local time when known. If the exact time is unavailable or a name already exists, add a stable numeric suffix. Never overwrite a record belonging to another conversation.

Structure each record as follows, omitting empty sections:

```markdown
# <Conversation topic>

- Date: YYYY-MM-DD
- Source: conversation
- Status: active | superseded | completed

## Context and goals
## Requirements and constraints
## Decisions and rationale
## Work completed and current state
## Corrections and superseded information
## Open questions and next steps
```

Record the meaning and provenance of the conversation, not a turn-by-turn transcript.

## Process

### Phase 1: Extract and Classify

1. Extract durable information from the full available conversation:
   - Working-contract rules for `GEMINI.md`.
   - Important conversation context for a new or existing source record.
   - Current project knowledge that must be added to, changed in, or removed from the `PROJECT.md` aggregate.
2. Identify the conversation topic and determine whether a record for this same conversation already exists. Prefer an explicit source marker or filename established earlier in the conversation; do not infer sameness from topic alone.
3. Distinguish confirmed facts from proposals, corrections, superseded decisions, and open questions.

### Phase 2: Inspect Existing State

1. Read `./GEMINI.md` and `./PROJECT.md`; treat missing files as empty.
2. List `./docs/project-records/*.md`; read the records relevant to the topics affected by the current conversation.
3. Read all records only when required to rebuild or verify the full aggregate. Use headings, filenames, and links in `PROJECT.md` for progressive discovery first.
4. Detect conflicts, stale aggregate statements, missing record links, duplicate conversation records, and broken paths or anchors.

### Phase 3: Prepare Proposed Deltas

Prepare a structured proposal before writing:

- **GEMINI.md**: Show at most 2 Add, Modify, or Delete edits.
- **Conversation record**: Show the proposed filename and all important content to save. State whether it is a new file or an update to the current conversation's existing file.
- **PROJECT.md**: Show how the cross-conversation aggregate and record index will change. Classify current-state changes as Add, Modify, or Delete, and identify any superseded statements.

Organize `PROJECT.md` around the project's actual needs. Keep this minimum structure:

```markdown
# Project

One or two sentences orienting a new reader.

## Current project summary

Concise, topic-based synthesis of all current important knowledge. Link claims or topic summaries to the records that provide their context.

## Read as needed

- [Architecture](./docs/project-records/<record>.md#decisions-and-rationale) — read before changing system design.
- [Current implementation state](./docs/project-records/<record>.md#work-completed-and-current-state) — read when resuming implementation.

## Conversation records

- [YYYY-MM-DD — Topic](./docs/project-records/<record>.md) — one-line description of the important contribution.
```

Include every conversation record in the record index. Avoid copying detailed rationale, history, or evidence from the source records into `PROJECT.md`.

### Phase 4: Gatekeeper Confirmation

Ask for explicit approval of two independently selectable change groups:

1. `GEMINI.md` working-contract changes.
2. The coordinated project-context changes: the conversation record and `PROJECT.md`.

Present the exact proposed delta for each group. Allow the user to approve, reject, or revise either group. Do not write any file while a required decision is pending.

### Phase 5: Apply and Verify

After approval:

1. Apply only the approved `GEMINI.md` edits.
2. Create the approved conversation record, or update it only if it belongs to the same conversation.
3. Reconcile `PROJECT.md` into an accurate cross-conversation synthesis and add the record to its index.
4. Verify:
   - The current conversation has exactly one record.
   - All approved important context from this conversation appears in that record.
   - `PROJECT.md` reflects all important current knowledge across records without unnecessary detail duplication.
   - Every conversation record appears in the `PROJECT.md` index.
   - Every relative link and section anchor resolves.
   - No unapproved changes were written.
   - `GEMINI.md` contains only working-contract rules and no more than 2 edits were applied.

Report which files changed, the record created or updated, aggregate statements superseded, and whether all links were verified.
