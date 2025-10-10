import os
import sys
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv

sys.path.append(os.path.dirname(__file__))  # Add current folder (app/) to path

from app.agents.supervisor_agent import SupervisorAgent



load_dotenv()
app = FastAPI(title="Azure AI Multi-Agent Copilot", version="1.0")

supervisor = SupervisorAgent()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def handle_query(request: QueryRequest):
    """Receives a user query and returns the agent response."""
    response = supervisor.handle_query(request.query)
    return {"query": request.query, "response": response}

@app.get("/")
async def root():
    return {"status": "ok", "message": "Azure AI Copilot is running."}
