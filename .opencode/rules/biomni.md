# Biomni MCP usage

## When to use `biomni` tools

- Use **`biomni` MCP tools** for tasks that map to Biomni’s packaged APIs: external database queries (UniProt, PDB, …), genomics helpers, and other functions exposed in the configured modules (`biomni.tool.database`, `biomni.tool.genomics` by default).
- Prefer MCP over ad-hoc `python -c` when the user already has OpenCode and the tool is listed.

## Tool name prefix

- OpenCode registers MCP tools with a **server prefix**. The server name in [`opencode.json`](../../opencode.json) is `biomni`, so tool identifiers typically match the pattern **`biomni_*`** (exact names depend on FastMCP / Biomni registration).

## Context size

- Many MCP tools increase context usage. This project:
  - Exposes only **two** `tool_modules` by default (see `BIOMNI_MCP_TOOL_MODULES` in [`opencode.json`](../../opencode.json) and [`scripts/run_biomni_mcp.py`](../../scripts/run_biomni_mcp.py)).
  - Sets [`opencode.json`](../../opencode.json) `mcp.biomni.timeout` to **120000** ms for slow cold starts.

### Optional: disable subsets via `tools` globs

- To turn off **all** tools from this MCP server globally, set in `opencode.json`:

```json
"tools": {
  "biomni_*": false
}
```

- Then enable per-agent only (see [OpenCode agents](https://opencode.ai/docs/agents#tools)) for a dedicated biomedical agent.
- To disable a subset, use a tighter glob if your tool names allow it (e.g. `biomni_query_*`), per OpenCode glob rules.

## NL→API inside tools

- Several database tools call an internal LLM (`default_config`) to map natural language to API parameters. This is **not** a replacement for OpenCode’s main model; it runs inside the tool implementation.
