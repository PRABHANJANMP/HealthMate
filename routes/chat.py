# routes/chat.py
"""
Chat Consultation Routes
Handles both standard HTML form POST submissions and JSON REST API.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Request, Form, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from services.agent_service import run_health_agent, get_session_history, clear_session

router = APIRouter(tags=["Chat"])

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    language: str = Field(default="English")
    session_id: str = Field(default="default")

class ChatResponse(BaseModel):
    success: bool
    language: str
    reply: str
    is_emergency: bool
    session_id: str

@router.post("/chat", response_model=ChatResponse)
async def chat_api(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Please enter a health question.")

    lang = "Tamil" if request.language in ("Tamil", "ta") else "English"

    try:
        reply_text, is_emergency_flag = run_health_agent(
            message=request.message.strip(),
            language=lang,
            session_id=request.session_id,
        )
        return ChatResponse(
            success=True,
            language=lang,
            reply=reply_text,
            is_emergency=is_emergency_flag,
            session_id=request.session_id,
        )
    except Exception as error:
        err_msg = "மன்னிக்கவும். தற்போது AI சேவையை அணுக முடியவில்லை. அவசர நிலையில் 108 அழையுங்கள்." if lang == "Tamil" else "Sorry, AI service is temporarily unavailable. In an emergency, call 108 immediately."
        raise HTTPException(status_code=503, detail=err_msg)

@router.post("/chat/submit")
async def chat_form_submit(
    request: Request,
    message: str = Form(...),
    language: str = Form(default="English"),
    session_id: Optional[str] = Form(default="default"),
):
    sid = session_id or request.cookies.get("healthmate_session_id", "default")
    lang = "Tamil" if language in ("Tamil", "ta") else "English"

    if message.strip():
        try:
            run_health_agent(
                message=message.strip(),
                language=lang,
                session_id=sid,
            )
        except Exception:
            pass

    response = RedirectResponse(url=f"/?tab=chat&lang={lang}", status_code=303)
    response.set_cookie("healthmate_session_id", sid, max_age=86400 * 30)
    response.set_cookie("healthmate_lang", lang, max_age=86400 * 30)
    return response

@router.get("/history/{session_id}")
def get_history(session_id: str):
    messages = get_session_history(session_id)
    return {"session_id": session_id, "message_count": len(messages), "messages": messages}

@router.delete("/clear/{session_id}")
@router.post("/clear/{session_id}")
def clear_chat(session_id: str):
    clear_session(session_id)
    return {"success": True, "session_id": session_id, "message": "History cleared."}
