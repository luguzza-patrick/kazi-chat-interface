from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Employee
from app.agent.router import KaziAgent
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: int
    message: str

class LoginRequest(BaseModel):
    email: str
    username: str

@router.post("/auth/login")
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(Employee).filter(
        Employee.email == request.email,
        Employee.username == request.username
    ).first()
    
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid email or username")
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "username": user.username,
        "role": user.role
    }

@router.post("/chat")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    # In a real app, user_id would come from a JWT token or session
    user = db.query(Employee).filter(Employee.id == request.user_id).first()
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid user ID")
    
    agent = KaziAgent(db, user)
    response = await agent.process_message(request.message)
    return {"response": response}
