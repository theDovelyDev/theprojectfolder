from agent.graph import build_graph

app = build_graph()

def run(query):
    result = app.invoke({
        'query': query,
        'messages': [], 'search_results': [],
        'total_cost': 0.0, 'iteration': 0,
        'route': '', 'final_answer': '',
        'budget_exceeded': False, 'awaiting_approval': False
    })
    print(f'Query:  {query}')
    print(f'Route:  {result["route"]}')
    print(f'Cost:   ${result["total_cost"]:.4f}')
    print(f'Loops:  {result["iteration"]}')
    print(f'Answer: {result["final_answer"][:150]}...')
    print()

run('How are you today?')
run('What are the latest AWS cost optimization announcements in 2025?')