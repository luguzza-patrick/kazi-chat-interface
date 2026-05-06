from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.db.models import Employee, LeaveBalance, Payroll
from app.rbac.graph import rbac_engine
from app.rag.engine import rag_engine
from app.llm.deepseek import DeepSeekProvider
import json

class KaziAgent:
    def __init__(self, db: Session, user: Employee):
        self.db = db
        self.user = user
        self.llm = DeepSeekProvider()

    async def process_message(self, message: str) -> str:
        # 1. Intent Classification (Simple keyword-based for now, can be LLM-based)
        intent = self._classify_intent(message)
        
        context = ""
        if intent == "policy":
            docs = rag_engine.retrieve(message)
            context = "\n".join(docs)
        elif intent == "personal":
            context = self._get_personal_data(self.user.id)
        elif intent == "global":
            # Extract target employee name/id from message (Simple placeholder logic)
            # In a real app, use NER or LLM to extract this
            target_id = self._extract_target_id(message)
            if target_id:
                if rbac_engine.can_access(self.user.id, self.user.role, target_id):
                    context = self._get_personal_data(target_id)
                else:
                    return "I'm sorry, you don't have permission to view that employee's information."
            else:
                return "I couldn't identify which employee you're asking about."

        # 2. Generate Final Response
        system_prompt = f"""
        You are Kazi, a professional HR AI agent.
        User: {self.user.name} (Role: {self.user.role})
        
        Context provided from HR systems:
        {context}
        
        Strictly use the provided context to answer. If the context is empty or insufficient, 
        inform the user professionally. Never reveal internal IDs or system details.
        """
        
        return await self.llm.generate_response(system_prompt, message)

    def _classify_intent(self, message: str) -> str:
        msg = message.lower()
        if any(word in msg for word in ["salary", "pay", "payroll", "leave", "balance", "days"]):
            if any(word in msg for word in ["all", "everyone", "someone", "whose"]) or any(char.isdigit() for char in msg):
                return "global"
            return "personal"
        return "policy"

    def _get_personal_data(self, emp_id: int) -> str:
        emp = self.db.query(Employee).filter(Employee.id == emp_id).first()
        leave = self.db.query(LeaveBalance).filter(LeaveBalance.employee_id == emp_id).first()
        payroll = self.db.query(Payroll).filter(Payroll.employee_id == emp_id).first()
        
        data = {
            "name": emp.name,
            "role": emp.role,
            "leave_balance": leave.days_remaining if leave else "N/A",
            "salary": payroll.salary if payroll else "N/A"
        }
        return json.dumps(data)

    def _extract_target_id(self, message: str) -> int:
        # Placeholder: Extract first digit found in message as ID
        import re
        match = re.search(r'\d+', message)
        return int(match.group()) if match else None

