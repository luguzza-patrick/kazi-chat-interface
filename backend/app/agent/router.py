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
        # 1. LLM Orchestration: Analyze Intent and Parameters
        analysis_prompt = f"""
        Analyze the user message and identify the intent and target.
        User: {self.user.name} (Role: {self.user.role})
        Message: "{message}"

        Return ONLY a JSON object with:
        - "intent": one of ["policy", "personal", "global"]
        - "target_name": name of the employee being asked about (or null)
        - "topic": the specific HR topic (e.g., "maternity leave", "salary", "remote work")
        
        Intent rules:
        - "personal": User asking about their OWN data (salary, leave, etc.)
        - "global": User asking about SOMEONE ELSE'S data.
        - "policy": General HR policy questions.
        """
        
        analysis_res = await self.llm.generate_response("You are a helpful HR routing assistant. Return JSON only.", analysis_prompt)
        
        # Strip potential markdown code blocks from LLM response
        analysis_res = analysis_res.strip().replace("```json", "").replace("```", "").strip()
        
        try:
            analysis = json.loads(analysis_res)
        except:
            # Fallback to simple logic if LLM fails JSON
            analysis = {"intent": "policy", "target_name": None, "topic": message}

        intent = analysis.get("intent", "policy")
        target_name = analysis.get("target_name")
        topic = analysis.get("topic", message)

        # 2. Tool Execution & Context Gathering
        context = ""
        if intent == "policy":
            # Focused retrieval based on topic
            docs = rag_engine.retrieve(topic or message, k=2)
            context = "\n".join(docs)
        
        elif intent == "personal":
            context = self._get_personal_data(self.user.id)
            
        elif intent == "global":
            target_id = self._find_employee_id(target_name) if target_name else None
            if target_id:
                if rbac_engine.can_access(self.user.id, self.user.role, target_id):
                    context = self._get_personal_data(target_id)
                else:
                    return f"Access Denied: As an {self.user.role}, you do not have permission to view sensitive data for {target_name}."
            else:
                context = f"I couldn't find an employee named '{target_name}' in our records."

        # 3. Final Response Generation
        system_prompt = f"""
        You are Kazi, a professional HR AI agent.
        Current User: {self.user.name} (Role: {self.user.role})
        
        Information retrieved from HR systems:
        {context}
        
        Instructions:
        1. Answer the user's question concisely using ONLY the provided information.
        2. If the information is missing, say you don't have access to that specific data.
        3. Use bullet points for any lists or policy details.
        4. Be professional and friendly.
        5. DO NOT mention internal database structures or JSON formats.
        """
        
        return await self.llm.generate_response(system_prompt, message)

    def _find_employee_id(self, name: str) -> int:
        if not name: return None
        # Case-insensitive partial name match
        emp = self.db.query(Employee).filter(Employee.name.ilike(f"%{name}%")).first()
        return emp.id if emp else None

    def _get_personal_data(self, emp_id: int) -> str:
        emp = self.db.query(Employee).filter(Employee.id == emp_id).first()
        if not emp: return "Employee not found."
        
        leave = self.db.query(LeaveBalance).filter(LeaveBalance.employee_id == emp_id).first()
        payroll = self.db.query(Payroll).filter(Payroll.employee_id == emp_id).first()
        
        salary_str = f"${payroll.salary:,.2f}" if payroll else "N/A"
        leave_str = f"{leave.days_remaining} days" if leave else "N/A"
        
        return f"""
        Employee Profile:
        - Name: {emp.name}
        - Role: {emp.role}
        - Leave Balance: {leave_str}
        - Current Salary: {salary_str}
        """

