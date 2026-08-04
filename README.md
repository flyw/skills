# Skills

This repository contains a curated collection of reusable agent skills and the tools used to install and synchronize them across devices.

## Repository layout

- [`flyw/`](flyw/) — the bundled plugin and its skills.
- [`install.py`](install.py) — installs the bundled plugin into a local agent plugins directory.
- [`sync-skills.sh`](sync-skills.sh) — synchronizes local skill links from the library into the local skills directory.

## What's included

### Agent ticket workflow

- **agent-ticket-planner** — Breaks large or failure-prone changes into ordered implementation tickets.
- **agent-ticket-executor** — Executes a single implementation ticket with repository provenance and evidence tracking.
- **agent-ticket-verifier** — Independently checks completed work against scope and fresh evidence.

### Intent alignment and cognitive safety

- **cognitive-grounding-guard** — Encourages calibrated confidence and reduces unsupported assumptions.
- **double-blind-circuit-breaker** — Pauses when ambiguity and uncertainty make execution unsafe.
- **project-ideation-alignment** — Maps domain knowledge and clarifies intent at the beginning of a project.
- **query-intent-alignment** — Expands underspecified requests and identifies missing constraints.

### Architecture and design

- **blueprint** — Aligns context and scope before implementation, refactoring, or architectural changes.
- **pattern-composition** — Selects and combines design patterns for maintainable architectures.

### Collaboration and project context

- **human-in-the-loop-feedback** — Supports user intervention, intermediate review, and correction of session context.
- **output-presentation-formatter** — Structures complex technical output for easier review.
- **sync-project-summary** — Synchronizes project requirements and working agreements into `PROJECT.md` and `GEMINI.md`.

## Install

```bash
python3 install.py
```

Preview the installation first:

```bash
python3 install.py --dry-run
```

To install into another plugin directory:

```bash
python3 install.py --target-dir /path/to/plugins
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

This is an evolving collection of reusable agent skills. Interfaces and workflows may change as the skills are tested across different projects and agent environments.

## Contributing

Contributions are welcome. Please keep each skill focused, document its trigger conditions and workflow, and verify that changes preserve the plugin structure.

## License

Licensed under the Apache License 2.0. See the plugin metadata for details.
