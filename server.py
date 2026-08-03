import os
from typing import List, Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
import json

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

model = ChatOpenAI(model="gpt-3.5-turbo")

app = FastAPI(title="Ironhack First App")

def build_messages(text: str):
    return [
        SystemMessage(content="Translate the following from English into Italian"),
        HumanMessage(content=text),
    ]

# ---- Request/response shapes matching LangServe's conventions ----

class InvokeRequest(BaseModel):
    input: str
    config: Optional[dict] = None

class InvokeResponse(BaseModel):
    output: str
    metadata: Optional[dict] = None

class BatchRequest(BaseModel):
    inputs: List[str]
    config: Optional[dict] = None

class BatchResponse(BaseModel):
    output: List[str]

class StreamRequest(BaseModel):
    input: str
    config: Optional[dict] = None


@app.post("/invoke", response_model=InvokeResponse)
def invoke(req: InvokeRequest):
    result = model.invoke(build_messages(req.input))
    return InvokeResponse(
        output=result.content,
        metadata={"run_id": result.id} if hasattr(result, "id") else None,
    )


@app.post("/batch", response_model=BatchResponse)
def batch(req: BatchRequest):
    results = [model.invoke(build_messages(t)).content for t in req.inputs]
    return BatchResponse(output=results)


@app.post("/stream")
def stream(req: StreamRequest):
    def event_generator():
        for chunk in model.stream(build_messages(req.input)):
            if chunk.content:
                yield f"data: {json.dumps({'content': chunk.content})}\n\n"
        yield "event: end\ndata: {}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ---- Simple browser UI to test without curl ----

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Translate App</title></head>
    <body style="font-family: sans-serif; max-width: 600px; margin: 40px auto;">
        <h2>English → Italian Translator</h2>
        <textarea id="text" rows="3" style="width: 100%;" placeholder="Type text to translate...">My tailor is rich</textarea>
        <br><br>
        <button onclick="callInvoke()">Invoke</button>
        <button onclick="callStream()">Stream</button>
        <pre id="output" style="background:#f4f4f4; padding:10px; margin-top:20px; white-space: pre-wrap;"></pre>

        <script>
            async function callInvoke() {
                const text = document.getElementById('text').value;
                document.getElementById('output').textContent = "Loading...";
                const res = await fetch('/invoke', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({input: text})
                });
                const data = await res.json();
                document.getElementById('output').textContent = JSON.stringify(data, null, 2);
            }

            async function callStream() {
                const text = document.getElementById('text').value;
                const output = document.getElementById('output');
                output.textContent = "";
                const res = await fetch('/stream', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({input: text})
                });
                const reader = res.body.getReader();
                const decoder = new TextDecoder();
                while (true) {
                    const {done, value} = await reader.read();
                    if (done) break;
                    const chunk = decoder.decode(value);
                    const match = chunk.match(/data: (.*)/);
                    if (match) {
                        try {
                            const parsed = JSON.parse(match[1]);
                            if (parsed.content) output.textContent += parsed.content;
                        } catch(e) {}
                    }
                }
            }
        </script>
    </body>
    </html>
    """