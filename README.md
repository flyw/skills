# Skills

This repository contains a curated collection of reusable agent skills and the tools used to install and synchronize them across devices.

## Repository layout

- [`flyw/`](flyw/) — the bundled plugin and its skills.
- [`install_mattpocock.py`](install_mattpocock.py) — downloads and flattens Matt Pocock's skills.
- [`install_deep_research.py`](install_deep_research.py) — downloads Deep Research skills.
- [`skills-sources.json`](skills-sources.json) — tracked list of downloaded sources; downloaded repositories themselves are ignored.
- [`sync-skills.sh`](sync-skills.sh) — synchronizes skill folders from the library into the local skills directory.

## What's included

### Agent ticket workflow

- **agent-ticket-planner** — Breaks large or failure-prone changes into ordered implementation tickets.
- **agent-initiative-orchestrator** — Coordinates ticket selection, Executor/Verifier sessions,
  dependency gates, resumptions, and consequential user decisions across the initiative.
- **agent-ticket-executor** — Executes a single implementation ticket with repository provenance and evidence tracking.
- **agent-ticket-verifier** — Independently checks completed work against scope and fresh evidence.

The ticket workflow is coordinated in this order: the planner creates the specification and
dependency-ordered tickets; the orchestrator selects the next uncompleted ticket and starts or
resumes the Executor; the Verifier independently checks tickets marked ready for verification;
only verified `completed` tickets unlock their dependents. The orchestrator may ask the user only
when a decision materially changes scope, behavior, risk, or authority, and otherwise resolves
reversible details from repository evidence and safe defaults.

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
python3 install_mattpocock.py
python3 install_deep_research.py
```

By default this downloads these repositories into the project directory:

- `https://github.com/mattpocock/skills` → `./mattpocock`
- `https://github.com/Weizhena/Deep-Research-skills` → `./DeepResearch`

Running the command again downloads the latest version and replaces the
existing directory:

```bash
python3 install_mattpocock.py --dry-run
python3 install_deep_research.py --dry-run
```

To install into another plugin directory:

```bash
python3 install_mattpocock.py --target-dir /path/to/plugins
python3 install_deep_research.py --target-dir /path/to/plugins
```

The `mattpocock` repository is normalized during download: skill folders are
moved from category directories such as `skills/engineering/` directly into
`mattpocock/skills/`.

`DeepResearch` keeps only the repository's `skills/research-codex-en` variant
and installs it as `DeepResearch/skills/`.

After installation, skills are available under the `flyw:` namespace. For example:

```text
flyw:blueprint
flyw:query-intent-alignment
flyw:agent-ticket-verifier
```

To copy and synchronize skills, run:

```bash
./sync-skills.sh
```

At startup it asks whether skills should be placed in `~/.agents/skills` or
`~/.codex/skills`.

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
