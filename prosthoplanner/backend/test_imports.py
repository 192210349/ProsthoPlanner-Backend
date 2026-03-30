print("Import test starting...")
import sys
import os
print("Importing flask...")
from flask import Flask, request, jsonify
print("Importing flask_cors...")
from flask_cors import CORS
print("Importing DatabaseManager...")
from db_manager import DatabaseManager
print("Importing AIEngine...")
from ai_engine import AIEngine
print("All imports successful!")
