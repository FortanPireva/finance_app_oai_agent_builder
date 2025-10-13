#!/bin/bash

# Development server startup script
# Uses uv to run the application

echo "🚀 Starting FinTech Support Chatbot (Development Mode)..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Please create .env from .env.example and configure your API keys"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Installing dependencies with pip instead..."
    python -m pip install -r requirements.txt
    uvicorn main:app --reload --port 8000
else
    echo "✅ Using uv for fast execution"
    echo ""
    
    # Ensure dependencies are installed
    if [ ! -d ".venv" ]; then
        echo "📦 Creating virtual environment..."
        uv venv
    fi
    
    echo "📥 Installing/updating dependencies..."
    uv pip install -r requirements.txt
    
    echo ""
    echo "📡 Server starting at: http://localhost:8000"
    echo "💬 Chat interface: http://localhost:8000"
    echo "📊 API docs: http://localhost:8000/docs"
    echo ""
    
    # Activate venv and run
    source .venv/bin/activate
    uvicorn main:app --reload --port 8000
fi

