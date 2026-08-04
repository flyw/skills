---
name: human-in-the-loop-feedback
description: Support expert user intervention, intermediate step inspection, and session memory corrections. Use when users provide feedback on prior mistakes or request fine-grained control over Agent reasoning.
---

# Human-In-The-Loop Feedback

Expand the **Johari Window Open Area**. Expose internal reasoning and persist user corrections across session turns.

## Process

### 1. Intermediate Transparency
- Expose Chain-of-Thought (CoT), tool logs, and citations upon user request.
- Provide clear seams for users to adjust intermediate assumptions before long-running execution.

### 2. Correction Persistence
- Extract the root cause gap when a user corrects an output.
- Update session context memory (`session_memory.md`) with explicit user preferences and anti-patterns.
- Incorporate corrections immediately without defensive prose or apologies.

> **Completion Criterion**: User correction is incorporated into current turn execution and persisted to session memory.
