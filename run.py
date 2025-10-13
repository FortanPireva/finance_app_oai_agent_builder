"""
Convenience script to run the application
Usage: uv run python run.py
"""
import uvicorn
from config import PORT

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
        log_level="info"
    )

