---
name: query-intent-alignment
description: Active clarification and query expansion when human input is underspecified or vague. Use when a prompt lacks constraints, environment context, or clear boundaries.
---

# Query Intent Alignment

Bridge the **Gulf of Execution**. Align underspecified prompts before executing execution steps.

## Process

### 1. Audit Completeness
Classify prompt intent into binary observable states:
- **Tight**: All parameters (language, target, constraints) defined. Proceed to execution immediately.
- **Underspecified**: Key parameters missing. Halt execution and trigger clarification.

### 2. Active Clarification Protocol
- **Max 2 Questions**: Never ask generic questions ("What do you mean?"). Ask at most two targeted questions.
- **Structured Options**: Provide multi-choice options for missing parameters.
- **State Default**: Declare the default path to execute if the user skips responding.

> **Completion Criterion**: The missing parameters are supplied by the user, or the declared default path is explicitly acknowledged.
