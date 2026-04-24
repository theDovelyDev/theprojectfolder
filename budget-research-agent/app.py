from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.graph import build_graph
from dotenv import load_dotenv
load_dotenv()
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('CARAQueryLog')

def log_query(result, query):
    table.put_item(Item={
        'query_id':              str(uuid.uuid4()),
        'timestamp':             datetime.utcnow().isoformat(),
        'query':                 query,
        'route':                 result.get('route'),
        'total_cost':            str(result.get('cost', 0)),
        'loops':                 result.get('loops', 0),
        'interrupted':           result.get('interrupted', False),
        'total_input_tokens':    result.get('total_input_tokens', 0),
        'total_output_tokens':   result.get('total_output_tokens', 0),
        'router_input_tokens':   result.get('router_input_tokens', 0),
        'router_output_tokens':   result.get('router_output_tokens', 0),
        'research_input_tokens': result.get('research_input_tokens', 0),
        'research_output_tokens': result.get('research_output_tokens', 0),
    })

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
    
    log_query(result, q.query)
    
    return {
        "answer":      result["final_answer"],
        "cost":        result["total_cost"],
        "route":       result.get("route"),
        "loops":       result.get("iteration", 0),
        "interrupted": result.get("budget_exceeded", False),
        "tokens": {
        "router_input":     result.get("router_input_tokens", 0),
        "router_output":    result.get("router_output_tokens", 0),
        "research_input":   result.get("research_input_tokens", 0),
        "research_output":  result.get("research_output_tokens", 0),
        "total_input":      result.get("total_input_tokens", 0),
        "total_output":     result.get("total_output_tokens", 0)
        }
    }


@app.get("/health")
def health():
    return {"status": "ok", "agent": "C.A.R.A."}