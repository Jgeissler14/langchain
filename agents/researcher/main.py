
from fastapi import FastAPI
from langchain_community.tools import DuckDuckGoSearchRun
from pydantic import BaseModel
import requests
from fastapi import Request

app = FastAPI()

class ResearchRequest(BaseModel):
    topic: str

@app.post("/research")
def research(request_data: ResearchRequest, request: Request):
    """
    Takes a topic, searches DuckDuckGo, and returns a written summary.
    """
    search = DuckDuckGoSearchRun()
    search_results = search.run(request_data.topic)
    # Build the URL dynamically based on the current request
    base_url = str(request.base_url).rstrip("/")
    writer_url = f"{base_url}/writer"
    response = requests.post(writer_url, json={"topic": request_data.topic, "search_results": search_results})
    written_summary = response.json().get("written_summary", "")
    return {"results": written_summary}

@app.get("/")
def health_check():
    return {"status": "ok"}

