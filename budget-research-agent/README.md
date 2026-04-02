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

## Status

🚧 In progress