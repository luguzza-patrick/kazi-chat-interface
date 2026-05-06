import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal, Base, engine
from app.db.models import Employee, LeaveBalance, Payroll

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Use existing seeded DB for simplicity in this demo, 
    # but ideally use a separate test DB.
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
