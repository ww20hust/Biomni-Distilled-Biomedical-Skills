# Biomni data lake layout (Unix / macOS)

**For biomedical users:** The “data lake” is simply a **directory of pre-downloaded tables** (gene sets, DepMap-style files, etc.) that Biomni tools read from disk. You or your IT copy files here so analyses do not depend on re-downloading everything during each session.

## Directory layout

Biomni’s `A1(path=ROOT)` uses:

- `ROOT/biomni_data/data_lake/` — dataset files (parquet, TSV, pkl, etc.)
- `ROOT/biomni_data/benchmark/` — optional benchmark bundles

This project’s MCP script passes `path=ROOT` where `ROOT` is **`BIOMNI_DATA_PATH`** (default: project root when set to `.` in [`opencode.json`](../opencode.json)).

So with `BIOMNI_DATA_PATH` pointing at the repo root, place files under:

```text
./biomni_data/data_lake/
```

## Populating files

- **Option A**: Sync from your own mirror (same layout and filenames as upstream Biomni releases).
- **Option B**: Let Biomni download (not used by default here): the stock `A1()` without `expected_data_lake_files=[]` pulls from the upstream S3 bucket. The provided [`scripts/run_biomni_mcp.py`](../scripts/run_biomni_mcp.py) uses **`expected_data_lake_files=[]`** to skip automatic download; you are responsible for filling `data_lake`.

## Filename reference

- Semantic descriptions of expected filenames live in Biomni’s `env_desc.data_lake_dict` (see the `biomni` package source). Use that as the checklist when mirroring data.
