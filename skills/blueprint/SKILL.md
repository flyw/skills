---
name: blueprint
description: Enforce structured alignment and planning before writing or modifying code. Reads context, aligns scope, and selects the right planning tool (/wayfinder, /grill-with-docs, /to-spec, or /to-tickets) before transition to implementation. Use when user requests new code, refactoring, architectural changes, or structured development workflow.
---

# Blueprint

Enforce **Gatekeeping** before writing or modifying code. Direct code generation is held until code context is inspected, scope is aligned, and an issue-tracker spec or ticket set is created.

## Process

### Phase 1: Read & Align

1. **Read Context**:
   - Read relevant core code, configuration files, and architecture documents.
   - Analyze current design patterns, dependency graphs, and potential blast radius.

2. **Align Scope & Boundaries**:
   - Summarize current project state and report understanding to the user.
   - Confirm explicit parameters with the user:
     - **Specific Scope**: Exact limits of modifications.
     - **Core Features**: Key functionality to implement.
     - **Boundary Conditions**: Constraints, edge cases, and non-goals.
     - **Vertical Slicing Requirement**: Decompose requirements into thin, end-to-end functional slices (spanning UI, API, Business Logic, and Data layers per slice) rather than horizontal technical layers. Each slice must be independently runnable, testable, and deliverable.

> **Completion Criterion**: The user explicitly confirms the project understanding, scope, boundary conditions, and vertical slice breakdown.

### Phase 2: Evaluate & Select Tool

Evaluate task scale, ambiguity, and readiness, ensuring chosen strategies adhere to **Vertical Slicing**, then recommend one of the four planning tools:

| Tool | Focus & Scale | Trigger Condition |
| :--- | :--- | :--- |
| `/mattpocock:wayfinder` | Massive / Multi-session | Task exceeds single-session capacity. Requires a shared decision-ticket map of vertical slices to clear obstacles sequentially. |
| `/mattpocock:grill-with-docs` | Ambiguous / High Risk | Technical route or feature scope is vague. Requires relentless grilling to sharpen design and capture ADRs & Glossary terms. |
| `/mattpocock:to-spec` | Clear / Consensus Reached | Requirements are fully aligned through discussion. Synthesizes current conversation into a formal tracker Spec organized by vertical slices. |
| `/mattpocock:to-tickets` | Execution-ready / Defined Plan | Spec or architecture is clear. Requires breakdown into independent, ordered end-to-end tracer-bullet tickets for step-by-step coding. |

Explain the rationale for the selected tool to the user.

> **Completion Criterion**: The user approves the tool recommendation.

### Phase 3: Execute & Transition

1. **Execute Tool**: Run the agreed tool command.
2. **Verify Tracker Artifacts**: Ensure specs or tickets are generated with clear vertical slice boundaries and published to the issue tracker.
3. **Transition to Implementation**: Guide the user to begin coding step-by-step based on the generated frontier ticket.

> **Completion Criterion**: Specs/Tickets are recorded on the tracker, and the user approves starting code execution.
