from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.graph import build_graph
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="C.A.R.A.", description="Cost-Aware Research Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://theprojectfolder.com",
        "https://www.theprojectfolder.com",
        "http://dev.theprojectfolder.com.s3-website-us-east-1.amazonaws.com", # dev site testing
        "http://localhost:8080",  # local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = build_graph()

class Query(BaseModel):
    query: str

@app.post("/research")
async def research(q: Query):
    result = agent.invoke({
        "query": q.query,
        "messages": [], "search_results": [],
        "total_cost": 0.0, "iteration": 0,
        "route": "", "final_answer": "",
        "budget_exceeded": False, "awaiting_approval": False
    })
    return {
        "answer":      result["final_answer"],
        "cost":        result["total_cost"],
        "route":       result.get("route"),
        "loops":       result.get("iteration", 0),
        "interrupted": result.get("budget_exceeded", False)
    }

@app.get("/health")
def health():
    return {"status": "ok", "agent": "C.A.R.A."}