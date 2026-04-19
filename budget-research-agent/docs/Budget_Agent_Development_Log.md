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
**Date:** April 18, 2026
**Time Spent:** In progress
**Status:** 🚧 In Progress

#### What I've Done So Far:
- [x] Renamed agent from CAP to CARA (Cost-Aware Research Agent)
- [x] Updated main.py, README.md, and dev log with CARA branding
- [x] Created architecture diagram in LucidChart (technical + simplified)
      - Full infrastructure diagram: Fargate boundary, Secrets Manager,
        CloudWatch, chat/research paths, HITL planned section
      - Simplified data flow diagram for Substack/general audience
- [x] Created app.py — FastAPI wrapper with /research and /health endpoints
- [x] Created Dockerfile using python:3.11-slim base image
- [x] Populated requirements.txt with production dependencies only
- [x] Installed fastapi and uvicorn
- [x] Built cara container image (Docker 29.4.0, ARM64)
- [x] Tested container locally via Docker Desktop
      - Health endpoint: {"status":"ok","agent":"C.A.R.A."} ✅
      - Chat route: $0.0002, correct answer ✅
      - Research route: $0.0048, Tavily + Sonnet firing correctly ✅
      - CPU spike visible in Docker Desktop Stats tab during research ✅
- [x] Created AWS Budget alert for CARA (CARA-Project2-Budget, $10 limit)
- [x] Tagged all hosting account (102587257710) resources
      - Cloud Resume Challenge resources tagged as Project0
      - S3 buckets, CloudFront, Lambda, DynamoDB, IAM policies, CFT stacks
      - Component tags added via console to bypass CFT system tag restriction
- [x] Set up HostingTagAuditFunction in hosting account
      - SNS topic, IAM role, Lambda, EventBridge Scheduler
      - Improved three-section report format (fully tagged, missing, untagged)
      - Weekly schedule confirmed active
- [x] Updated sandbox TagAuditFunction with improved report format
      - Per-project breakdown by KNOWN_PROJECTS
      - Summary counts + three grouped lists per project
- [x] Created ECR repository `cara` in correct sandbox account (848747536965)

#### Still To Do:
- [ ] Debug manual Lambda invoke not sending email (sandbox TagAuditFunction)
- [ ] Set up CloudWatch alarm with auto-stop for idle Fargate
- [ ] Push CARA image to ECR
- [ ] Create ECS cluster and Fargate task definition
- [ ] Configure Secrets Manager for API keys
- [ ] Deploy and test live endpoint
- [ ] Wire cost dashboard to live Fargate API
- [ ] Deploy dashboard to theprojectfolder.com


#### Lessons Learned So Far:
---

### Phase 7: Documentation & Portfolio Prep
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