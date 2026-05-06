from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Employee

# Mocking user context
def get_current_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Employee).filter(Employee.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user ID")
    return user
