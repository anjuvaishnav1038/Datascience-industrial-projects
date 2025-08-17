from fastapi import FastAPI
from pydantic import BaseModel
from analyze_email_body import analyze_email
from analyze_agent_email import analyze_agent_email
import asyncio
class email_Request(BaseModel):
    email_text:str
app = FastAPI()
@app.post("/api/customer_query")
async  def analyze_email_function(request: email_Request):
    ans=await analyze_email(request.email_text, model_name='llama3.1:8b')
    return ans
@app.post("/api/agent_reply")
async  def analyze_email_function(request: email_Request):
    ans=await analyze_agent_email(request.email_text, model_name='llama3.1:8b')
    return ans
    # return "email analyzed successfully"

