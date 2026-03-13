# Agentic AI Workshop — Starter Agent

A minimal Python agent built with the Anthropic SDK that demonstrates the core agentic loop: **perceive → reason → act → observe → repeat**.

The agent has three tools it can use autonomously:
- `search_web` — searches DuckDuckGo (no API key needed)
- `save_note` — saves text to a local file
- `calculate` — safely evaluates math expressions

---

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
# .venv\Scripts\activate         # Windows

# 2. Install dependencies
pip install anthropic python-dotenv requests

# 3. Add your Anthropic API key
cp .env.example .env
# Open .env and paste your key from https://console.anthropic.com/

# 4. Run the agent
python agent.py
```

That's it. The agent will research agentic AI, summarize it, and save `notes/summary.txt`.

> **Next time** you open the project, just re-activate the venv before running:
> ```bash
> source .venv/bin/activate   # Mac/Linux
> ```

---

## How It Works

```
You (task) ──► Claude (reasoning) ──► Tool call?
                    ▲                      │
                    │                      ▼
              Tool result ◄──── Python runs the tool
```

1. `agent.py` sends your task to Claude along with a list of available tools.
2. Claude decides whether to call a tool or respond directly.
3. If Claude calls a tool, `agent.py` runs it locally and sends the result back.
4. This loop repeats until Claude says it's done, or after 5 iterations.

The agent prints every reasoning step and tool call to the terminal — so you can follow exactly what Claude is thinking at each step.

---

## File Structure

```
repo/
├── agent.py       # Agent loop — reads messages, calls Claude, handles tools
├── tools.py       # Tool implementations (search, save, calculate)
├── .env.example   # Template for your API key
└── notes/         # Created automatically when save_note is called
```

---

## Try Custom Tasks

```bash
python agent.py "What is the speed of light? Calculate how long it takes light to travel 1 million km."
python agent.py "Search for the definition of machine learning and save a summary to ml_notes.txt"
```

---

## Key Concepts Demonstrated

| Concept | Where to look |
|---|---|
| Tool schema definition | `agent.py` → `TOOLS` list |
| Tool dispatch | `agent.py` → `TOOL_DISPATCH` dict |
| Agent loop | `agent.py` → `run_agent()` function |
| Tool implementations | `tools.py` |
| Safe code evaluation | `tools.py` → `calculate()` / `_eval_node()` |
