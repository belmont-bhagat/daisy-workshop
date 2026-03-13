# Agentic AI Workshop — 50-Minute Facilitator Outline

**Audience:** Students / academics with some API and AI tool exposure
**Goal:** Build a working mental model of agentic AI and leave with a runnable starter repo
**Format:** Lecture + live demos (no slides-only sections; always have a terminal or browser open)

---

## PRE-WORKSHOP CHECKLIST (Before Students Arrive)

- [ ] Terminal open in `repo/` directory, `.env` filled in with working API key
- [ ] `python agent.py` tested — confirmed it runs end-to-end
- [ ] Browser tab open at claude.ai (logged in)
- [ ] Projector showing terminal, not slides
- [ ] Demo 1 prompt copied to clipboard
- [ ] Backup: record a 2-min screen capture of the agent running (in case of network issues)

---

## SECTION 1 — Hook / Opening Demo Setup `[0:00 – 5:00]`

**Goal:** Create curiosity before explaining anything. Show, don't tell.

### What to do
Open your terminal. Run:
```bash
python agent.py
```

Let it run completely while you say nothing except:

> "Watch the terminal. Don't explain anything yet."

After it finishes, ask the room:

> **"What did you just see? Describe it back to me."**

Wait 15–20 seconds. Accept 2–3 answers. You will likely hear:
- "It searched something"
- "It wrote a file"
- "It made decisions"

Then say:

> "You just watched a language model use tools to complete a multi-step task on its own. That's an agent. In the next 45 minutes I want to show you exactly how that works — and by the end you'll be able to build one yourself."

### Speaker Notes
- Do NOT explain what an agent is yet. The mystery is the hook.
- If the agent fails (network issue), pivot: "That failure is actually useful — let's talk about why." Then show the saved file from a previous run and walk through what it would have done.
- Keep this section tight. The energy is "something just happened, let's figure out what."

### Transition Cue
> "Before we go any deeper into the code, I want to give you the mental model that makes all of this click."

---

## SECTION 2 — Mental Model: LLM vs Agent `[5:00 – 15:00]`

**Goal:** Give students a durable conceptual framework. This is the core 10 minutes.

### Talking Point 1: What's Wrong with the Chatbot Model (2 min)

> "Most of you have used ChatGPT or Claude as a chatbot. You type a question. It answers. You type another question. It answers. That's a **one-shot request-response loop**. You're the agent — you decide what to do next."

Ask the room:
> **"What are the limits of that model? What can't a chatbot do that a human assistant could?"**

Expected answers: "it can't remember between sessions," "it can't look things up," "it can't take actions."

Then say:
> "Exactly. A chatbot is stateless, passive, and isolated. An agent is none of those things."

### Talking Point 2: The Agent Loop — Perceive → Reason → Act (4 min)

Draw or reveal this loop on the slide:

```
[ PERCEIVE ]  ←──────────────────────────────┐
     │                                        │
     ▼                                        │
[ REASON  ]  (LLM: "Given what I know, what │
     │        should I do next?")             │
     ▼                                        │
[  ACT    ]  (Call a tool, write a file,     │
     │        send a request...)              │
     ▼                                        │
[ OBSERVE ]  (Tool result comes back) ───────┘
```

> "This is the loop. The LLM isn't 'running' the agent — the LLM is the reasoning step inside a loop that your code runs. The LLM decides what to do. Your code does it."

**Key analogy to say out loud:**
> "Think of the LLM as a very smart intern who can only communicate by writing memos. You give them a task. They write back 'please look up X for me.' You look it up. You hand them the answer. They write back 'now save this summary.' You save it. They write back 'done.' The intern never touched the keyboard — your code did. The intern just reasoned."

### Talking Point 3: What Makes It Agentic (4 min)

Write these three words on the board/slide:
- **Autonomy** — it completes sub-tasks without you directing each step
- **Tool use** — it can reach outside the model (search, write, call APIs)
- **Memory / state** — it carries context across multiple reasoning steps

Ask:
> **"If I give an LLM a system prompt that says 'you are a helpful assistant,' is that an agent?"**

Pause. Then:
> "No. That's still a chatbot with a costume on. The difference is the loop — does the model observe the result of its actions and decide what to do next based on that? If yes, it's an agent."

### Talking Point 4: Why Now? (1 min)

> "Function calling / tool use shipped in major APIs in 2023. Before that you'd have to parse free-form text and hope the model said 'SEARCH:' in the right place. Now the model returns structured JSON telling you exactly which tool to call and with what arguments. That reliability is what made production agents viable."

### Speaker Notes
- Write "Perceive → Reason → Act → Observe" in large letters before this section starts. Leave it visible for the rest of the workshop.
- The intern analogy consistently lands well. Use it verbatim.
- Expect a question: "Is this the same as RAG?" Answer: "RAG is one way to implement the Perceive step — giving the model context. But an agent can also act and create new information, not just retrieve existing info."

### Transition Cue
> "Okay, mental model locked. Let's make this concrete. I'm going to run three demos, each one adds one layer."

---

## SECTION 3 — Live Demo Arc `[15:00 – 35:00]`

**Goal:** Progressive disclosure — each demo adds one concept. Students should feel the "aha" at each step.

> Full step-by-step instructions for each demo are in `DEMO_SCRIPT.md`. Summaries below.

### Demo 1: "The Smart Autocomplete Illusion" `[15:00 – 20:00]` (5 min)

**What:** Paste a complex multi-step task into Claude.ai with zero tools. Show that Claude reasons about what it *would* do but can't actually do it.

**Concept:** LLMs reason but don't act. Reasoning ≠ action.

**What to say after:**
> "Claude wrote a beautiful plan. It even wrote fake search results it imagined. But nothing actually happened. No file was saved. No search was run. Without the loop, it's still just autocomplete — very smart autocomplete, but autocomplete."

Ask audience:
> **"What would we need to add to make this actually work?"**

Expected: "a way to run the search," "some code to execute the steps."

### Demo 2: "Giving the Model Hands" `[20:00 – 28:00]` (8 min)

**What:** In Claude.ai, paste a system prompt that defines tools in plain English. Ask Claude to complete a task. Manually play the role of the tool executor — copy Claude's "tool call" response, paste a fake result back.

**Concept:** Tool use is just structured communication. The model tells you what it wants. You (or your code) does it.

**What to say while doing it:**
> "Right now, I'm playing the role of `agent.py`. Claude told me what tool to call. I ran it. Now I'm handing the result back. This is the exact loop — I'm just doing it by hand."

Ask audience:
> **"What's the difference between me doing this manually and the code doing it?"**

Expected: "speed," "scale," "it can run unsupervised."

### Demo 3: "The Real Agent" `[28:00 – 35:00]` (7 min)

**What:** Run `python agent.py` live in the terminal with a custom task. Walk through each printed line as it appears.

**Concept:** Everything just shown, automated. Perception, reasoning, action, observation — all in the loop.

**What to narrate as it runs:**
- When Claude's reasoning appears: "This is the Reason step — Claude deciding what to do next."
- When a tool call appears: "This is the Act step — our code runs the tool."
- When a tool result appears: "This is the Observe step — Claude gets the result back."
- When it loops: "And now we Perceive again. New context, new decision."

After it finishes:
```bash
cat notes/summary.txt
```
> "The agent saved a file to disk. That's not a chatbot. That's a system that completed a task."

### Speaker Notes
- Keep Demo 3 to 7 minutes. If the agent runs slowly, narrate while waiting — don't let silence kill the energy.
- Have a pre-run `notes/summary.txt` as backup in case of API issues.
- If a student asks "why didn't it use calculate?" — "Great catch. The task didn't need math. Claude only calls tools it needs. If we gave it a task that involved numbers, it would."

### Transition Cue
> "Now that you've seen it work, let's open the code so you understand exactly how to replicate this."

---

## SECTION 4 — Repo Walkthrough `[35:00 – 45:00]`

**Goal:** Students leave knowing where every piece of the agent lives and how to modify it.

### Open `agent.py` in editor (or terminal: `cat agent.py`)

**Walk through in order, 2 min per concept:**

#### 4a. The TOOLS list (2 min)
Point to the `TOOLS` list.
> "This is the menu Claude reads. It's a JSON schema — name, description, and what arguments each tool expects. Claude uses this to decide which tool to call and what to pass it. **The description matters** — write it like documentation for a smart colleague, not a computer."

Ask:
> **"If you wanted to add an email-sending tool, what would you put here?"**

Let one student answer. Validate it.

#### 4b. The Tool Dispatch (1 min)
Point to `TOOL_DISPATCH`.
> "This maps the tool name Claude returns to the Python function that actually runs it. String → function. When Claude says 'call search_web,' this dict finds `search_web` in tools.py and calls it."

#### 4c. The Agent Loop — `run_agent()` (4 min)
Walk through `run_agent()` step by step:
1. "We send the task to Claude."
2. "Claude responds. We check `stop_reason`."
3. "If `end_turn` — done."
4. "If `tool_use` — extract the tool call, run it, append the result, loop."
5. "After MAX_ITERATIONS, we stop regardless."

> "That's the whole agent. It's ~60 lines. The complexity isn't in the loop — the complexity is in what the tools do and how you design them."

#### 4d. Open `tools.py` (3 min)
Scroll to `search_web`, `save_note`, `calculate`.
> "Each tool is just a Python function that takes arguments and returns a string. The agent doesn't care how complex the implementation is — it just needs a string result to hand back to Claude."

Point to `calculate` and `_eval_node`:
> "Note we're not using Python's built-in `eval()`. That would be dangerous — Claude could theoretically ask it to evaluate `os.system('rm -rf /')`. We use Python's AST parser and only allow numeric operations. Security matters in agentic systems because the model controls what gets executed."

### Speaker Notes
- Keep this section moving. You're not teaching them to memorize the code — you're teaching them to have confidence that they *could* write this.
- If time is tight, skip `calculate` internals and just say "we use safe parsing, the README has details."
- Recommended: bump the font size to 18+ before this section so everyone can read from the back.

### Transition Cue
> "One last thing before Q&A — I want to show you where this is going, because a single agent is just the beginning."

---

## SECTION 5 — Multi-Agent Concepts + Where It's Going + Q&A `[45:00 – 50:00]`

**Goal:** Zoom out. Plant seeds for further exploration. Open questions.

### Multi-Agent Concept (2 min)

**One analogy:**
> "Imagine you're running a research report. One agent searches the web and extracts facts. A second agent critiques those facts for bias or errors. A third agent formats and writes the final document. None of them do the whole task — they're specialists who hand work to each other. That's a multi-agent system. You get parallelism, specialization, and the ability to have one agent check another's work."

**One diagram description (draw or show on slide):**
```
User Task
    │
    ▼
[Orchestrator Agent]
    ├──► [Research Agent]  → hands findings to →
    │                                            [Writer Agent] → Output
    └──► [Critic Agent]   → hands feedback to →
```

> "The orchestrator doesn't do the work. It delegates, collects, and synthesizes. This is how production systems like customer support pipelines or coding assistants are built today."

### Where It's Going (1 min)

> "Three things to watch:
> 1. **Long-horizon tasks** — agents that run for hours or days, not seconds.
> 2. **Computer use** — agents that control a browser or desktop UI, not just APIs.
> 3. **Agent-to-agent protocols** — standardized ways for agents built by different companies to hand tasks to each other."

> "The starter repo you're cloning today is a toy, but the loop is the same loop that powers production systems at scale. The complexity is in the tooling, the memory, and the orchestration — not the core idea."

### Q&A (2 min)

**Seed questions if the room is quiet:**
- "What task would you want an agent to do for you that you currently do manually?"
- "What could go wrong if an agent had too many powerful tools with no human in the loop?"
- "How would you test an agent? How do you know it did the right thing?"

### Final Close

> "Clone the repo, swap in your own tools, change the default task. The only way to really learn this is to run it and break it. Thank you."

---

## TIMING SUMMARY

| Section | Duration | Cumulative |
|---|---|---|
| 1. Hook / Opening Demo | 5 min | 0:05 |
| 2. Mental Model | 10 min | 0:15 |
| 3. Live Demo Arc (3 demos) | 20 min | 0:35 |
| 4. Repo Walkthrough | 10 min | 0:45 |
| 5. Multi-Agent + Q&A | 5 min | 0:50 |

**Buffer strategy:** If demos run long, cut Section 5 to the analogy + one "where it's going" bullet + Q&A. Never cut the demos — that's where learning happens.
