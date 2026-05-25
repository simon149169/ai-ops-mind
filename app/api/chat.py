from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatMessage
from app.services.llm_service import stream_chat_completion, build_messages
from app.services.session_manager import create_session, add_message, get_messages, get_sessions, delete_session
from app.prompts.chat_system import CHAT_SYSTEM_PROMPT
import json

router = APIRouter()

@router.post("/stream")
async def stream_chat(message: ChatMessage):
    session_id = message.session_id or create_session()
    
    history = get_messages(session_id)
    messages = build_messages(CHAT_SYSTEM_PROMPT, message.message)
    
    async def generate():
        full_content = ""
        async for chunk in stream_chat_completion(messages):
            full_content += chunk
            yield f'data: {json.dumps({"type": "token", "content": chunk})}\n\n'
        
        add_message(session_id, "user", message.message)
        add_message(session_id, "assistant", full_content)
        
        yield f'data: {json.dumps({"type": "done", "session_id": session_id})}\n\n'
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.get("/sessions")
async def list_sessions():
    return get_sessions()

@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str):
    return get_messages(session_id)

@router.delete("/sessions/{session_id}")
async def remove_session(session_id: str):
    delete_session(session_id)
    return {"status": "success", "message": "会话已删除"}
