"""
agent.py — A minimal teaching agent using the Anthropic SDK with tool use.

The agent follows a simple loop:
  1. Send the task (and any prior history) to Claude
  2. If Claude calls a tool → execute it, append the result, loop
  3. If Claude says it's done (end_turn) → print the final answer and stop
  4. Stop after MAX_ITERATIONS regardless, to prevent runaway loops

Run it:
  python agent.py
"""

import json
import os
import sys

from anthropic import Anthropic
from dotenv import load_dotenv

from tools import search_web, save_note, calculate

# Load ANTHROPIC_API_KEY from .env file
load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL = "claude-sonnet-4-20250514"
MAX_ITERATIONS = 5  # Hard cap on reasoning loops

# Default task that runs when you execute: python agent.py
DEFAULT_TASK = (
    "Research what agentic AI is, summarize it in 3 bullet points, "
    "and save the summary to summary.txt"
)

# ---------------------------------------------------------------------------
# Tool schema — tells Claude what tools exist and what arguments they take.
# This is the "menu" Claude reads before deciding what to do.
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "name": "search_web",
        "description": (
            "Search the web using DuckDuckGo and return a plain-text summary. "
            "Use this to look up facts, definitions, or current information."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query string",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "save_note",
        "description": (
            "Save text content to a local .txt file. "
            "Use this to persist any output or summary for the user."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text content to save",
                },
                "filename": {
                    "type": "string",
                    "description": "Filename for the note, e.g. 'summary.txt'",
                },
            },
            "required": ["text", "filename"],
        },
    },
    {
        "name": "calculate",
        "description": (
            "Safely evaluate a mathematical expression and return the result. "
            "Supports +, -, *, /, ** and parentheses. Example: '(3 + 5) * 2'"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate",
                }
            },
            "required": ["expression"],
        },
    },
]

# Maps tool names to their Python implementations
TOOL_DISPATCH = {
    "search_web": lambda args: search_web(args["query"]),
    "save_note": lambda args: save_note(args["text"], args["filename"]),
    "calculate": lambda args: calculate(args["expression"]),
}

# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

client = Anthropic()


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Look up a tool by name and execute it with the given arguments."""
    if tool_name not in TOOL_DISPATCH:
        return f"Error: unknown tool '{tool_name}'"
    try:
        return TOOL_DISPATCH[tool_name](tool_input)
    except Exception as e:
        return f"Error running {tool_name}: {e}"


def run_agent(task: str) -> None:
    """
    Main agent loop. Sends the task to Claude, processes tool calls,
    and repeats until the task is done or MAX_ITERATIONS is reached.
    """
    print("\n" + "=" * 60)
    print(f"TASK: {task}")
    print("=" * 60)

    # Conversation history — grows as the agent acts and observes
    messages = [{"role": "user", "content": task}]

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n{'─' * 40}")
        print(f"  Iteration {iteration} / {MAX_ITERATIONS}")
        print(f"{'─' * 40}")

        # ── Step 1: Ask Claude what to do next ──────────────────────────────
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            tools=TOOLS,
            messages=messages,
        )

        # ── Step 2: Print any reasoning text from Claude ────────────────────
        for block in response.content:
            if hasattr(block, "text") and block.text.strip():
                print(f"\n[Claude's Reasoning]\n{block.text.strip()}\n")

        # ── Step 3: If Claude is done, print the result and exit ─────────────
        if response.stop_reason == "end_turn":
            print("\n" + "=" * 60)
            print("  Agent finished — task complete.")
            print("=" * 60 + "\n")
            return

        # ── Step 4: If Claude wants to call tools, run them ──────────────────
        if response.stop_reason == "tool_use":
            # Save Claude's response (including tool_use blocks) to history
            messages.append({"role": "assistant", "content": response.content})

            # Execute every tool Claude requested in this turn
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue

                tool_name = block.name
                tool_input = block.input
                print(f"[Tool Call]   {tool_name}({json.dumps(tool_input, ensure_ascii=False)})")

                result = execute_tool(tool_name, tool_input)

                # Truncate long results for display (full result still passed to Claude)
                display = result if len(result) <= 300 else result[:297] + "..."
                print(f"[Tool Result] {display}")

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,  # full result goes to Claude
                })

            # Add tool results to history so Claude can see what happened
            messages.append({"role": "user", "content": tool_results})

        else:
            # Unexpected stop reason — bail out gracefully
            print(f"\n[Agent] Unexpected stop reason: {response.stop_reason}. Stopping.")
            return

    # Reached the iteration cap
    print(f"\n[Agent] Reached max iterations ({MAX_ITERATIONS}). Stopping.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Allow passing a custom task as a command-line argument
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else DEFAULT_TASK
    run_agent(task)
