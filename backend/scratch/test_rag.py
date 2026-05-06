import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from app.rag.engine import rag_engine

query = "What is the probation period?"
results = rag_engine.retrieve(query, k=2)
print(f"Query: {query}")
for i, res in enumerate(results):
    print(f"Result {i+1}:\n{res}\n")

query = "How many hours do full-time employees work?"
results = rag_engine.retrieve(query, k=2)
print(f"Query: {query}")
for i, res in enumerate(results):
    print(f"Result {i+1}:\n{res}\n")
