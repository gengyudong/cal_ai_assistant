from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from chatbot import process_chat_message
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str 
    content: str
    name: str = None
    
class ChatRequest(BaseModel):
    messages: List[Message]
    
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # logger.info("Received request: %s", request.model_dump_json())
        messages = [message.model_dump() for message in request.messages]
        response = process_chat_message(messages)
        # logger.info("Response: %s", response)
        return response
    
    except Exception as e:
        logger.error("Error in chat function: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Error in chat function: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    