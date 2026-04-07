from agent.graph import build_graph
from dotenv import load_dotenv
load_dotenv()

app = build_graph()

def run(query):
    return app.invoke({
        'query': query,
        'messages': [], 'search_results': [],
        'total_cost': 0.0, 'iteration': 0,
        'route': '', 'final_answer': '',
        'budget_exceeded': False, 'awaiting_approval': False
    })

if __name__ == "__main__":
    print("=" * 50)
    print("  CAP — Cost-Aware Processing Agent")
    print("  kill switch: $0.05 | max loops: 3")
    print("=" * 50)
    print()

    while True:
        query = input("Ask CAP (or 'quit'): ").strip()
        if not query:
            continue
        if query.lower() == 'quit':
            print("CAP out.")
            break
        result = run(query)
        print(f"\nAnswer: {result['final_answer']}")
        print(f"Cost: ${result['total_cost']:.4f} | Route: {result['route']} | Loops: {result['iteration']}")
        print()