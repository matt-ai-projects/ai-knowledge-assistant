import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.rag.chain import ask_question

# Test questions based on our sample ACME document
ask_question("What are the three user roles in ACME X200?")
ask_question("How much does the Professional plan cost?")
ask_question("How do I connect Slack to ACME X200?")