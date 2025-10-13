#!/bin/bash

# FinTech Support Chatbot Setup Script
# This script uses uv for fast Python package management

set -e

echo "🚀 Setting up FinTech Support Chatbot..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✅ uv is installed"
echo ""

# Create virtual environment with uv
echo "📦 Creating virtual environment with uv..."
uv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies using uv
echo "📥 Installing dependencies with uv (this is fast!)..."
uv pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed successfully!"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your OpenAI API key and Agent ID"
    echo ""
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p knowledge_base
mkdir -p static

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your credentials:"
echo "   - OPENAI_API_KEY=sk-your-key"
echo "   - OPENAI_AGENT_ID=wf-your-agent-id"
echo ""
echo "2. Run the application:"
echo "   uv run uvicorn main:app --reload"
echo ""
echo "3. Open http://localhost:8000 in your browser"
echo ""

