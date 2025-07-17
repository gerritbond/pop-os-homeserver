import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

OPEN_WEBUI_URL = os.getenv("OPEN_WEBUI_URL", "http://localhost:3000")
OPEN_WEBUI_API_KEY = os.getenv("OPEN_WEBUI_API_KEY", "")

app = FastAPI(title="MCP for Open WebUI")

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None

@app.post("/chat")
async def chat(request: ChatRequest):
    url = f"{OPEN_WEBUI_URL}/api/chat"
    headers = {"Authorization": f"Bearer {OPEN_WEBUI_API_KEY}"} if OPEN_WEBUI_API_KEY else {}
    payload = {"message": request.message}
    if request.conversation_id:
        payload["conversation_id"] = request.conversation_id
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Error communicating with Open WebUI: {str(e)}")

@app.get("/")
def root():
    return {"message": "MCP is running. Use /chat to interact with Open WebUI."} 