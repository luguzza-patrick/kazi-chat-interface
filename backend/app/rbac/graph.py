import networkx as nx
from typing import Dict

class RBACEngine:
    def __init__(self):
        self.G = nx.DiGraph()
        self._build_hierarchy()

    def _build_hierarchy(self):
        # Roles
        self.G.add_node("employee")
        self.G.add_node("hr")
        self.G.add_node("ceo")

        # Inheritance: CEO -> HR -> Employee (meaning CEO can do anything HR can, etc.)
        self.G.add_edge("ceo", "hr")
        self.G.add_edge("hr", "employee")

    def can_access(self, requester_id: int, requester_role: str, target_id: int) -> bool:
        # Rule 1: Anyone can access their own data
        if requester_id == target_id:
            return True

        # Rule 2: HR and CEO can access all employee data
        if requester_role in ["hr", "ceo"]:
            return True

        # Rule 3: CEO can access HR data
        if requester_role == "ceo":
            return True

        return False

rbac_engine = RBACEngine()
