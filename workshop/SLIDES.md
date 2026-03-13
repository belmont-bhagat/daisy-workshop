# Agentic AI Workshop — Slide Deck Outline

**Design principle:** Every slide either asks a question, shows a diagram, or displays code. No bullet-point walls. Max 20 words of body text per slide. Visuals carry the weight — your voice carries the explanation.

**Recommended tool:** Slides.com, Keynote, or Canva. Dark background (#0f0f0f), monospace font for code, high contrast.

---

## SLIDE 1 — Title Slide

**Title:** Agentic AI: From Chatbot to Agent
**Subtitle:** A 50-minute workshop
**Visual:** Animated terminal with a blinking cursor, then text appearing: `> python agent.py`

**Presenter note:** Don't show this slide — go straight to the terminal demo. Come back to this only if you need to introduce yourself before starting.

---

## SLIDE 2 — "What did you just see?"

**Title:** What did you just see?
**Visual:** A screenshot or recording of the agent terminal output (the run you just did)
**Body:** *(nothing — just the screenshot)*

**Presenter note:** Show this after the opening demo. Let students read the output on screen. Ask: "Describe what happened." This slide is an anchor for the discussion, not new information.

---

## SLIDE 3 — The Chatbot Model

**Title:** The Chatbot Model
**Visual:** Simple two-box diagram

```
[ You ] ──── question ────► [ LLM ]
[ You ] ◄─── answer ──────  [ LLM ]
[ You ] ──── question ────► [ LLM ]
[ You ] ◄─── answer ──────  [ LLM ]
```

**Body:** You are the agent. The LLM reacts.

**Presenter note:** Point out that the human is doing all the deciding — what to ask next, what to do with the answer. The LLM is stateless and passive. "You're doing all the work."

---

## SLIDE 4 — The Agent Loop

**Title:** The Agent Loop
**Visual:** Circular diagram with four nodes, arrows going clockwise

```
        PERCEIVE
       (task + context)
           │
           ▼
        REASON          ◄───┐
     (LLM decides)          │
           │                │
           ▼                │
          ACT           OBSERVE
     (tool call)    (tool result back)
           │                │
           └────────────────┘
```

**Body:** *(no body — diagram only)*

**Presenter note:** Say the four words out loud. Walk the loop slowly. "Perceive — here's the context. Reason — what should I do? Act — call a tool. Observe — what happened? And repeat." Leave this diagram visible on a side monitor or whiteboard for the rest of the workshop.

---

## SLIDE 5 — The Intern Analogy

**Title:** The LLM is a reasoning step, not a runtime
**Visual:** Two-column layout

| Smart Intern | Your Code |
|---|---|
| Reads the task | Sends the task |
| Writes "please search X" | Runs the search |
| Reads the result | Returns the result |
| Writes "save this summary" | Saves the file |
| Writes "done" | Stops the loop |

**Body:** The intern never touched the keyboard.

**Presenter note:** This is the most important conceptual slide. Say: "The LLM communicates by writing structured memos. Your code carries out the physical actions. The intelligence is in the reasoning — the execution is in the loop."

---

## SLIDE 6 — What Makes It Agentic

**Title:** Three properties of an agent
**Visual:** Three large words, each with a one-line definition below

**AUTONOMY**
completes sub-tasks without step-by-step direction

**TOOL USE**
can reach outside the model — search, write, call APIs

**STATE**
carries context across multiple reasoning steps

**Presenter note:** Ask: "If I give an LLM a system prompt that says 'you are a helpful assistant' — is that an agent?" Answer: No. Without the loop and tool execution, it's a chatbot with a costume. The agent property comes from the architecture, not the prompt.

---

## SLIDE 7 — Why Now?

**Title:** Why is this possible now?
**Visual:** Timeline or before/after comparison

**Before (2022):**
Model returns: *"I would search for: agentic AI..."*
You parse free text and hope.

**After (2023+):**
Model returns structured JSON:
```json
{ "tool": "search_web", "query": "agentic AI" }
```
Reliable. Parseable. Automatable.

**Presenter note:** "Function calling / tool use in the API is what unlocked production agents. Before, you'd prompt the model to say 'SEARCH:' in the right place and pray. Now it returns a typed structure you can route programmatically. Reliability = agency."

---

## SLIDE 8 — Demo 1 Setup

**Title:** Demo 1: The Reasoning Illusion
**Visual:** Browser window with Claude.ai open (or screenshot)
**Body:** Can Claude complete a multi-step task... without tools?

**Presenter note:** This is a transition slide — show it, say "Let's find out," and switch to Claude.ai. The slide sets the question before the demo answers it.

---

## SLIDE 9 — Demo 1 Debrief

**Title:** Reasoning ≠ Action
**Visual:** Two boxes, one struck through

```
[✓] Reasoned about the task
[✓] Generated a plan
[✓] Wrote "search results" (hallucinated)
[✗] Searched anything
[✗] Saved any file
[✗] Completed the task
```

**Body:** Very smart autocomplete. Nothing more.

**Presenter note:** "Claude wrote a beautiful plan. It even imagined what the search results might say. But nothing happened. Without the loop, it's still just text generation."

---

## SLIDE 10 — Demo 2 Setup

**Title:** Demo 2: Giving the Model Hands
**Visual:** System prompt text (use a monospace code block, 14pt)
```
You have access to these tools:
- search_web(query: str)
- save_note(text: str, filename: str)
When you want to use a tool, respond with:
TOOL_CALL: tool_name(arg1, arg2)
```

**Body:** What happens when Claude knows it has tools?

**Presenter note:** Paste this into Claude.ai system prompt. Show students that the model immediately starts planning around the tools rather than hallucinating results. Manually role-play the tool executor — copy Claude's tool call, paste a fake result back.

---

## SLIDE 11 — Demo 2 Debrief

**Title:** Tool use is structured conversation
**Visual:** Message exchange shown as chat bubbles

```
You:     "Research agentic AI and save a summary."
Claude:  TOOL_CALL: search_web("agentic AI definition")
You:     [result: "Agentic AI refers to..."]
Claude:  TOOL_CALL: save_note("• Point 1...", "summary.txt")
You:     [result: "Saved to notes/summary.txt"]
Claude:  "Done. Summary saved."
```

**Body:** You just played the role of agent.py.

**Presenter note:** "The only difference between what I just did manually and what the code does: speed and the ability to run unsupervised. The protocol is identical."

---

## SLIDE 12 — Demo 3 Setup

**Title:** Demo 3: The Full Loop
**Visual:** Terminal screenshot or live terminal window

```bash
python agent.py
```

**Body:** Now the code plays the role you just played.

**Presenter note:** Switch to terminal. Run the agent live. Narrate each line as it appears. "That's Reason. That's Act. That's Observe. And now Reason again."

---

## SLIDE 13 — Code: TOOLS Schema

**Title:** The Tool Menu
**Visual:** Code block (agent.py TOOLS list, trimmed)

```python
TOOLS = [{
    "name": "search_web",
    "description": "Search DuckDuckGo and return a summary.",
    "input_schema": {
        "properties": {
            "query": {"type": "string"}
        }
    }
}]
```

**Body:** The description is read by the model, not the computer.

**Presenter note:** "Claude reads this schema and decides which tool fits the task. Write descriptions like you're documenting an API for a smart teammate — the quality of your description directly affects which tools Claude chooses and when."

---

## SLIDE 14 — Code: The Loop

**Title:** The Whole Agent — 15 Lines
**Visual:** Code block (the core of run_agent, condensed)

```python
while iteration < MAX_ITERATIONS:
    response = client.messages.create(
        model=MODEL, tools=TOOLS, messages=messages
    )
    if response.stop_reason == "end_turn":
        break
    if response.stop_reason == "tool_use":
        result = execute_tool(tool_call)
        messages.append(tool_result)
```

**Body:** Everything else is plumbing.

**Presenter note:** "The loop itself is trivial. That's the point — the intelligence is in the model, not in your orchestration code. Your job is to wire the tools correctly."

---

## SLIDE 15 — Multi-Agent Systems

**Title:** One agent is just the start
**Visual:** Org chart style diagram

```
         [Orchestrator]
        /       |       \
[Research]  [Critic]  [Writer]
   agent      agent     agent
```

**Body:** Specialists. Parallelism. One agent checks another.

**Presenter note:** "Each box is the loop we just built. The orchestrator delegates. Research agent searches. Critic validates. Writer formats. You get parallelism and quality checks — exactly how human teams work."

---

## SLIDE 16 — Where It's Going

**Title:** Three things to watch
**Visual:** Three rows, icon + short label each

```
⏳  Long-horizon tasks — agents that run for hours
🖥️  Computer use — agents that control a browser or desktop
🤝  Agent-to-agent protocols — agents from different companies collaborating
```

**Body:** The loop is the same. The tools get more powerful.

**Presenter note:** Keep this brief. "The starter repo you're cloning today runs the same loop as production systems. The difference is scale, tooling, and safety infrastructure — not the core idea."

---

## SLIDE 17 — Clone the Repo

**Title:** Your turn
**Visual:** Large monospace text block, center-aligned

```bash
git clone [repo URL]
cd repo
pip install anthropic python-dotenv requests
cp .env.example .env
# Add your API key
python agent.py
```

**Body:** Running in under 10 minutes.

**Presenter note:** Show this while students open their laptops. Walk around and help anyone who hits an issue. The README has full setup instructions. Common issue: forgetting to copy `.env.example` to `.env`.

---

## SLIDE 18 — Q&A

**Title:** Questions?
**Visual:** The agent loop diagram from Slide 4, with a question mark in the center

**Presenter note:** Seed questions if the room is quiet:
- "What task would you want to automate with an agent?"
- "What could go wrong if an agent had too many powerful tools?"
- "How would you test an agent? How do you know it did the right thing?"

---

## SLIDE COUNT SUMMARY

| # | Title | Section |
|---|---|---|
| 1 | Title | Pre-workshop |
| 2 | What did you just see? | Hook |
| 3 | The Chatbot Model | Mental Model |
| 4 | The Agent Loop | Mental Model |
| 5 | The Intern Analogy | Mental Model |
| 6 | What Makes It Agentic | Mental Model |
| 7 | Why Now? | Mental Model |
| 8 | Demo 1 Setup | Demo Arc |
| 9 | Demo 1 Debrief | Demo Arc |
| 10 | Demo 2 Setup | Demo Arc |
| 11 | Demo 2 Debrief | Demo Arc |
| 12 | Demo 3 Setup | Demo Arc |
| 13 | Code: TOOLS Schema | Repo Walkthrough |
| 14 | Code: The Loop | Repo Walkthrough |
| 15 | Multi-Agent Systems | Closing |
| 16 | Where It's Going | Closing |
| 17 | Clone the Repo | Closing |
| 18 | Q&A | Closing |

**Total: 18 slides for 50 minutes = ~2.75 min per slide average.** Demos 1-3 (slides 8-12) should feel fast — the terminal is the content, not the slide.
