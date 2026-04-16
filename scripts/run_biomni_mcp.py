#!/usr/bin/env python3
"""Biomni FastMCP stdio server for OpenCode (macOS / Linux).

Reads environment:
  BIOMNI_DATA_PATH or BIOMNI_PATH — parent directory under which ``biomni_data/`` lives
    (same semantics as ``A1(path=...)``). Defaults to project root (parent of scripts/).
  BIOMNI_MCP_TOOL_MODULES — comma-separated module names, e.g.
    ``biomni.tool.database,biomni.tool.genomics``. Defaults to database + genomics.

Uses ``expected_data_lake_files=[]`` to skip automatic S3 datalake download when data is
already present locally. Set ``use_tool_retriever=False`` for faster MCP handshake.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _load_dotenv(root: Path) -> None:
    env_path = root / ".env"
    if not env_path.is_file():
        return
    try:
        from dotenv import load_dotenv

        load_dotenv(env_path, override=False)
    except ImportError:
        pass


def _stderr_print(*args: object) -> None:
    print(*args, file=sys.stderr)


def main() -> None:
    root = _project_root()
    os.chdir(root)
    _load_dotenv(root)

    data_path = os.environ.get("BIOMNI_DATA_PATH") or os.environ.get("BIOMNI_PATH") or str(root)
    modules_raw = os.environ.get(
        "BIOMNI_MCP_TOOL_MODULES",
        "biomni.tool.database,biomni.tool.genomics",
    )
    tool_modules = [m.strip() for m in modules_raw.split(",") if m.strip()]

    # A1 logs to stdout by default; MCP requires stdout for JSON-RPC only.
    _stderr_print("Biomni MCP: data path (A1 path arg):", data_path)
    _stderr_print("Biomni MCP: tool_modules:", tool_modules)

    _stdout = sys.stdout
    sys.stdout = sys.stderr
    try:
        from biomni.agent.a1 import A1

        agent = A1(
            path=data_path,
            use_tool_retriever=False,
            expected_data_lake_files=[],
        )
        mcp = agent.create_mcp_server(tool_modules=tool_modules)
    finally:
        sys.stdout = _stdout

    _stderr_print("Biomni MCP: starting stdio transport (JSON-RPC on stdout).")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
