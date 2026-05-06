from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .session import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)  # employee, hr, ceo

    leave_balances = relationship("LeaveBalance", back_populates="employee", uselist=False)
    payroll = relationship("Payroll", back_populates="employee", uselist=False)

class LeaveBalance(Base):
    __tablename__ = "leave_balances"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True)
    days_remaining = Column(Integer)

    employee = relationship("Employee", back_populates="leave_balances")

class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True)
    salary = Column(Float)

    employee = relationship("Employee", back_populates="payroll")
