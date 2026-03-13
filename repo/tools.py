"""
tools.py — Tool implementations for the workshop agent.
Each tool maps to a real action the agent can take in the world.
"""

import os
import ast
import operator
import requests


# ---------------------------------------------------------------------------
# Tool 1: search_web
# Uses the DuckDuckGo Instant Answer API — no API key required.
# ---------------------------------------------------------------------------

def search_web(query: str) -> str:
    """Search DuckDuckGo and return a plain-text summary of the results."""
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Prefer the main abstract if available
        abstract = data.get("Abstract", "").strip()
        if abstract:
            source = data.get("AbstractSource", "DuckDuckGo")
            return f"{abstract}\n\n(Source: {source})"

        # Fall back to the top related topic snippets
        topics = data.get("RelatedTopics", [])
        snippets = []
        for topic in topics[:5]:
            if isinstance(topic, dict) and "Text" in topic:
                snippets.append(topic["Text"])

        if snippets:
            return "\n\n".join(snippets)

        return f"No summary found for '{query}'. Try a more specific query."

    except requests.RequestException as e:
        return f"Search failed (network error): {e}"
    except Exception as e:
        return f"Search failed: {e}"


# ---------------------------------------------------------------------------
# Tool 2: save_note
# Writes text to a .txt file inside a local notes/ directory.
# ---------------------------------------------------------------------------

def save_note(text: str, filename: str) -> str:
    """Save text content to a local file in the notes/ folder."""
    # Create notes directory if it doesn't exist
    os.makedirs("notes", exist_ok=True)

    # Sanitize filename to prevent path traversal
    safe_name = "".join(c for c in filename if c.isalnum() or c in "._- ").strip()
    if not safe_name:
        safe_name = "note"
    if not safe_name.endswith(".txt"):
        safe_name += ".txt"

    path = os.path.join("notes", safe_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return f"Note saved to {path} ({len(text)} characters)"


# ---------------------------------------------------------------------------
# Tool 3: calculate
# Safely evaluates a math expression using Python's AST — no exec/eval.
# Supports: +, -, *, /, ** and parentheses. No arbitrary code execution.
# ---------------------------------------------------------------------------

# Whitelist of safe AST node types and their corresponding operators
_SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _eval_node(node):
    """Recursively evaluate a safe AST node (raises ValueError for unsafe ops)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _SAFE_OPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _SAFE_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _SAFE_OPS:
        return _SAFE_OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError(f"Unsupported operation in expression: {ast.dump(node)}")


def calculate(expression: str) -> str:
    """Safely evaluate a math expression and return the numeric result as a string."""
    try:
        tree = ast.parse(expression.strip(), mode="eval")
        result = _eval_node(tree.body)
        # Format cleanly: drop .0 for whole numbers
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(round(result, 10))
    except ZeroDivisionError:
        return "Error: division by zero"
    except ValueError as e:
        return f"Error: {e}"
    except SyntaxError:
        return f"Error: invalid expression '{expression}'"
