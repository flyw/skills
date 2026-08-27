---
name: show-me
description: Explain the current topic with one small, reviewable visual such as Mermaid, ASCII, a table, a diff, or pseudocode. Use when a visual clarifies structure, flow, state, comparison, or change.
---

# Show Me

Make the current topic easier to understand with a compact, static, copyable visual. Treat the visual as an explanatory artifact: it answers a bounded question and stays within an approved scope.

## 1. Ground the explanation

Before choosing a format:

1. Read the current request and conversation context.
2. When working in a repository, read the applicable `AGENTS.md` and `PROJECT.md`, then inspect only the relevant source, tests, and design documents.
3. Reuse the project's actual terminology, boundaries, and verified facts.
4. Mark illustrative assumptions explicitly. Do not invent data or infer domain constraints merely from a language, framework, or project type.
5. Identify the single question the visual must answer.

**Completion criterion:** the visual goal, relevant sources, known constraints, and unresolved assumptions are clear before a representation is proposed.

## 2. Choose the smallest representation

Route by the relationship the user needs to see:

- **Process, algorithm, or decision path:** pseudocode or a Mermaid flowchart.
- **Calls, events, threads, or time order:** a Mermaid sequence diagram or an ASCII timeline.
- **States and lifecycle transitions:** a Mermaid state diagram or a table.
- **Hierarchy, ownership, modules, or dependencies:** an ASCII tree or a Mermaid graph.
- **Comparisons, parameters, mappings, or constraints:** a Markdown table.
- **Before/after behavior or structure:** a `diff` block.
- **Small buffer, memory, layout, or spatial relationship:** an ASCII sketch.
- **Code shape:** pseudocode, a focused code block, or a diff when the change itself is the point.

Choose one primary representation. Combine formats only when each format answers a different part of the approved question. Prefer a plain code block when diagram syntax would make the relationship harder to read.

For domain-specific work, adapt labels to the context. Audio work may involve callbacks, buffers, channels, threads, ownership, and latency; Python work may involve modules, data transformations, shapes, and dependencies. Use those concepts only when the current context establishes that they matter.

## 3. Confirm the visual plan before generating

Before rendering the visual, present a concise plan and wait for explicit user confirmation. The plan is not the visual and must not contain the final diagram.

Use this shape:

```text
### Visual plan · Pending approval

Goal: <the question this visual answers>

Format: <Mermaid / ASCII / table / diff / pseudocode>

In scope:
- <objects, steps, relationships, or details included>

Out of scope:
- <nearby details intentionally excluded>

Sources and assumptions:
- <conversation, project document, source code, or explicit illustrative assumption>

Acceptance check: <what the user should be able to understand or verify>

Reply with: confirm / change the format / change the scope.
```

The plan must name the relevant units, ordering, boundaries, or invariants when they affect interpretation. For example, include sample rate, block size, channel count, thread boundary, or ownership only when the approved topic requires them and the context supplies them.

Wait after presenting the plan. If the user changes the format or scope, revise the plan and wait again. Generate only the approved portion when the user approves a subset. An explicit request to generate immediately is an explicit waiver of this confirmation step.

**Completion criterion:** the format, scope, sources, assumptions, and acceptance check have been approved or explicitly waived before any visual is generated.

## 4. Generate the inline artifact

Generate only the approved static artifact inside the response:

- Mermaid diagrams go in a `mermaid` fenced block.
- ASCII sketches, pseudocode, and code shapes go in a `text` or language-appropriate fenced block.
- Comparisons and mappings use a Markdown table.
- Changes use a `diff` fenced block with enough surrounding context to show ownership and order.

Keep the prose around the artifact brief. Put the artifact next to the one-sentence interpretation it supports. Use real labels from the context, preserve direction and ordering, and label anything illustrative.

The artifact exists in the response; this skill does not create file-based or interactive visualizations.

## 5. Verify and deliver

After generating, check the artifact against its approved plan:

- It answers the stated goal.
- Every in-scope object or relationship needed for that answer is present.
- Out-of-scope detail has not expanded the diagram.
- Direction, ordering, ownership, units, and boundaries are unambiguous where applicable.
- Sources and illustrative assumptions are not mixed together.
- No unsupported facts or fabricated data appear.
- Mermaid and fenced-block syntax is structurally valid.

Report the result with a compact artifact record:

```text
### Visual artifact · Verified

Type: <format>
Goal: <question answered>
Scope: <what is covered>
Sources: <context or documents used>
Assumptions: <none, or clearly marked examples>
Verification: <checks completed>
```

Use the lifecycle `planned → awaiting-confirmation → approved → generated → verified`. If the user requests a material scope or format change after generation, treat the previous artifact as superseded, create a new plan, and obtain confirmation before regenerating.

**Completion criterion:** the delivered artifact is traceable to an approved plan and has passed the relevant structural and scope checks.
