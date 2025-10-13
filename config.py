"""
Configuration settings for the FinTech Support Chatbot
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_AGENT_ID = os.getenv("OPENAI_AGENT_ID", "")
EMBEDDING_MODEL = "text-embedding-ada-002"

# API Configuration
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "")
SEARCH_API_URL = os.getenv("SEARCH_API_URL", "https://api.duckduckgo.com/")

# FAISS Configuration
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
FAISS_INDEX_PATH = KNOWLEDGE_BASE_DIR / "faiss.index"
DOCUMENTS_PATH = KNOWLEDGE_BASE_DIR / "documents.json"

# App Configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
PORT = int(os.getenv("PORT", "8000"))

# Ensure directories exist
KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)
