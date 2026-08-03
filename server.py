import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

model = ChatOpenAI(model="gpt-3.5-turbo")

app = FastAPI(title="Ironhack First App")

class TranslateRequest(BaseModel):
    text: str

@app.post("/translate")
def translate(req: TranslateRequest):
    messages = [
        SystemMessage(content="Translate the following from English into Italian"),
        HumanMessage(content=req.text),
    ]
    result = model.invoke(messages)
    return {"translation": result.content}

@app.get("/")
def root():
    return {"status": "running"}