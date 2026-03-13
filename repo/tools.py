"""
tools.py — Tool implementations for the workshop agent.
Each tool maps to a real action the agent can take in the world.
"""

import os
import ast
import operator
from ddgs import DDGS


# ---------------------------------------------------------------------------
# Tool 1: search_web
# Uses the duckduckgo-search package — no API key required.
# Returns the top 3 result snippets joined as plain text.
# ---------------------------------------------------------------------------

def search_web(query: str) -> str:
    """Search DuckDuckGo and return plain-text snippets from the top results."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return f"No results found for '{query}'."

        # Format each result as: Title\nSnippet\nURL
        parts = []
        for r in results:
            parts.append(f"{r.get('title', '')}\n{r.get('body', '')}\n{r.get('href', '')}")

        return "\n\n---\n\n".join(parts)

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
