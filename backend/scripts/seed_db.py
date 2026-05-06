import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal, engine, Base
from app.db.models import Employee, LeaveBalance, Payroll

def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 3 Employees
    employees = [
        Employee(id=1, name="Alice Johnson", role="employee"),
        Employee(id=2, name="Bob Smith", role="employee"),
        Employee(id=3, name="Charlie Brown", role="employee"),
        Employee(id=4, name="David HR", role="hr"),
        Employee(id=5, name="Eve CEO", role="ceo"),
    ]
    db.add_all(employees)
    db.commit()

    # Leave Balances
    leaves = [
        LeaveBalance(employee_id=1, days_remaining=15),
        LeaveBalance(employee_id=2, days_remaining=10),
        LeaveBalance(employee_id=3, days_remaining=20),
        LeaveBalance(employee_id=4, days_remaining=25),
        LeaveBalance(employee_id=5, days_remaining=30),
    ]
    db.add_all(leaves)
    db.commit()

    # Payroll
    payrolls = [
        Payroll(employee_id=1, salary=50000.0),
        Payroll(employee_id=2, salary=55000.0),
        Payroll(employee_id=3, salary=60000.0),
        Payroll(employee_id=4, salary=75000.0),
        Payroll(employee_id=5, salary=200000.0),
    ]
    db.add_all(payrolls)
    db.commit()

    print("Database seeded successfully!")
    db.close()

if __name__ == "__main__":
    seed()
