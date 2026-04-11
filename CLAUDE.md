# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TosecDB is a Python tool that converts TOSEC datfiles (XML) into a SQL database. TOSEC is a standardized naming convention for retro game ROM files.

## Tooling

- **Python 3.14**, managed via [mise](https://mise.jdx.dev/) (`mise.toml`)
- **uv** for package management (no dependencies currently)
- **Ruff** for linting and formatting

After cloning, run `mise trust && mise install` to set up the toolchain.

## Running

```bash
uv run python -m tosecdb    # run from repo root
```

## Linting / Formatting

```bash
ruff check src/              # lint
ruff format src/             # format
```

## Architecture

The project has two main layers:

1. **`src/tosecdb/tosec_parser/`** — Parses TOSEC data into Python dataclasses:
   - `datfile_parser.py` — SAX-based XML parser that reads `.dat` files and yields `TOSECXMLGame` / `TOSECXMLRom` objects.
   - `name_parser.py` — Regex-based parser that decodes the TOSEC naming convention string into a `TOSECInfo` dataclass (date, publisher, country, dump flags, etc.).
   - `definitions.py` — Lookup lists for valid TOSEC field values (countries, languages, systems, dump flags, etc.).

2. **`src/tosecdb/dbschema.sql` / `dbschema.py`** — Database schema. Four tables: `platform` → `game` → `gameversion` → `rom`. The `gameversion` table links a specific version of a game (with its metadata flags) to a platform and contains one or more ROMs.

The parsing pipeline: datfile XML → `TOSECXMLGame` → name parsed via `parse_tosec_name()` → `TOSECInfo` → mapped to DB schema dataclasses → inserted into the database.
