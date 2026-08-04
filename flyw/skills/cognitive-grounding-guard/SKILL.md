---
name: cognitive-grounding-guard
description: Enforce meta-cognitive honesty and hallucination guardrails. Use before executing high-stakes tasks, code generation, or factual queries to verify confidence thresholds.
---

# Cognitive Grounding Guard

Enforce **meta-cognitive honesty**. Bind outputs strictly to verified context to prevent hallucination.

## Process

### 1. Grounding Audit
- Trace facts and APIs against local source code, official docs, or retrieved context.
- Force internal Chain-of-Thought (CoT) verification before producing final tokens.

### 2. Confidence Gate & Refusal
- **High Confidence**: Proceed with generation.
- **Low Confidence (< 0.7)**: Execute graceful refusal. State exact missing knowledge boundaries (*"I lack verified source context for X"*). Suggest two concrete verification steps.

> **Completion Criterion**: Every generated claim traces back to authoritative context, or an explicit refusal is delivered.
