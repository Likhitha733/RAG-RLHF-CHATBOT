import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
    
    # RAG Settings
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    TOP_K_RESULTS = 5
    
    # Paths
    PDF_PATH = "./Ebook-Agentic-AI.pdf"
    CHROMA_PATH = "./chroma_db"
    FEEDBACK_FILE = "./data/feedback_history.json"