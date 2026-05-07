import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal, engine, Base
from app.db.models import Employee, LeaveBalance, Payroll
from app.db.constants import EMPLOYEES

def seed():
    # Base.metadata.drop_all(bind=engine) # Commented out to avoid accidental data loss if already seeded
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Check if we already have employees
    if db.query(Employee).count() > 0:
        print("Database already seeded. Skipping...")
        db.close()
        return

    for emp_data in EMPLOYEES:
        emp = Employee(
            name=emp_data["name"],
            email=emp_data["email"],
            username=emp_data["username"],
            role=emp_data["role"]
        )
        db.add(emp)
        db.flush() # To get the id

        leave = LeaveBalance(employee_id=emp.id, days_remaining=emp_data["leave"])
        payroll = Payroll(employee_id=emp.id, salary=emp_data["salary"])
        
        db.add(leave)
        db.add(payroll)

    db.commit()
    print("Database seeded successfully with constant data!")
    db.close()

if __name__ == "__main__":
    seed()
