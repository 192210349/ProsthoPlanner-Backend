print("Instantiation test starting...")
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db_manager import DatabaseManager
from ai_engine import AIEngine

print("Instantiating DatabaseManager...")
db = DatabaseManager()
print("DatabaseManager instantiated successfully!")

print("Instantiating AIEngine...")
ai = AIEngine()
print("AIEngine instantiated successfully!")

print("All instantiations successful!")
