---
name: pattern-composition
description: Select, evaluate, and combine design patterns for codebase architecture or refactoring. Use when designing new modules, refactoring complex code, or establishing component architecture.
---

# Pattern Composition

Select, evaluate, and compose software design patterns tailored to codebase context and task demands. Enforce **deep modules**, clean **seams**, and anti-over-engineering guardrails.

## Process

### Phase 1: Context & Demand Analysis

1. **Inspect Code Base & Domain**:
   - Trace current architecture, language-native idioms (OOP, functional, traits, closures), and module boundaries.
   - Identify primary quality drivers: *Concurrency*, *State Complexity*, *Modularity*, *Extensibility*, or *Performance*.

2. **Map Task Requirements**:
   - Frame the problem domain and isolate distinct design challenges (e.g., variable algorithms, multi-step creation, asynchronous notification, state machine).

> **Completion Criterion**: Every core domain constraint and quality driver is mapped to explicit design challenges and confirmed by the user.

### Phase 2: Pattern Selection & Trade-Off Evaluation

1. **Evaluate Candidate Patterns**:
   - **Creational**: Defer instantiation mechanics (Factory Method, Abstract Factory, Builder, Prototype, DI, Object Pool).
   - **Structural**: Compose interface boundaries and adapters (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy).
   - **Behavioral**: Encapsulate interaction and execution state (Chain of Resp, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor).
   - **Concurrency / Architecture**: Isolate execution threads and system boundaries (Reactor, Active Object, Producer-Consumer, CQRS, DDD Aggregate/Repository).

2. **Check Language Idioms**:
   - Prefer language-native abstractions (e.g., functions/closures over single-method Strategy classes, traits over deep class hierarchies).

3. **Rate Trade-Offs**:
   - Score candidate patterns across *Simplicity*, *Locality*, *Flexibility*, and *Performance*.

> **Completion Criterion**: Candidate patterns are rated across all four dimensions and language-native alternatives are evaluated before presenting 1–3 complementary patterns to the user.

### Phase 3: Composition & Anti-Over-Engineering Audit

1. **Compose Patterns across Seams**:
   - Define clean **seams** between complementary patterns (e.g., *Factory + Strategy*, *Observer + Command*, *Adapter + Facade*, *Decorator + Composite*).
   - Ensure the combined pattern interface forms a **Deep Module** (simple, intuitive interface hiding rich implementation complexity).

2. **Audit against Over-Engineering**:
   - **YAGNI & Rule of Three**: Reject premature generalization or single-use pattern abstractions.
   - **Eliminate Patternitis**: Eliminate pattern wrappers around straightforward conditional branching.

> **Completion Criterion**: Every interface boundary forms a deep module, seam locations are defined, and YAGNI/Patternitis checks pass with user approval.

### Phase 4: Implementation Blueprint & Vertical Slice Breakdown

1. **Specify Contracts**:
   - Define explicit type definitions, class/interface signatures, and interaction flows.
2. **Break into Vertical Slices**:
   - Break implementation into independent, testable **vertical slices** (covering core logic through integration tests).

> **Completion Criterion**: Complete type/interface signatures and an independent, testable vertical slice breakdown are generated and approved by the user.
