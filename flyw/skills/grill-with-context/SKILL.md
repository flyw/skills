---
name: grill-with-context
description: Interview a plan or design against the active project's AGENTS.md, PROJECT.md, and conversation context, carrying explicit guidance forward and highlighting only unresolved decisions.
disable-model-invocation: true
---

# Grill with Context

Run a repository-aware design interview in the shape of Matt Pocock's `grill-with-docs`: understand the project's language and constraints before questioning, then work through a dependency-aware design tree in rounds. This skill changes how questions are classified and presented; it does not impose a one-question-per-turn limit.

Keep the grilling session read-only. Read project context and report decisions in the conversation. Persist a glossary entry, ADR, or other artifact only when a separate workflow explicitly authorizes that write.

## 1. Establish the context

Before the first round:

1. Determine the active project/worktree root and read every applicable `AGENTS.md` according to the project's instruction-file scope.
2. Read the project's applicable `PROJECT.md`. Follow relevant pointers such as `CONTEXT-MAP.md`, `CONTEXT.md`, ADRs, glossaries, and linked design records; do not load unrelated documents.
3. Read the complete current conversation, including earlier answers, corrections, explicit requirements, and decisions.
4. Build a small evidence ledger with four labels:
   - **Constraint** — a rule, boundary, priority, or non-goal the solution must obey.
   - **Guidance** — an explicit preferred solution or direction.
   - **Decision** — a choice the user has already made or accepted.
   - **Fact** — information that can be established from the repository or tools.
5. Record unresolved, superseded, or conflicting statements separately. The model's own default or recommendation is not evidence from the project.

Facts available from files or tools are for the agent to find. Do not ask the user to repeat them.

**Completion criterion:** every proposed design area is classified as supported by context, constrained but undecided, missing a constraint, or conflicting/stale before the first question round is presented.

## 2. Build the frontier

Map the design as a dependency tree. The **frontier** is every decision whose prerequisites are settled. Present the whole current frontier in one round; independent frontier questions may appear together. Defer a question that depends on another question still open in the same round.

Give every frontier item a recommended answer, then classify it:

### Context-settled

Use this class when an applicable document or the conversation contains clear, current, non-conflicting guidance or a decision. Show the item and its answer for traceability, but do not ask the user to confirm it again.

Use this shape:

```text
✅ **D1 — <decision>**

推荐方案：<answer>

依据：<conversation turn, document, section, or repository fact>

符合约束：
- <constraint and why the recommendation satisfies it>
- <constraint and why the recommendation satisfies it>

状态：上下文已明确，不重复询问。
```

### User decision required

Use this class when the choice is not explicitly settled, even if some constraints are known. Make the missing decision visible and give a recommended answer that satisfies the known constraints.

### Constraint missing

When the conversation and applicable project documents provide no constraint for a material decision, mark the gap at the question itself and focus the question on that missing constraint. Name the exact dimension that is absent, such as compatibility, priority, deadline, risk tolerance, or non-goal; do not hide the gap behind a generic question.

### Conflict or stale guidance

When sources disagree, or an older decision may have been superseded, show the competing guidance and ask the user to resolve that conflict. Do not silently select one source or present a derived preference as an existing decision.

Use this shape for all items that need user input:

```text
⚠️ **Q1 — <question title>**: <question body>

约束状态：<known constraints, or the exact missing constraint/conflict>

重点确认：<the decision the user must make>

➡️ 推荐答案：<recommended answer and why it fits the known context>
```

Every round must make the distinction between **已由上下文确定** and **需要用户重点确认** obvious. A round can contain several user questions when they are independent; the rule is to cover the frontier, not to ask one question per turn.

## 3. Preserve provenance and avoid redundant questions

- Attach a source to every context-settled answer. Cite the file and heading when the source is a document, or identify the relevant earlier user statement when the source is the conversation.
- List the actual constraints satisfied by each recommended solution. Never claim that a recommendation satisfies a constraint that was not found in the context.
- Treat a clear current user decision as authoritative over older guidance, while noting the supersession when it matters.
- Treat a suggestion, example, or the model's previous recommendation as unresolved unless the user or project guidance clearly adopted it.
- After the user answers, add the answer to the ledger and recompute the frontier. Do not re-ask a settled decision unless the user revises it or new evidence creates a material conflict.
- If a source can answer a factual question, investigate it with the available tools instead of turning it into a user question.

**Completion criterion:** each round contains only frontier decisions, every displayed answer has provenance or an explicit unresolved status, and no settled decision is asked again without a stated reason.

## 4. Close the session

Continue round by round until every branch of the design tree has been visited and no material decision remains silently assumed. Then summarize:

- decisions settled by the user or project context;
- constraints and their sources;
- unresolved risks or decisions, if any;
- the recommended next action and its boundary.

Ask whether this summary represents a shared understanding before any implementation or documentation workflow begins. If the user corrects the summary, update the ledger and continue grilling from the changed frontier.

**Completion criterion:** the session ends only after the frontier is empty and the user confirms the shared understanding, or the user explicitly chooses to stop with the remaining decisions listed.
