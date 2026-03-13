# Workshop Demo Script

Three progressive demos. Each one adds one layer to the mental model.

| Demo | Tool | Concept |
|---|---|---|
| 1 | Claude.ai (no tools) | Reasoning without action |
| 2 | Claude.ai (manual tool simulation) | Tool use as structured conversation |
| 3 | `python agent.py` (live terminal) | The full automated loop |

---

## DEMO 1 — "The Reasoning Illusion"

**Duration:** 5 minutes
**Tool:** Browser → claude.ai
**Concept:** LLMs can reason about actions but can't take them without a loop.

### Setup (before demo)
- Open claude.ai in a browser tab
- Make sure you're in a **New conversation** with no system prompt
- Bump the font size so students can read from the back (`Ctrl+` or browser zoom to 125%)

### Exact Prompt to Paste

Copy this entire block and paste it as your message:

```
I want you to complete this task:

1. Search the web for "what is agentic AI"
2. Summarize the results in exactly 3 bullet points
3. Save the summary to a file called summary.txt

Please complete all three steps.
```

### What Will Happen
Claude will respond with something like:
- A plan: "Sure! Here's what I'll do..."
- Hallucinated search results: "Based on my search, here are the key points..."
- A fake file save: "I've saved the summary to summary.txt"

None of this will actually happen. No search was run. No file exists.

### What to Say While It Runs

While Claude is generating:
> "Watch what it does. It's reasoning through the task. Notice it's not hesitating — it knows what it would do."

After it finishes:
> "Beautiful. It wrote a plan, it searched, it summarized, it saved the file. Except — none of that happened. Let me show you."

Open a terminal. Type:
```bash
ls notes/
```
No file. Or if the directory doesn't exist:
```bash
ls: cannot access 'notes/': No such file or directory
```

> "No file. Claude narrated a plan so convincingly it looked like action. This is the reasoning illusion. The model can think about doing something without actually doing it. The gap between reasoning and action is exactly what the agent loop closes."

### What to Point Out

1. **Claude hallucinated search results.** It doesn't know what DuckDuckGo would return, so it made up plausible-sounding results. This is not deception — it's the model doing what it's trained to do: generate the most likely next token.

2. **The file save is pure fiction.** Claude has no filesystem access. It wrote "I've saved the file" the same way it writes anything — because those tokens are plausible given the context.

3. **This is not a bug.** A language model's job is to generate text. Making it an agent requires external architecture — the loop, the tools, the execution layer.

### Transition to Demo 2

> "So what changes? We need to give the model a way to tell us what it wants, and then we need to actually do it. Let me show you the first version of that — by hand."

---

## DEMO 2 — "Giving the Model Hands"

**Duration:** 8 minutes
**Tool:** Browser → claude.ai (with system prompt)
**Concept:** Tool use is structured communication. You manually play the role of the executor.

### Setup (before demo)
- Open a **new Claude.ai conversation**
- Open the system prompt panel (usually a settings icon or "System prompt" section in Claude.ai)
- You will paste the system prompt below before sending any messages

### System Prompt to Paste

Paste this into the **System Prompt** field (not the message box):

```
You are a task-completion agent. You have access to three tools:

1. search_web(query: str)
   - Searches DuckDuckGo and returns a text summary
   - Use when you need factual information

2. save_note(text: str, filename: str)
   - Saves text to a local file
   - Use to persist any output or summary

3. calculate(expression: str)
   - Evaluates a math expression like "2 + 2"
   - Use for any numeric calculation

IMPORTANT: When you want to use a tool, respond ONLY with:
TOOL_CALL: tool_name(arg1, arg2)

Wait for the tool result before continuing.
When the task is complete, respond with:
DONE: [brief summary of what was accomplished]

Do not narrate. Do not explain. Just call tools and complete the task.
```

### Initial User Message to Send

```
Research what agentic AI is, summarize it in 3 bullet points,
and save the summary to summary.txt
```

### What Will Happen (and How to Respond)

**Claude's first response will be something like:**
```
TOOL_CALL: search_web("what is agentic AI")
```

**You say to the audience:**
> "Claude just told me what it wants. It doesn't have hands — it can't search. But it knows what needs to happen, so it asked. Now I'm going to play the role of the agent.py script."

**Type this as your next message (simulating a search result):**
```
Tool result: Agentic AI refers to artificial intelligence systems that
can autonomously plan and execute multi-step tasks to achieve goals.
Unlike traditional AI models that respond to single queries, agentic
AI systems use a loop of perceiving context, reasoning about next steps,
taking actions via tools, and observing results. Key applications include
autonomous research assistants, coding agents, and customer service
automation. (Source: DuckDuckGo)
```

**Claude's second response will be something like:**
```
TOOL_CALL: save_note("• Agentic AI autonomously plans and executes multi-step tasks\n• Uses a loop: perceive, reason, act, observe\n• Applications: research assistants, coding agents, automation", "summary.txt")
```

**You say:**
> "Now it wants to save a file. Again, I'll play the executor."

**Type this as your next message:**
```
Tool result: Note saved to notes/summary.txt (187 characters)
```

**Claude's final response will be:**
```
DONE: Researched agentic AI, created a 3-bullet summary,
and saved it to summary.txt.
```

### What to Say After

> "I just did manually what agent.py does automatically. Claude told me what tool to call. I ran it — or pretended to. I passed the result back. Claude decided what to do next based on that result. That's the loop. I was the loop."

**Ask the audience:**
> "What's the difference between me doing this by hand and the code doing it?"

Wait for answers. Expected: "speed," "scale," "can run without me."

> "Exactly. The protocol is identical. The only difference is automation. agent.py is a for-loop with a dictionary. The intelligence is entirely in Claude."

### What to Point Out

1. **The system prompt is the tool manifest.** Claude didn't know these tools existed until we told it. The description is what determines when and how Claude uses each tool.

2. **Structured output makes this automatable.** Because Claude responded with `TOOL_CALL: tool_name(args)` we could parse that. In the real SDK, this is handled with typed JSON — no parsing needed.

3. **Claude waits for confirmation.** After each tool call, Claude stopped and waited. It didn't assume what the result would be. This is the observation step — the agent updates its understanding based on what actually happened.

### Transition to Demo 3

> "That was the protocol. Now let's run the actual code and watch it do all of that automatically."

---

## DEMO 3 — "The Real Agent"

**Duration:** 7 minutes
**Tool:** Terminal → `python agent.py`
**Concept:** The full automated loop — the same protocol, running in code.

### Setup (before demo)
- Terminal is open in the `repo/` directory
- `.env` file exists with a valid `ANTHROPIC_API_KEY`
- Previous `notes/summary.txt` from any prior run has been deleted:
  ```bash
  rm -f notes/summary.txt
  ```
- Font size bumped so students can read (terminal font 16+)

### Commands to Run

**Step 1 — Show what's in the repo:**
```bash
ls -la
```
Say: "Here's the whole thing. agent.py, tools.py, a .env file for the API key, and a README."

**Step 2 — Show the default task (optional, for curious audiences):**
```bash
head -10 agent.py
```
Say: "The default task is baked in at the top. We can also pass our own task as an argument."

**Step 3 — Run the agent:**
```bash
python agent.py
```

### What to Narrate While It Runs

The agent will print output as it runs. Narrate each section as it appears:

**When you see `TASK:` printed:**
> "This is the task being sent to Claude. The loop starts now."

**When you see `[Claude's Reasoning]`:**
> "This is the Reason step. Claude is deciding what to do based on the task and whatever it knows so far. Read it — it's actual reasoning, not a template."

**When you see `[Tool Call]`:**
> "The Act step. Claude has decided to call a tool. Our code intercepts this — extracts the tool name and arguments — and runs the Python function."

**When you see `[Tool Result]`:**
> "The Observe step. The result of the tool call. Claude will see this on the next iteration and use it to decide what to do next."

**When the loop iterates (Iteration 2, 3...):**
> "Back to the top. New context — Claude now has the search result. New decision."

**When you see `Agent finished — task complete.`:**
> "Claude returned `end_turn` — it decided the task was done. The loop exits cleanly."

### After the Agent Finishes

```bash
cat notes/summary.txt
```

> "There's the file. The agent searched the web, synthesized a summary, and wrote it to disk — autonomously, in the time it took to run. That's not a chatbot."

**Optional — run a custom task:**
```bash
python agent.py "What is 2 to the power of 10? Calculate it and save the result to math_note.txt"
```

Watch the agent use `calculate` instead of `search_web`. Narrate:
> "Different task, different tool choice. Claude reads the task, looks at the tool menu, and picks the right tool. No hardcoded routing — pure reasoning."

### What to Point Out

1. **The agent decides which tools to use.** You didn't write `if "search" in task: search_web()`. Claude reads the task, reads the tool descriptions, and figures it out. Change the task, the tool choices change.

2. **Every step is visible.** The print statements in `agent.py` are intentional — this is teaching code. In production you'd log these to a structured system, but the logic is the same.

3. **The loop is the same one from Demo 2.** The only difference is that `agent.py` is playing the role you played manually. The Claude API, the tool schema, the result passing — identical.

4. **MAX_ITERATIONS is a safety net.** If something goes wrong or the task is open-ended, the agent won't run forever. This is a simple version of what production systems handle with more sophisticated termination conditions.

### If Something Goes Wrong

| Problem | What to say | What to do |
|---|---|---|
| API key error | "Let me grab the key — this happens" | Fix `.env`, re-run |
| Search returns no results | "DuckDuckGo's instant API is conservative — Claude will reason around it" | Re-run with a more specific task |
| Agent hits MAX_ITERATIONS | "The agent hit its safety cap — interesting, let's look at why" | Show the partial output, discuss what Claude tried |
| No internet | "Let's use the pre-recorded run" | Show backup `notes/summary.txt`, narrate from the OUTLINE |

---

## POST-DEMO: HOW TO GET THE REPO

After Demo 3, show this on screen:

```bash
# Clone and run in under 10 minutes:
git clone https://github.com/belmont-bhagat/daisy-workshop.git
cd repo
pip install anthropic python-dotenv requests
cp .env.example .env
# Edit .env — add your key from console.anthropic.com
python agent.py
```

> "Clone it, add your API key, change the tools to do something you care about. That's the whole exercise."
