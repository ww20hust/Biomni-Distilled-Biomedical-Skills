# Agent context (OpenCode + Biomni)

Human-oriented setup steps, checklists, and example prompts: **[README.md](README.md)**.

## Primary orchestration

- **OpenCode** owns the chat loop and model routing. Do **not** start `A1.go()` as the main interactive session for day-to-day work in this repo.

## Biomni MCP (`biomni`)

- This project exposes **Biomni** tools via a **local MCP** server (stdio) named `biomni` in [`opencode.json`](opencode.json).
- For database queries, literature-backed lookups, genomics helpers, etc., **prefer the `biomni` MCP tools** when they match the task.
- Tool names are typically prefixed with the server name (e.g. patterns like `biomni_*`). See [`.opencode/rules/biomni.md`](.opencode/rules/biomni.md) for details and context limits.

## Data layout

- Biomni expects a parent directory (here: project root when `BIOMNI_DATA_PATH=.`) containing:
  - `biomni_data/data_lake/` — parquet/TSV/pkl files (see [docs/datalake-setup.md](docs/datalake-setup.md))
  - optional `biomni_data/benchmark/` for benchmarks
- The MCP runner uses `expected_data_lake_files=[]` so it does **not** auto-download from S3; populate `data_lake` yourself or via your mirror.

## Python interpreter

- [`opencode.json`](opencode.json) uses `python3` on your `PATH`. For a venv, replace the first element of `mcp.biomni.command` with the **absolute** path to the venv interpreter, e.g. `/path/to/venv/bin/python`.

## Nested LLM calls

- Some `database` tools use Biomni’s `default_config` LLM for NL→API translation. That is a **tool-internal** call, not a second chat UI.
