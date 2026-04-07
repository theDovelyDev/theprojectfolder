# Cost Tracker Guide — Budget Research Agent

## Where to Check Usage

### Anthropic API
- Go to: console.anthropic.com → Usage
- Shows: token consumption and cost by day and model
- Update frequency: near real-time
- What to log: input tokens, output tokens, cost per session

### Tavily
- Go to: app.tavily.com → Dashboard
- Shows: search requests used vs free tier limit (1,000/month)
- What to log: searches used, searches remaining

### AWS
- Go to: AWS Console → Billing → Cost Explorer
- Filter by tag: CostCenter = Project2
- Shows: Fargate, ECR, API Gateway costs by day
- What to log: daily Fargate spend, total monthly AWS cost

---

## Excel Tracker

Log after every development session:

| Date | Phase | Service | Model | Queries | Tokens In | Tokens Out | Cost |
|------|-------|---------|-------|---------|-----------|------------|------|
| 2026-04-07 | Phase 3 | Anthropic | Haiku | 6 | ~1,200 | ~300 | $0.001 |
| 2026-04-07 | Phase 4 | Anthropic | Haiku + Sonnet | 4 | ~8,000 | ~2,000 | $0.011 |
| 2026-04-07 | Phase 4 | Tavily | — | 2 | — | — | $0.000 |

**Running Total: ~$0.012**

---

## Budget Thresholds

| Threshold | Action |
|-----------|--------|
| $0.05 | Agent kill switch triggers (configurable) |
| $10.00 | Anthropic account spend limit (dev) |
| $20.00 | Current Anthropic credit balance |

---

## Tips

- Check Anthropic usage **after every coding session** — costs accumulate fast
  during testing
- Tavily free tier resets monthly — no action needed unless you exceed 1,000
  searches
- AWS costs won't appear until Phase 6 (Fargate deployment)
- The agent's `total_cost` field tracks per-session cost in real time —
  check terminal output after every test run