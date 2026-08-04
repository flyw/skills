---
name: project-ideation-alignment
description: Enforce domain knowledge mapping, intent elicitation, and progressive decision navigation before project initiation. Use when exploring unfamiliar domains, ideas are unformed, or execution boundaries must be strictly defined.
---

# Project Ideation Alignment

Clear the **Ideation Fog**. Ground mental models in an unfamiliar domain before producing an **Execution Blueprint**.

## Core Operating Principles
- **Domain-First Orientation**: Transfer domain topology and trade-off axes before requesting technical or architectural choices.
- **Intent Over Specs**: Elicit goals, scope boundaries, and core priorities rather than technical implementation details.
- **Vector-Based Navigation**: Frame choices as explicit trade-off vectors matched to user priorities, rather than prescriptive solution packages.

---

## Process

### Phase 0: Context Discovery
Audit the existing workspace before generating domain maps or questions:
- **Inspect Environment**: Scan project files, configuration, README, or graph tools (`get_architecture`, `list_dir`) to ground the existing tech stack, architecture, and current capabilities.
- **Completion Criterion**: The agent identifies current project constraints and avoids proposing patterns or asking questions that contradict the existing workspace context.

### Phase 1: Domain Orientation
Draw the domain landscape to ground the user's mental model, incorporating the discovered project context:
- **Topology**: Core concepts, domain terminology, and standard paradigms relevant to the current project.
- **Trade-off Axes**: Primary tension vectors (e.g., *Speed vs Scalability*, *Simplicity vs Flexibility*).
- **Completion Criterion**: The user confirms understanding of the domain map or asks targeted clarifying questions.


### Phase 2: Intent & Boundary Elicitation
Ground project parameters across three pillars:
- **Goal**: Target outcome and definition of done.
- **Scope**: Phase 1 essentials vs explicit **Non-Goals** (what will not be built).
- **Key Priorities**: Non-negotiable constraints (e.g., time-to-market, cost, maintainability).
- **Completion Criterion**: User explicitly states or confirms Goal, Non-Goals, and top Priority.

### Phase 3: Progressive Decision Navigation
Break multi-faceted choices into single-axis decision points:
- For each choice, present Option A vs Option B with plain-language trade-offs and priority matching (*"Choose A if priority is X; Choose B if priority is Y"*).
- Ground recommendations strictly in the user's Phase 2 priorities.
- **Completion Criterion**: All critical architectural/functional choice points are resolved.

### Phase 4: Fact-Finding & Research Escalation
- If domain parameters remain uncertain, invoke background research to investigate technical feasibility, standard stacks, or reference implementations.
- Present evidence to resolve remaining ambiguity.
- **Completion Criterion**: No unresolved technical or domain unknowns block blueprint creation.

### Phase 5: Blueprint Ratification
Draft and ratify an exhaustive **Execution Blueprint**:
1. Present a Markdown document specifying:
   - In-Scope deliverables & Non-Goals.
   - Grounded architectural decisions.
   - Step-by-step implementation roadmap.
2. Require explicit user ratification before executing implementation steps.
- **Completion Criterion**: User explicitly ratifies the Execution Blueprint.

