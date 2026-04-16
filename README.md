# OpenCode + Biomni — Quick guide for biomedical users

**In one sentence:** You chat in **OpenCode** (like a smart terminal assistant). It can call **Biomni** tools to query public databases, run genomics-oriented helpers, and use your local **data lake** files—without you writing glue code for every step.

**Who this is for:** Researchers and analysts in biology/medicine who are comfortable opening a terminal *occasionally* but want a **clear checklist** rather than distributed engineering docs.

**Platforms:** **macOS and Linux** only. (Windows is not covered here.)

---

## Concepts in plain language

| Term | What it means for you |
|------|------------------------|
| **OpenCode** | The app where you type requests and see answers. It also chooses when to call tools. [Docs](https://opencode.ai/docs/config/). |
| **Biomni** | A biomedical AI toolkit (Python package) with functions for databases, genomics, protocols, etc. [Project](https://github.com/snap-stanford/Biomni). |
| **MCP** | A standard way for OpenCode to talk to a small **side program** that runs Biomni on your machine. You do not need to learn MCP—just know that tools appear with names like `biomni_*`. |
| **Data lake** | A **folder of tables/files** (e.g. DepMap, GTEx-style resources—see Biomni docs) that many analyses read locally. You (or IT) place them under `biomni_data/data_lake/`. This repo **does not** auto-download the full ~11GB release by default. |

**Important:** Keep **OpenCode** as your main chat. Do **not** run Biomni’s `A1.go()` as your everyday interface when using this setup.

---

## Before you start — checklist

Copy this list and tick items with your lab / IT as needed.

- [ ] **OpenCode** installed and able to open this project folder.
- [ ] **Python 3** available (`python3 --version`). A **virtual environment** is strongly recommended (keeps Biomni isolated).
- [ ] **API keys** in a `.env` file at the project root (at minimum what Biomni needs for *database* tools—often Claude or OpenAI keys; see [Biomni README](https://github.com/snap-stanford/Biomni#readme)). Without keys, **online database-style tools may fail** even if local files exist.
- [ ] **Data lake** (if your analysis needs local tables): files copied or synced into `./biomni_data/data_lake/` — see [docs/datalake-setup.md](docs/datalake-setup.md).
- [ ] **Absolute path to your venv Python** after install (macOS/Linux example: `/Users/you/BiomedicalAgent/.venv/bin/python`). You will paste this into `opencode.json` (step 3 below).

---

## Fast path (first successful run)

**Goal:** OpenCode can invoke Biomni tools without import errors.

### Step 1 — Install Biomni into a virtual environment

In a terminal:

```bash
cd /path/to/BiomedicalAgent
python3 -m venv .venv
source .venv/bin/activate          # Linux/macOS bash/zsh
# If you use fish: source .venv/bin/activate.fish
pip install -r requirements.txt
```

Check:

```bash
python -c "import biomni; print('OK')"
```

If this prints `OK`, the environment is ready.

### Step 2 — API keys for tools that call models

Create a file named `.env` in the project root. At minimum, follow [Biomni’s environment variables](https://github.com/snap-stanford/Biomni) (e.g. `ANTHROPIC_API_KEY` and/or `OPENAI_API_KEY`). The script [`scripts/run_biomni_mcp.py`](scripts/run_biomni_mcp.py) loads `.env` when `python-dotenv` is installed (included in `requirements.txt`).

### Step 3 — Tell OpenCode which Python to use

Open [`opencode.json`](opencode.json). Replace **`python3`** in `mcp.biomni.command` with the **full path** to the interpreter from Step 1, for example:

```json
"command": [
  "/Users/yourname/BiomedicalAgent/.venv/bin/python",
  "scripts/run_biomni_mcp.py"
]
```

Why: OpenCode may not see your activated shell; the path makes the Biomni install **unambiguous**.

### Step 4 — (Optional) Local data lake

If your work needs Biomni’s **local** tables (not only live API calls), populate:

```text
BiomedicalAgent/biomni_data/data_lake/
```

See [docs/datalake-setup.md](docs/datalake-setup.md). If you skip this, many **API-based** queries can still work; **file-based** joins and offline workflows may not.

### Step 5 — Open the project in OpenCode

Start OpenCode from this repository (or open the folder). It reads [`opencode.json`](opencode.json) and starts the **`biomni`** MCP server (unless disabled). Default timeout is **120 seconds** for slow first load.

---

## How to actually “analyze” from chat

1. **You** describe the scientific question in **OpenCode** (English or your usual language, depending on model support).
2. The **model** may choose **Biomni tools** (often named with a `biomni` prefix).
3. Those tools run on your machine via [`scripts/run_biomni_mcp.py`](scripts/run_biomni_mcp.py), using modules such as **`biomni.tool.database`** and **`biomni.tool.genomics`** (configurable).
4. **Results** return to the same OpenCode thread so you can iterate (interpret, refine, plot in a follow-up step).

**Note:** Some database tools trigger an **extra** model call *inside* Biomni to turn your natural language into a structured API request. That is **not** a second chat app—it happens inside the tool.

---

## Example prompts you can try

Adapt to your organism/genes/disease. Mention **Biomni** or **use biomni tools** if the model is hesitant.

- “Using Biomni tools, given UniProt ID **P01308**, summarize key protein attributes and any linked disease associations you can retrieve.”
- “Call the relevant Biomni database tools to find PDB structures for human **TP53** and list the top hits with resolution.”
- “With Biomni genomics tools, outline a sensible approach to check basic annotation for gene **BRCA1** (do not invent file paths; say what inputs you need).”

If your **data lake** is populated, add: “Assume local Biomni data lake paths as in this project; join or summarize **only the files I name** (e.g. a specific `.parquet`), and only if the tool supports it.”

---

## What is enabled by default

In [`opencode.json`](opencode.json):

- **Modules:** `biomni.tool.database` and `biomni.tool.genomics` (comma-separated in `BIOMNI_MCP_TOOL_MODULES`).
- **Data root:** `BIOMNI_DATA_PATH` = `.` (project root), so Biomni looks for `./biomni_data/data_lake/`.

To add more domains (immunology, cancer biology, etc.), extend the comma-separated list **carefully**—each extra module adds many tool definitions and can **fill the model context** ([OpenCode MCP note](https://opencode.ai/docs/mcp-servers/)).

---

## If something fails

| Symptom | What to check |
|---------|----------------|
| `ModuleNotFoundError: biomni` | Venv not used in `opencode.json` `command` — use absolute `.../bin/python`. |
| Tool errors about **API / auth** | `.env` keys missing or wrong provider for Biomni’s `default_config`. |
| **Timeout** when MCP starts | Machine slow or large imports; increase `mcp.biomni.timeout` in [`opencode.json`](opencode.json). |
| Analysis needs **local** tables but paths fail | Confirm files exist under `biomni_data/data_lake/` and names match Biomni’s expected inventory (see Biomni `env_desc.data_lake_dict`). |

---

## Files in this repo (short map)

| File | Role |
|------|------|
| [`opencode.json`](opencode.json) | Registers the Biomni MCP server for OpenCode |
| [`scripts/run_biomni_mcp.py`](scripts/run_biomni_mcp.py) | Starts Biomni tools over MCP (stdio) |
| [`AGENTS.md`](AGENTS.md) | Short rules for the agent |
| [`.opencode/rules/biomni.md`](.opencode/rules/biomni.md) | Tool naming and optional `tools` globs |
| [`requirements.txt`](requirements.txt) | `biomni` and helpers |
| [`docs/datalake-setup.md`](docs/datalake-setup.md) | Where to put datalake files |

---

## Security

Biomni can run powerful code and reach the network. Use only on **trusted machines** and **non-sensitive** or properly governed data, consistent with your institution’s policies.

---

## Further reading

- [Biomni (GitHub)](https://github.com/snap-stanford/Biomni) — full paper, environment, and tool list.
- [OpenCode configuration](https://opencode.ai/docs/config/) — `opencode.json`, rules, agents.
