
import os
from fastapi import FastAPI
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

app = FastAPI()

class WriterRequest(BaseModel):
    topic: str
    research_notes: str

@app.post("/write")
def write(request: WriterRequest):
    """
    Takes a topic and research notes and writes a short summary.
    """
    # You will need to set the OPENAI_API_KEY environment variable
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    
    prompt_template = """
    You are a helpful assistant that writes a short summary based on the provided research notes.
    
    Topic: {topic}
    Research Notes: {research_notes}
    
    Summary:
    """
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["topic", "research_notes"])
    
    chain = prompt | llm
    
    summary = chain.invoke({"topic": request.topic, "research_notes": request.research_notes})
    
    return {"summary": summary.content}

@app.get("/")
def health_check():
    return {"status": "ok"}

