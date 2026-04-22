# Building a Budget-Conscious Research Agent with LangGraph

## A Developer's Journey from Concept to Production

---

## 📝 Development Log

**Project:** Budget-Conscious Research Agent  
**Start Date:** April 7, 2026  
**End Date:** [END DATE]  
**Total Hours:** ~2 hours (Phase 1)  
**Final Cost:** $0.00 (so far)

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Why I Built This](#why-i-built-this)
3. [Development Log](#development-log)
4. [Technical Challenges & Solutions](#challenges)
5. [Key Learnings](#learnings)
6. [Results & Impact](#results)
7. [What's Next](#whats-next)

---

## Project Overview

**The Problem:** AI agents can run up API costs fast — especially research agents that loop through multiple searches. Most tutorials show you how to build the agent. Nobody shows you how to put a budget guardrail on it.

**The Solution:** A LangGraph research agent with a `check_budget()` kill switch that interrupts execution, reports cost to the user, and asks for permission before spending more.

**The FinOps Angle:** The same pattern that controls a $0.05 research budget is the same pattern that controls $50,000 AI inference budgets at enterprise scale.

**Tech Stack:**
- Python, LangGraph, Anthropic API (Claude Haiku + Sonnet), Tavily Search, AWS Fargate

**Key Metrics (Target):**
- Routing cost per query: < $0.001 (Haiku)
- Research cost per query: ~$0.02–0.04 (Sonnet)
- Budget interrupt threshold: $0.05 (configurable)
- Max iterations guardrail: 3

---

## Why I Built This

[FILL IN YOUR PERSONAL MOTIVATION]

---

## Development Log

### Phase 1: Environment Setup
**Date:** April 7, 2026
**Time Spent:** ~2 hours
**Status:** ✅ Complete

#### What I Did:
- [x] Created Anthropic API account, confirmed $20 credit balance
- [x] Created Tavily API account (free tier — 1,000 searches/month)
- [x] Added both API keys to `.env`
- [x] Created virtual environment (`venv`) and installed dependencies
  - `langgraph`, `langchain-anthropic`, `tavily-python`, `python-dotenv`
- [x] Created `README.md` with project overview and architecture summary
- [x] Created `tagging-dictionary.md` for Project 2 tag values
- [x] Created `setup.sh` with Project 2 environment variables
- [x] Created `verify-tag-audit.sh` for on-demand tag scanning
- [x] Created `fix-tags.sh` for remediating non-compliant resources
- [x] Updated `TAGGING_STRATEGY.md` with Project 2 entry
- [x] Extended DocFlow `TagAuditFunction` to cover Project 2 resources
- [x] Confirmed weekly email audit active and reporting correctly
- [x] Tagged stray DocFlow resources (DynamoDB, SNS) surfaced by audit
- [x] Committed and pushed to `dev` and `main` in both repos
- [x] Tagged `phase-1-complete`

#### Challenges Faced:
```
Challenge 1: pip install ran in project folder instead of venv
- Issue: Dependencies installed globally, not in isolated environment
- Solution: Deactivated, uninstalled packages, created venv, reinstalled
- Lesson: Always activate venv BEFORE running pip install
- Command: python -m venv venv && source venv/Scripts/activate

Challenge 2: Anthropic API page error on first credit purchase
- Issue: Page kicked an error mid-checkout — unclear if charge went through
- Solution: Checked Billing page to confirm $20 credit registered correctly
- Lesson: Always verify billing page after any payment error before retrying
```

#### What Worked Well:
```
Success 1: Extended existing TagAuditFunction instead of rebuilding
- Recognized that DocFlow's Lambda already scanned all resources account-wide
- Updated function to bucket resources by project and report per-project
- No new infrastructure needed — pure code change
- FinOps win: reuse over rebuild

Success 2: Tag audit immediately surfaced 3 untagged DocFlow resources
- DynamoDB table and SNS topic tagged and remediated same session
- UUID stale reference investigated and confirmed non-existent
- 100% compliance restored across both projects
```

#### Cost Tracker:
- Anthropic API: $0.00 (credits purchased, not yet used)
- Tavily: $0.00 (free tier)
- AWS: $0.00
- Running total: $0.00

---

### Phase 2: LangGraph Concepts
**Date:** April 7, 2026
**Time Spent:** ~1 hour
**Status:** ✅ Complete

#### What I Did:
- [x] Reviewed State, Nodes, and Edges mental model
- [x] Mapped LangGraph concepts to Budget Agent architecture
- [x] Completed knowledge check exercises using customer support and loan agent scenarios

#### Notes:
**State** — like a temp table passed between agents, populated column by column.
Each node reads what it needs and writes back its results. Not where data lives —
what the agent carries with it through the graph.

**Nodes** — one job only. Reads from state, writes back to state. If a node can't
complete its job, it writes a failure signal (None, error message, or a flag like
budget_exceeded: True) so the graph knows how to respond.

**Edges** — a dichotomous key. Fixed edges always go to the same next node.
Conditional edges ask a yes/no question and branch based on the answer.
The budget gate is a conditional edge: cost < $0.05 → keep going, cost ≥ $0.05 → stop.

---

### Phase 3: Router Node
**Date:** April 7, 2026
**Time Spent:** ~1 hour
**Status:** ✅ Complete

#### What I Built:
- [x] Defined AgentState TypedDict in graph.py — the state dictionary 
      that flows through every node
- [x] Built router_node using Claude Haiku for cheap query classification
- [x] Built route_decision edge function — reads state["route"] and tells
      LangGraph where to go next
- [x] Built chat_responder_node for non-research queries
- [x] Wired full graph in build_graph()
- [x] Fixed API key loading — added load_dotenv() before Anthropic client init
- [x] Tested all four routing scenarios successfully

#### Key Decisions:
- Claude Haiku chosen for routing — cheapest model, one-word output, 
  classification doesn't need Sonnet-level reasoning
- System prompt defines exactly two categories: chat and research
- Edge function is separate from the node — Haiku classifies, 
  route_decision routes. Two separate jobs.

#### Cost Tracker:
- Routing cost per query: ~$0.000070 (target was <$0.001 ✅)
- Chat response cost per query: ~$0.000130
- Running total: ~$0.001

---

### Phase 4: Budget Kill Switch & Researcher Node
**Date:** April 7, 2026
**Time Spent:** ~2 hours
**Status:** ✅ Complete

#### What I Built:
- [x] Built budget.py with check_budget() function and budget_gate edge
- [x] Built tools.py with Tavily search wrapper (search_web())
- [x] Added researcher_node to nodes.py — calls Tavily then Claude Sonnet
- [x] Added needs_more_research edge function to nodes.py
- [x] Wired full graph in graph.py with all four nodes and three 
      conditional edges
- [x] Tested chat and research routes end-to-end

#### Key Decisions:
- check_budget() is pure Python — no API call, no external service.
  Runs before every research loop inside the Fargate container
- budget_gate and needs_more_research are edge functions — they read 
  state and return a string, they don't do work
- Tavily chosen for search — built for LLM agents, clean output, 
  free tier covers full dev cycle
- Claude Sonnet used for research synthesis — best reasoning for 
  complex multi-source answers
- Human-in-the-loop interrupt message implemented as display only —
  full yes/no resume workflow documented as planned Phase 2 feature

#### Three Conditional Edges:
- route_decision — chat or research?
- budget_gate — budget exceeded or clear?
- needs_more_research — loop back or done?

#### Cost Tracker:
- Routing cost per query: ~$0.000070
- Research cost per query: ~$0.0049 (target was $0.02-0.04 ✅)
- Running total: ~$0.012

---

### Phase 5: Testing, CLI & Cost Tracker
**Date:** April 7, 2026
**Time Spent:** ~1 hour
**Status:** ✅ Complete

#### What I Built:
- [x] Wrote tests/test_agent.py with three test scenarios
- [x] Test 1: Chat route — confirmed cheap, correct answer
- [x] Test 2: Research route — confirmed Tavily + Sonnet firing correctly
- [x] Test 3: Budget interrupt — confirmed kill switch fires at $0.05
- [x] Named agent CARA (Cost-Aware Research Agent)
- [x] Built main.py CLI with CARA branding
- [x] Created COST_TRACKER_GUIDE.md
- [x] Built interactive cost dashboard (HTML artifact)

#### Key Decisions:
- pytest collects 0 items on run() functions — ran tests directly 
  with python -m tests.test_agent instead
- Budget interrupt test requires total_cost: 0.04999 not 0.0499 —
  router adds ~$0.000077 which tips it just over $0.05
- CARA named for portfolio and Substack recording clarity
- Cost dashboard built as simulated demo — will wire to live Fargate 
  API endpoint in Phase 6

#### Challenges:
- Budget interrupt didn't fire at 0.0499 — root cause: router runs 
  first and adds cost BEFORE budget check. Solution: start at 0.04999
  so router cost tips it over the threshold

#### Cost Tracker:
- Phase 5 testing: ~$0.015 (chat + research + interrupt tests)
- Running total: ~$0.027

---

### Phase 6: Deployment to AWS Fargate
**Date:** April 18-19, 2026
**Time Spent:** ~4 hours
**Status:** ✅ Complete

#### What I Built:
- [x] Created `app.py` — FastAPI wrapper with /research and /health endpoints
- [x] Created `Dockerfile` using python:3.11-slim base image
- [x] Populated `requirements.txt` with production dependencies only
- [x] Built CARA container image locally (Docker 29.4.0, ARM64 machine)
- [x] Tested container locally via Docker Desktop
      - Health endpoint: {"status":"ok","agent":"C.A.R.A."} ✅
      - Chat route: $0.0002 ✅
      - Research route: $0.0048 ✅
- [x] Created ECR repository `cara` in sandbox account (848747536965)
- [x] Created `budget-research-agent-dev` IAM user with least-privilege permissions
- [x] Updated `setup.sh` with `AWS_PROFILE=budget-research-agent-dev`
- [x] Rebuilt image for `linux/amd64` (Fargate default platform)
- [x] Pushed image to ECR successfully
- [x] Created ECS cluster `cara-cluster`
- [x] Created Fargate task definition `cara-task`
      - linux/x86_64, 0.25 vCPU, 0.5GB RAM
      - Environment variables set for API keys and budget config
- [x] Created and deployed `cara-service` (1 desired task)
- [x] Confirmed live endpoint responding to HTTP requests
- [x] Set desired count to 0 after testing (cost control)

#### Infrastructure Guardrails:
- [x] Created `CaraAutoStopFunction` Lambda — sets ECS desired count to 0
- [x] Created `CaraAutoStopNotifications` SNS topic for email alerts
- [x] Created `CaraAutoStopLambdaRole` IAM role with least privilege
- [x] Created two CloudWatch alarms wired directly to Lambda:
      - `CARA-Idle-CPU-AutoStop` — CPU < 5% for 30 consecutive minutes
      - `CARA-2Hour-AutoStop` — Memory < 5% for 2 consecutive hours
- [x] Created architecture diagram for guardrails system

#### Challenges Faced:
- **Challenge 1**: Platform mismatch — ARM64 vs AMD64
    - Error: ECS Deployment Circuit Breaker triggered
    - Root cause: Image built on ARM64 machine, Fargate defaults to linux/x86_64
    - Solution: Rebuilt with --platform linux/amd64 flag
    - Lesson: Always specify --platform linux/amd64 for Fargate deployments regardless of local machine architecture

- **Challenge 2**: ECR created in wrong AWS account
    - Created repo in hosting account (102587257710) instead of sandbox (848747536965)
    - Solution: Deleted repo, recreated in correct account
    - Lesson: Always verify account switcher before creating resources

- **Challenge 3**: Missing ECR permissions on IAM user
    - Error: AccessDeniedException on GetAuthorizationToken
    - Solution: Added AmazonEC2ContainerRegistryFullAccess to user group
    - Lesson: ECR auth requires explicit GetAuthorizationToken permission

- **Challenge 4**: IAM inline policy scoped too narrowly
    - Error: AccessDenied on CreateRole for CaraAutoStopLambdaRole
    - Root cause: Policy Resource only allowed TagAuditLambdaRole
    - Solution: Added CaraAutoStop* to Resource list
    - Lesson: Per-project IAM policies need to be scoped to project patterns not specific resource names

#### Key Decisions:
- **AMD64 over ARM64** — Fargate default, avoids platform complexity in dev
- **CloudWatch → Lambda directly** — cleaner than CloudWatch → SNS → Lambda
- **Two alarm types** — CPU idle catches forgotten containers, memory+time
  catches long-running sessions that aren't actively being used
- **Desired count = 0 not service delete** — preserves configuration,
  easy to restart, costs $0 when idle

#### Docker Desktop Lesson:
- Docker Desktop is an underrated local testing tool for containerized agents:
    - Stats tab: watch CPU/memory spike during research loops in real time
    - Logs tab: uvicorn output and request logs without CloudWatch
    - Run button: set env vars visually without --env-file flag
  - This was the first containerization project — Desktop made debugging significantly faster than CLI alone.

#### Cost Tracker:
- ECR storage: ~$0.01
- Fargate (dev testing): ~$0.05
- CloudWatch alarms: $0.00 (free tier)
- Lambda invocations: $0.00 (free tier)
- Running total: ~$0.09

---

### Phase 7: CARA Live UI + Cost Dashboard
**Date:** April 20-21, 2026
**Time Spent:** ~4 hours
**Status:** ✅ Complete

#### What I Built:
- [x] Created `content/cara.html` — single page UI with chat + dashboard
- [x] Set up API Gateway (HTTP API) as stable HTTPS endpoint
      - Routes: GET /health, POST /research
      - Replaces raw Fargate IP — stable URL across task restarts
- [x] Configured CORS at both FastAPI and API Gateway level
- [x] Deployed to theprojectfolder.com/content/cara.html
- [x] Wired SNS trigger to CaraAutoStopFunction
      - Confirmed auto-stop working end to end
      - CloudWatch alarm → SNS → Lambda → ECS desired count = 0
- [x] Fixed chat_responder_node missing route in return dict
- [x] Light theme with amber accents matching simulated dashboard style


#### Challenges Faced:
- **Challenge 1**: API Gateway returning 404
    - Root cause: Stage URL includes /prod prefix — correct URL is https://67bw5r3zvj.execute-api.us-east-1.amazonaws.com/prod/health
    - Lesson: HTTP API stages append stage name to the base URL

- **Challenge 2**: CORS blocking POST requests
    - Health check (GET) passed but research queries (POST) blocked
    - Root cause: API Gateway has its own CORS settings separate from FastAPI
    - Solution: Configure CORS directly in API Gateway console
    - Lesson: CORS must be configured at every layer — FastAPI AND API Gateway

- **Challenge 3**: Auto-stop Lambda had no trigger
    - Fargate ran for ~9 hours overnight despite CPU alarm firing
    - Root cause: CloudWatch alarm action didn't properly wire to Lambda
    - Solution: SNS subscription + Lambda permission via console
    - Confirmed working: manual SNS publish stopped Fargate immediately

- **Challenge 4**: Chat route badge showing query text
    - Root cause: chat_responder_node not returning route in state
    - Solution: Added route: state["route"] to return dict

#### Key Decisions:
- **API Gateway over ALB** — stable HTTPS endpoint at near-zero cost
  for controlled demo traffic. ALB reserved for if CARA goes fully public.
- **SNS → Lambda over direct CloudWatch → Lambda** — more reliable,
  SNS subscription model is the correct AWS pattern
- **Light theme** — consistent with portfolio aesthetic preferences,
  amber accents preserve CARA brand identity
#### Architecture Decision: API Gateway + ALB vs Manual IP Updates

**The Problem:**
API Gateway provides a stable HTTPS endpoint for users, but its backend
integrations are hardcoded to the Fargate task's public IP. Every time
Fargate restarts (new deployment, auto-stop, scale event), the task gets
a new IP — breaking the API Gateway → Fargate connection silently.

**Options Considered:**

| Option | Cost | Complexity | Stability |
|--------|------|------------|-----------|
| Manual IP update each session | $0.00 | Low | ❌ Breaks on restart |
| Application Load Balancer (ALB) | ~$1.44/3 days | Medium | ✅ Always stable |
| AWS Service Discovery | $0.00 | High | ✅ Always stable |
| Elastic IP + NAT Gateway | >$1.44 | High | ✅ Always stable |

**Decision: Add ALB for the 48-hour live window**

$1.44 is the cost of making CARA reliably accessible to LinkedIn audience
without requiring manual intervention during the live window. Without it,
a single Fargate restart during the 48 hours would silently break the
demo for all visitors.

**The FinOps Lesson:**
This is a real enterprise pattern at scale. The question is never "does
infrastructure cost money?" It's "does the cost justify the reliability
requirement?" For a no-revenue portfolio site in normal dev, manual
updates are fine. For a time-boxed public demo with a live audience,
$1.44 buys you reliability SLA. Same decision framework, different answer.

**Impact:**
- ALB added to architecture diagram in Phase 8
- API Gateway integrations updated to point to ALB DNS name
- Fargate IP changes become invisible to the stack
- Auto-stop still works — ALB routes to 0 tasks gracefully

#### Cost Tracker:
- API Gateway: $0.00 (free tier)
- Fargate (Phase 7 testing): ~$0.10
- ECR storage: ~$0.01
- Anthropic API (Phase 7 queries): ~$0.08 (verify in console)
- Tavily: $0.00 (free tier)
- **Phase 7 total: ~$0.19**
- **Project running total: ~$0.28**

---

### Phase8: Documentation & Portfolio Prep
**Date:** [DATE]
**Time Spent:** [HOURS]
**Status:** ⬜ Not Started

---

## Technical Challenges & Solutions

[Compiled at project close from phase logs above]

---

## Key Learnings

[Compiled at project close]

---

## Results & Impact

[Compiled at project close]

---

## What's Next

[Compiled at project close]

---

## Changelog

**2026-04-07** — Phase 1 complete (environment setup, tagging, venv)

---

*Part of the Project Folder portfolio — theprojectfolder.com*
*Carlandra in the Cloud · Building at the intersection of FinOps and engineering*