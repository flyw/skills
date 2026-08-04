# Flyw Skills

A collection of modular AI agent skills for planning, collaboration, architecture, and reliable workflows.

Flyw helps agents turn ambiguous requests into aligned plans, make architectural decisions explicit, introduce safety checks, and keep humans involved at the right points in the workflow.

## What's included

### Planning and alignment

- **blueprint** — Aligns context and scope before implementation, refactoring, or architectural changes.
- **project-ideation-alignment** — Maps domain knowledge and clarifies intent at the beginning of a project.
- **query-intent-alignment** — Expands underspecified requests and identifies missing constraints.
- **agent-ticket-planner** — Breaks large or failure-prone changes into ordered implementation tickets.

### Reliability and safety

- **cognitive-grounding-guard** — Encourages calibrated confidence and reduces unsupported assumptions.
- **double-blind-circuit-breaker** — Pauses when ambiguity and uncertainty make execution unsafe.
- **agent-ticket-verifier** — Independently checks completed work against scope and fresh evidence.

### Architecture and implementation

- **pattern-composition** — Selects and combines design patterns for maintainable architectures.
- **agent-ticket-executor** — Executes a single implementation ticket with repository provenance and evidence tracking.

### Collaboration and knowledge management

- **human-in-the-loop-feedback** — Supports user intervention, intermediate review, and correction of session context.
- **output-presentation-formatter** — Structures complex technical output for easier review.
- **sync-project-summary** — Synchronizes project requirements and working agreements into `PROJECT.md` and `GEMINI.md`.

## Installation

Clone the repository into the local plugins directory used by your agent environment:

```bash
git clone https://github.com/flyw/skills.git ~/.gemini/config/plugins/flyw
```

The repository follows the plugin layout expected by Codex-compatible environments:

```text
flyw/
├── .codex-plugin/plugin.json
├── skills/
│   ├── agent-ticket-executor/
│   ├── agent-ticket-planner/
│   ├── agent-ticket-verifier/
│   ├── blueprint/
│   ├── cognitive-grounding-guard/
│   ├── double-blind-circuit-breaker/
│   ├── human-in-the-loop-feedback/
│   ├── output-presentation-formatter/
│   ├── pattern-composition/
│   ├── project-ideation-alignment/
│   ├── query-intent-alignment/
│   └── sync-project-summary/
├── GEMINI.md
└── PROJECT.md
```

After installation, skills are available under the `flyw:` namespace. For example:

```text
flyw:blueprint
flyw:query-intent-alignment
flyw:agent-ticket-verifier
```

## Design principles

- Clarify intent before committing to implementation.
- Make assumptions and boundaries visible.
- Prefer small, verifiable units of work.
- Keep humans in the loop for consequential decisions.
- Support evidence-based verification instead of self-declared completion.

## Status

Flyw is an evolving collection of reusable agent skills. Interfaces and workflows may change as the skills are tested across different projects and agent environments.

## Contributing

Contributions are welcome. Please keep each skill focused, document its trigger conditions and workflow, and verify that changes preserve the plugin structure.

## License

Licensed under the Apache License 2.0. See the plugin metadata and the repository license file for details.
