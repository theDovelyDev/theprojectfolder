# Budget-Conscious Research Agent

A LangGraph research agent with a built-in budget kill switch that interrupts execution, 
reports cost to the user, and asks for permission before spending more.

## The FinOps Angle

The same pattern that controls a $0.05 research budget is the same pattern that controls 
$50,000 AI inference budgets at enterprise scale.

## Tech Stack

- Python, LangGraph, Anthropic API (Claude Haiku + Sonnet), Tavily Search, AWS Fargate

## Architecture
```
User Query → Router (Haiku) → Researcher (Sonnet + Tavily) → Budget Check → Loop or Stop
```

## Setup

1. Clone the repo
2. Copy `.env.example` to `.env` and add your API keys
3. Install dependencies: `pip install -r requirements.txt`

## Status 🚧 In progress

| Phase | Status |
|-------|--------|
| Phase 1 — Environment setup | ✅ Complete |
| Phase 2 — LangGraph concepts | ✅ Complete |
| Phase 3 — Router node | ✅ Complete |
| Phase 4 — Budget kill switch | ✅ Complete |
| Phase 5 — Testing + CLI | ✅ Complete |
| Phase 6 — Fargate deployment | ✅ Complete |
| Phase 7 — Documentation + Portfolio | 🚧 In Progress |

## Live Endpoint

CARA is deployed to AWS Fargate. Start the service by setting desired
count to 1 in ECS console, then:

```bash
# Health check
curl http://<FARGATE_PUBLIC_IP>:8080/health

# Research query
curl -X POST http://<FARGATE_PUBLIC_IP>:8080/research \
  -H "Content-Type: application/json" \
  -d '{"query": "Your question here"}'
```

Note: Service is set to desired count 0 when not in use to minimize cost.
Auto-stop guardrails will stop the service automatically if left running idle.