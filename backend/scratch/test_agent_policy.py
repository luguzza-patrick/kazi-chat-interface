import sys
import os
import asyncio
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from app.db.session import SessionLocal
from app.db.models import Employee
from app.agent.router import KaziAgent

async def test_agent():
    db = SessionLocal()
    user = db.query(Employee).filter(Employee.id == 1).first() # Alice Johnson
    agent = KaziAgent(db, user)
    
    questions = [
        "What is the probation period at Kazi?",
        "How many hours a week do full-time employees work?",
        "Tell me about the different employment types."
    ]
    
    for q in questions:
        print(f"\nUser: {q}")
        response = await agent.process_message(q)
        print(f"Kazi: {response}")
    
    db.close()

if __name__ == "__main__":
    asyncio.run(test_agent())
