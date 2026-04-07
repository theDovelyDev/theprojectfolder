import os
from dotenv import load_dotenv
load_dotenv()

MAX_BUDGET = float(os.getenv("MAX_BUDGET", "0.05"))

def check_budget(state: dict) -> dict:
    """
    The kill switch. Runs before every research loop.
    Returns updated state with budget_exceeded flag.
    """
    total_cost = state.get("total_cost", 0.0)
    iteration  = state.get("iteration", 0)
    max_iter   = int(os.getenv("MAX_ITERATIONS", "3"))

    print(f"[Budget] Total cost so far: ${total_cost:.4f} / ${MAX_BUDGET}")

    # Check 1: Budget exceeded
    if total_cost >= MAX_BUDGET:
        print(f"[Budget] 🛑 Threshold reached. Interrupting.")
        return {
            "budget_exceeded": True,
            "awaiting_approval": True,
            "final_answer": (
                f"Budget threshold of ${MAX_BUDGET} reached after {iteration} research loop(s).\n"
                f"Total spent: ${total_cost:.4f}\n\n"
                f"Results so far:\n{_summarize_results(state)}\n\n"
                f"Would you like to spend another ${MAX_BUDGET} to continue? (yes/no)"
            )
        }

    # Check 2: Max iterations reached
    if iteration >= max_iter:
        print(f"[Budget] 🛑 Max iterations ({max_iter}) reached.")
        return {
            "budget_exceeded": True,
            "awaiting_approval": False,
            "final_answer": (
                f"Reached maximum research loops ({max_iter}).\n"
                f"Total spent: ${total_cost:.4f}\n\n"
                f"Here's what I found:\n{_summarize_results(state)}"
            )
        }

    # All clear — continue research
    return {"budget_exceeded": False}


def _summarize_results(state: dict) -> str:
    """Format search results for the interrupt message."""
    results = state.get("search_results", [])
    if not results:
        return "No results collected yet."
    return "\n".join(f"- {r}" for r in results)


def budget_gate(state: dict) -> str:
    """Edge function: routes based on budget check result."""
    if state.get("budget_exceeded"):
        return "end"
    return "researcher"