# Adapting This Workshop

This workshop is designed to be forked and customised. Here's how to make it your own.

---

## Forking for Your Own Delivery

1. Fork the repo on GitHub
2. Update the clone URL in `workshop/DEMO_SCRIPT.md` and `scripts/generate_slides.py` to point to your fork
3. Regenerate the slide deck: `python3 scripts/generate_slides.py` (requires `pip install python-pptx`)
4. Update `MY_NOTES.md` with your own pre-workshop checklist

---

## Swapping in New Tools

The agent ships with three tools: `search_web`, `save_note`, `calculate`. To add your own:

1. **Implement it** in `repo/tools.py` — any function that takes arguments and returns a string
2. **Register the schema** in the `TOOLS` list in `repo/agent.py` — name, description, input_schema
3. **Add the dispatch entry** in `TOOL_DISPATCH` in `repo/agent.py`

Example tools that work well in a workshop setting:
- `get_weather(city)` — call a free weather API
- `fetch_url(url)` — fetch and return plain text from a webpage
- `list_files()` — list files in the current directory

---

## Changing the Default Task

Edit `DEFAULT_TASK` at the top of `repo/agent.py`. Good tasks for live demos:
- Something that visibly uses multiple tools in sequence
- Something with an observable output (a saved file, a calculation result)
- Something the audience would find relatable

---

## Regenerating the Slide Deck

The slide deck is generated from `scripts/generate_slides.py`. After making changes:

```bash
pip install python-pptx   # one-time
python3 scripts/generate_slides.py
# Output: dist/slides.pptx
```

The `SLIDES.md` file in `workshop/` is the human-readable outline — keep both in sync when you make changes.

---

## Reporting Issues

Open an issue on GitHub if something is broken or unclear.
