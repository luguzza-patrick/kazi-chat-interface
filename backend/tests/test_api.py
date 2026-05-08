import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal, Base, engine
from app.db.models import Employee, LeaveBalance, Payroll

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Create tables and seed test data before running tests"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if employees already exist
        existing = db.query(Employee).first()
        if existing:
            return  # Database already seeded
        
        # Seed test employees (IDs 1-5)
        employees = [
            Employee(id=1, name="Alice Johnson", email="alice@kazi.com", username="alice", role="Employee"),
            Employee(id=2, name="Bob Smith", email="bob@kazi.com", username="bob", role="Employee"),
            Employee(id=3, name="Charlie Brown", email="charlie@kazi.com", username="charlie", role="Employee"),
            Employee(id=4, name="David HR", email="david@kazi.com", username="david", role="HR"),
            Employee(id=5, name="Eve CEO", email="eve@kazi.com", username="eve", role="CEO"),
        ]
        
        for emp in employees:
            db.add(emp)
        
        # Add leave balances
        leave_balances = [
            LeaveBalance(employee_id=1, days_remaining=15),
            LeaveBalance(employee_id=2, days_remaining=20),
            LeaveBalance(employee_id=3, days_remaining=10),
            LeaveBalance(employee_id=4, days_remaining=22),
            LeaveBalance(employee_id=5, days_remaining=30),
        ]
        
        for lb in leave_balances:
            db.add(lb)
        
        # Add payroll
        payroll = [
            Payroll(employee_id=1, salary=55000),
            Payroll(employee_id=2, salary=48000),
            Payroll(employee_id=3, salary=60000),
            Payroll(employee_id=4, salary=65000),
            Payroll(employee_id=5, salary=150000),
        ]
        
        for p in payroll:
            db.add(p)
        
        db.commit()
    finally:
        db.close()
    
    yield


def test_chat_policy():
    response = client.post("/api/v1/chat", json={
        "user_id": 1,
        "message": "What is the leave policy?"
    })
    assert response.status_code == 200
    assert "response" in response.json()
    assert "Mock Response" in response.json()["response"]

def test_chat_personal_data_authorized():
    response = client.post("/api/v1/chat", json={
        "user_id": 1,
        "message": "How many leave days do I have left?"
    })
    assert response.status_code == 200
    assert "15" in response.json()["response"]

def test_chat_global_data_unauthorized():
    response = client.post("/api/v1/chat", json={
        "user_id": 1,
        "message": "What is employee 2's salary?"
    })
    assert response.status_code == 200
    assert "don't have permission" in response.json()["response"]

def test_chat_global_data_authorized_hr():
    response = client.post("/api/v1/chat", json={
        "user_id": 4, # HR
        "message": "What is employee 1's salary?"
    })
    assert response.status_code == 200
    assert "50000" in response.json()["response"]
