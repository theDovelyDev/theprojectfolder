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
**Date:** [DATE]
**Time Spent:** [HOURS]
**Status:** ⬜ Not Started

---

### Phase 4: Budget Kill Switch
**Date:** [DATE]
**Time Spent:** [HOURS]
**Status:** ⬜ Not Started

---

### Phase 5: Testing
**Date:** [DATE]
**Time Spent:** [HOURS]
**Status:** ⬜ Not Started

---

### Phase 6: Deployment to Fargate
**Date:** [DATE]
**Time Spent:** [HOURS]
**Status:** ⬜ Not Started

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