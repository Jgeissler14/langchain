
from fastapi import FastAPI
from langchain_community.tools import DuckDuckGoSearchRun
from pydantic import BaseModel

app = FastAPI()

class ResearchRequest(BaseModel):
    topic: str

@app.post("/research")
def research(request: ResearchRequest):
    """
    Takes a topic and returns research information from DuckDuckGo.
    """
    search = DuckDuckGoSearchRun()
    research_results = search.run(request.topic)
    return {"results": research_results}

@app.get("/")
def health_check():
    return {"status": "ok"}
