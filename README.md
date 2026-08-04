# Skills

This repository contains a curated collection of reusable agent skills and the tools used to install and synchronize them across devices.

## Repository layout

- [`flyw/`](flyw/) — the bundled plugin and its skills.
- [`install.py`](install.py) — installs the bundled plugin into a local agent plugins directory.
- [`sync-skills.sh`](sync-skills.sh) — synchronizes local skill links from the library into the local skills directory.

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

## Included skills

The bundled skills are documented in [`flyw/README.md`](flyw/README.md).
