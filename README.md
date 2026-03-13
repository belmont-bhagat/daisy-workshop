# Agentic AI Workshop

A complete 50-minute live workshop package on Agentic AI — designed for students and academics with some API/AI exposure.

## What's Inside

```
daisy-workshop/
├── repo/               ← Student starter repo (clone & run in <10 min)
│   ├── agent.py        ← Main agent loop
│   ├── tools.py        ← Tool implementations
│   ├── .env.example    ← API key template
│   └── README.md       ← Student-facing setup guide
└── workshop/           ← Facilitator materials
    ├── OUTLINE.md      ← 50-min script with speaker notes & timing
    ├── SLIDES.md       ← 18-slide deck outline with presenter notes
    └── DEMO_SCRIPT.md  ← Step-by-step live demo instructions
```

## For Students

Go to the `repo/` folder — that's your starting point.

```bash
cd repo

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
# .venv\Scripts\activate         # Windows

# Install dependencies
pip install anthropic python-dotenv requests

# Add your Anthropic API key
cp .env.example .env
# Open .env and paste your key

# Run the agent
python agent.py
```

Get your free API key at [console.anthropic.com](https://console.anthropic.com/)

## For Facilitators

Read `workshop/OUTLINE.md` first — it has the full 50-minute script, timing, speaker notes, and audience questions. Then review `workshop/DEMO_SCRIPT.md` before the session and run through the demos at least once on your own machine.

**Pre-workshop checklist:**
- [ ] Working Anthropic API key in `repo/.env`
- [ ] `python agent.py` tested and running end-to-end
- [ ] Terminal font size bumped to 16+ for projection
- [ ] Backup `notes/summary.txt` ready in case of network issues

## What the Agent Demonstrates

The starter agent shows the core agentic loop — **perceive → reason → act → observe** — using three tools:

| Tool | What it does |
|---|---|
| `search_web` | Searches DuckDuckGo (no API key needed) |
| `save_note` | Saves text to a local `.txt` file |
| `calculate` | Safely evaluates math expressions |

## Requirements

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)
- A virtual environment (recommended — keeps dependencies isolated)
- `pip install anthropic python-dotenv requests`
