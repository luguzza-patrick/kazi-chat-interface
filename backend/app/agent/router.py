import json
from sqlalchemy.orm import Session
from app.db.models import Employee, LeaveBalance, Payroll
from app.llm.deepseek import DeepSeekProvider
from app.rag.engine import rag_engine
from app.rbac.graph import rbac_engine

class KaziAgent:
    def __init__(self, db: Session, user: Employee):
        self.db = db
        self.user = user
        self.llm = DeepSeekProvider()

    async def process_message(self, message: str) -> str:
        # 1. Pre-check for names and pronouns to help the small LLM
        potential_names = ["Alice", "Bob", "Charlie", "David", "Eve"]
        found_name = next((n for n in potential_names if n.lower() in message.lower()), None)
        found_pronoun = any(p in message.lower().split() for p in ["my", "me", "i", "mine"])
        
        analysis_prompt = f"""
        Identify the INTENT and TARGET.
        
        MESSAGE: "{message}"
        DETECTION_HINT: {"Name: " + found_name if found_name else ("Pronoun found" if found_pronoun else "None")}

        INTENT OPTIONS:
        - "LOOKUP_MYSELF": ONLY for personal data (salary, leave, my profile).
        - "LOOKUP_OTHER": ONLY for another person's name.
        - "POLICY_QUESTION": For everything else (rules, behavior, how-to, grooming, resources).

        EXAMPLES:
        "my salary" -> {{"intent": "LOOKUP_MYSELF", "target_name": null, "topic": "salary"}}
        "Bob's salary" -> {{"intent": "LOOKUP_OTHER", "target_name": "Bob", "topic": "salary"}}
        "how to resign?" -> {{"intent": "POLICY_QUESTION", "target_name": null, "topic": "resignation"}}
        "grooming rules" -> {{"intent": "POLICY_QUESTION", "target_name": null, "topic": "grooming"}}
        """
        
        print(f"--- AGENT ANALYSIS ---\nMessage: {message}\nUser: {self.user.name} ({self.user.role})")
        
        analysis_res = await self.llm.generate_response("You are a strict HR intent analyzer. Return JSON only.", analysis_prompt)
        analysis_res = analysis_res.strip().replace("```json", "").replace("```", "").strip()
        
        try:
            raw_analysis = json.loads(analysis_res)
            # Normalize keys to lowercase to handle model inconsistencies
            analysis = {k.lower(): v for k, v in raw_analysis.items()}
            print(f"Normalized Analysis: {analysis}")
        except:
            print(f"JSON Parse Failed: {analysis_res}")
            analysis = {"intent": "POLICY_QUESTION", "target_name": None, "topic": message}

        # Force intent and target based on pre-checks and normalized keys
        intent = analysis.get("intent") or analysis.get("intent_type") or "POLICY_QUESTION"
        target_name = analysis.get("target_name") or analysis.get("target") or found_name
        
        # Map specific model-generated intents back to our internal names
        if "myself" in str(intent).lower() or "personal" in str(intent).lower():
            intent = "LOOKUP_MYSELF"
        elif "other" in str(intent).lower() or "global" in str(intent).lower():
            intent = "LOOKUP_OTHER"
        elif "policy" in str(intent).lower():
            intent = "POLICY_QUESTION"
        
        if found_name:
            intent = "LOOKUP_OTHER"
            target_name = found_name
        elif found_pronoun and intent != "POLICY_QUESTION":
            intent = "LOOKUP_MYSELF"
            target_name = None

        topic = analysis.get("topic", message)

        # 2. Context Gathering with RBAC Enforcement
        context = ""
        denied_msg = None

        if intent == "POLICY_QUESTION":
            docs = await rag_engine.retrieve(topic or message, k=4)
            context = "\n".join([f"Document Chunk: {d}" for d in docs])
        
        elif intent == "LOOKUP_MYSELF":
            context = self._get_personal_data(self.user.id)
            
        elif intent == "LOOKUP_OTHER":
            target_id = self._find_employee_id(target_name) if target_name else None
            if target_id:
                has_access = rbac_engine.can_access(self.user.id, self.user.role, target_id)
                print(f"Global Access Check: Requester={self.user.name}, Target={target_name}, Access={has_access}")
                if has_access:
                    context = self._get_personal_data(target_id)
                else:
                    denied_msg = f"ACCESS DENIED: You (an {self.user.role}) do not have permission to view private data for {target_name}."
            else:
                context = f"ERROR: Employee '{target_name}' not found."

        print(f"Generated Context: {context if not denied_msg else 'DENIED'}")
        
        # 3. Final Response Generation
        if denied_msg:
            return denied_msg

        system_prompt = f"""
        You are Kazi, a friendly and professional HR AI Assistant. 
        Your goal is to help {self.user.name} by providing clear, conversational, and accurate information based on the HR records provided below.
        
        SYSTEM CONTEXT:
        {context if context else "No specific records found for this topic."}
        
        GUIDELINES:
        1. Be Conversational: Speak like a helpful colleague. Use phrases like "I've checked our records for you," or "Based on our company policy..."
        2. Stay Accurate: Only provide information that is explicitly mentioned in the SYSTEM CONTEXT. 
        3. No Hallucinations: If the information isn't in the context, politely say you don't have those specific details yet.
        4. Structured but Natural: Use bullet points for lists (like dress code items) but introduce them naturally.
        5. RBAC Awareness: If you see "ACCESS DENIED" in the context, explain politely that the information is restricted.
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
