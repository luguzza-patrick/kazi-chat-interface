from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.auth.mock import get_current_user
from app.db.models import Employee
from app.agent.router import KaziAgent
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: int
    message: str

@router.post("/chat")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    # In a real app, user_id would come from a JWT token
    user = get_current_user(request.user_id, db)
    agent = KaziAgent(db, user)
    response = await agent.process_message(request.message)
    return {"response": response}
