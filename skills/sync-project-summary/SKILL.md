---
name: sync-project-summary
description: Synchronizes conversation context into GEMINI.md (working style rules, max 2 edits) and PROJECT.md (project scope/specs). Use when the user asks to summarize, update, or sync project rules, working styles, or project context.
---

# Sync Project Summary

Synchronizes working style rules into `./GEMINI.md` and project specifications into `./PROJECT.md`.

## Core Scope Boundaries
- **GEMINI.md (Working Contract Only)**: Every conversation automatically loads `GEMINI.md`. Therefore, it MUST ONLY contain agent behavioral constraints, collaboration style rules, coding conventions, and interaction contracts. **Do NOT put project/feature descriptions here.**
- **PROJECT.md (Project Domain & Features)**: Contains domain architecture, tech stack, feature requirements, and project specifications.

## Core Constraints
- **GEMINI.md Hard Cap**: Maximum 2 total working contract edits (additions, modifications, or deletions combined) per invocation.
- **Gatekeeper Protocol**: Zero disk write operations until explicit user approval of the proposed diff.

---

## Process

### Phase 1: Context Extraction & Delta Generation

1. **Extract Context**:
   - **Working Contract (for GEMINI.md)**: User preferences, behavioral guardrails, workflow rules, formatting constraints, or collaboration guidelines. (Exclude feature specs).
   - **Project Specs (for PROJECT.md)**: Architecture decisions, tech stack choices, feature scopes, or domain models.

2. **Inspect Existing Files**:
   - Read `./GEMINI.md` (treat as empty if non-existent).
   - Read `./PROJECT.md` (treat as empty if non-existent).

3. **Prepare Proposed Deltas**:
   - **GEMINI.md**: Identify missing or outdated working style rules. **Enforce Hard Cap**: Select at most **2 items** total (adds + updates + deletes <= 2).
   - **PROJECT.md**: Classify changes into **Tri-Mode Edits**:
     - **Append**: New features, architecture details, or scope additions.
     - **Modify**: Revised requirements or updated explanations.
     - **Delete**: Removed features or deprecated specs.

> **Completion Criterion**: A structured diff proposal is ready, with GEMINI.md changes strictly bounded to <= 2 items and PROJECT.md changes categorized into Append/Modify/Delete.

---

### Phase 2: Gatekeeper Confirmation

Present two distinct interactive questions (via `ask_question` or user prompt) to confirm each file independently:

1. **GEMINI.md Confirmation Question**:
   - Question: "是否保存 GEMINI.md 的工作契约修改？"
   - Options:
     - "(Recommended) 同意并保存 GEMINI.md 的工作契约修改"
     - "暂不保存 GEMINI.md，稍后处理"
   - User write-in option allows specifying custom adjustments for GEMINI.md.

2. **PROJECT.md Confirmation Question**:
   - Question: "是否修改/保存 PROJECT.md 的项目说明？"
   - Options:
     - "(Recommended) 同意并保存 PROJECT.md 的项目说明"
     - "暂不保存 PROJECT.md，稍后处理"
   - User write-in option allows specifying custom adjustments for PROJECT.md.

> **Completion Criterion**: Explicit decisions/feedback received for both GEMINI.md and PROJECT.md before executing any file writes. Stop tool calls if confirmation is pending or if the user requests changes.

---

### Phase 3: Apply & Verify

Upon receiving user approval:

1. **Apply GEMINI.md Edits**: Write/update `./GEMINI.md` with approved working style items.
2. **Apply PROJECT.md Edits**:
   - Append new sections for **Append** items.
   - Replace target sections for **Modify** items.
   - Remove target sections for **Delete** items.
3. **Verify**: Ensure both `./GEMINI.md` and `./PROJECT.md` exist and accurately reflect the approved diff.

> **Completion Criterion**: `./GEMINI.md` and `./PROJECT.md` are persisted to disk and verified matching the user-approved diff.
