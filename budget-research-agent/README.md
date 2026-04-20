# C.A.R.A. — Cost-Aware Research Agent

A LangGraph research agent with a built-in budget kill switch that interrupts 
execution, reports cost to the user, and asks permission before spending more.

> "Most AI agent tutorials teach you how to build the agent. Nobody teaches you 
> how to stop it from running up your bill. I built one with a $0.05 kill switch."

---

## The Problem

AI agents can run up API costs fast — especially research agents that loop through 
multiple searches. Most tutorials show you how to build the agent. Nobody shows you 
how to put a budget guardrail on it.

## The Solution

CARA uses a `check_budget()` kill switch that runs before every research loop. 
When the threshold is hit, the agent stops, reports what it found, and asks 
permission to continue.

## The FinOps Angle

The same pattern that controls a $0.05 research budget is the same pattern that 
controls $50,000 AI inference budgets at enterprise scale.

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Routing cost per query | ~$0.000070 (Claude Haiku) |
| Research cost per query | ~$0.005 (Tavily + Claude Sonnet) |
| Budget kill switch threshold | $0.05 (configurable) |
| Max research iterations | 3 (configurable) |
| Total dev cost | ~$0.09 |

---

## Architecture
User Query
↓
Router (Claude Haiku) — chat or research?
├── chat → Chat Responder → Answer
└── research → Budget Check
├── exceeded → Interrupt message + partial results
└── clear → Researcher (Tavily + Claude Sonnet)
↓
needs more research?
├── yes → Budget Check (loop, max 3)
└── no → Answer + cost report

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Orchestration | LangGraph |
| Router model | Claude Haiku |
| Research model | Claude Sonnet |
| Web search | Tavily Search API |
| API wrapper | FastAPI |
| Container | Docker |
| Registry | AWS ECR |
| Runtime | AWS Fargate |
| Hosting | theprojectfolder.com |

---

## Project Structure
budget-research-agent/
├── agent/
│   ├── graph.py          ← LangGraph state + graph assembly
│   ├── nodes.py          ← Router, chat responder, researcher nodes
│   ├── budget.py         ← check_budget() kill switch
│   └── tools.py          ← Tavily search wrapper
├── lambda/
│   └── auto-stop/        ← CloudWatch auto-stop Lambda
├── tests/
│   └── test_agent.py     ← Three test scenarios
├── app.py                ← FastAPI wrapper for Fargate
├── Dockerfile
├── main.py               ← CLI interface
├── requirements.txt
└── .env.example

---

## How the Kill Switch Works

`check_budget()` is a pure Python function — no API call, no cost. It runs 
before every research loop and checks `total_cost` in agent state against 
`MAX_BUDGET`.

When the threshold is hit:
Budget threshold of $0.05 reached after 1 research loop(s).
Total spent: $0.0501
Results so far:

[partial search results]

Would you like to spend another $0.05 to continue? (yes/no)

---

## Sample Output

```bash
$ python main.py

==================================================
  C.A.R.A. — Cost-Aware Research Agent
  kill switch: $0.05 | max loops: 3
==================================================

Ask CARA (or 'quit'): What are the latest AWS cost optimization tools in 2025?

[Router] Classifying query: 'What are the latest AWS cost optimization tools in 2025?'
[Router] Route: research | Cost: $0.000076
[Budget] Total cost so far: $0.0001 / $0.05
[Researcher] Starting research loop 1
[Researcher] Got 3 results from Tavily
[Researcher] Cost this loop: $0.004794

Answer: Based on the search results, here are the latest AWS cost 
optimization announcements for 2025...

Cost: $0.0049 | Route: research | Loops: 1
```

---

## Infrastructure Guardrails

CARA includes two CloudWatch alarms that automatically stop the Fargate 
service when idle — cost guardrails on the agent AND the infrastructure 
running it.

| Alarm | Trigger | Action |
|-------|---------|--------|
| `CARA-Idle-CPU-AutoStop` | CPU < 5% for 30 minutes | Set desired count to 0 |
| `CARA-2Hour-AutoStop` | Memory < 5% for 2 hours | Set desired count to 0 |

Both alarms invoke `CaraAutoStopFunction` directly — no SNS middleman.

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/theDovelyDev/budget-research-agent.git
cd budget-research-agent

# 2. Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Git Bash on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Add your ANTHROPIC_API_KEY and TAVILY_API_KEY

# 5. Run locally
python main.py
```

---

## Live Interface

CARA is deployed at **[theprojectfolder.com/cara](https://theprojectfolder.com/cara)**

Chat interface + live cost dashboard — wired to the Fargate endpoint in real time.

---

## Cost Breakdown

| Phase | Service | Estimated | Actual |
|-------|---------|-----------|--------|
| Dev | Anthropic API | ~$4.00 | ~$0.08 |
| Dev | Tavily | $0.00 | $0.00 |
| Deploy | Fargate (dev) | ~$0.50/day | ~$0.05 |
| Deploy | ECR storage | ~$0.10 | ~$0.01 |
| **Total** | | **~$6.00** | **~$0.14** |

---

## Status

| Phase | Status |
|-------|--------|
| Phase 1 — Environment setup | ✅ Complete |
| Phase 2 — LangGraph concepts | ✅ Complete |
| Phase 3 — Router node | ✅ Complete |
| Phase 4 — Budget kill switch | ✅ Complete |
| Phase 5 — Testing + CLI | ✅ Complete |
| Phase 6 — Fargate deployment | ✅ Complete |
| Phase 7 — Live UI + Dashboard | 🚧 In Progress |

---

## Connect

- 🌍 [The Project Folder](https://theprojectfolder.com?utm_source=github&utm_medium=profile&utm_campaign=portfolio)
- 📝 [Carlandra in the Cloud — Substack](https://carlandrainthecloud.substack.com?utm_source=github&utm_medium=profile&utm_campaign=portfolio)
- 💼 [LinkedIn](https://www.linkedin.com/in/carlandra?utm_source=github&utm_medium=profile&utm_campaign=portfolio)

---

*Part of the Project Folder portfolio — theprojectfolder.com*
*Carlandra in the Cloud · Building at the intersection of FinOps and engineering*