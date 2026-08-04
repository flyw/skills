---
name: double-blind-circuit-breaker
description: Halt execution and enforce active clarification when user input is underspecified and internal confidence is low. Use when facing vague pronouns, missing context, or high hallucination risk.
---

# Double-Blind Circuit Breaker

Bridge the **Articulation Gap** and practice **Epistemic Humility**. Break the cycle of mutual confusion by surfacing the boundaries of your knowledge and forcing explicit user selection before executing state changes.

## Process

### Phase 1: Ambiguity Triage
1. **Assess Input & Confidence**:
   - Evaluate the prompt for missing entities, implicit context, or vague pronouns.
   - Gauge your internal confidence in the target action. If confidence is below 70% and the input is underspecified, trigger the circuit breaker.

### Phase 2: Active Clarification Protocol
1. **Halt Execution**: Stop all mutating tool calls immediately.
2. **State the Void**: Declare exactly what information is missing to proceed (e.g., "I lack the target environment name").
3. **Propose Categorical Options**: Present 2-3 specific, mutually exclusive interpretations of the user's intent.
4. **Declare Default Fallback**: State the safest read-only path you will take if the user confirms none of the options.

> **Completion Criterion**: The user explicitly selects one of the proposed interpretations or provides the exact missing entities required to raise execution confidence above the threshold.
