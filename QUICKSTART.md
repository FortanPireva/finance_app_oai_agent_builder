# Quick Start Guide

Get your FinTech Support Chatbot running in under 5 minutes!

## Prerequisites

- Python 3.9+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- uv package manager

## Installation

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Setup

```bash
# Clone the repo
git clone <your-repo-url>
cd finance_app

# Run setup script
chmod +x setup.sh
./setup.sh
```

### 3. Configure Environment

Edit `.env`:
```env
OPENAI_API_KEY=sk-your-api-key
OPENAI_AGENT_ID=wf-your-agent-id
```

Don't have an Agent ID yet? See [AGENT_SETUP.md](AGENT_SETUP.md)

### 4. Run the App

```bash
# Using the dev script
./dev.sh

# Or manually with uv
uv run uvicorn main:app --reload
```

### 5. Open Browser

Visit: **http://localhost:8000**

Click the chat button (💬) and start chatting!

## First Time Setup

If you don't have an OpenAI Agent yet:

1. Follow [AGENT_SETUP.md](AGENT_SETUP.md) to create your agent
2. Copy the Agent ID
3. Add it to `.env`
4. Restart the application

## Testing

Try these queries:

✅ **"How do I withdraw funds?"**  
Tests knowledge base search

✅ **"Calculate compound interest on $5,000 at 5% for 2 years"**  
Tests calculation tools

✅ **"What's the current price of Bitcoin?"**  
Tests web search

✅ **"Analyze $10,000 growing to $15,000 in 3 years"**  
Tests investment analysis

## Common Issues

### "Module not found"
```bash
uv pip install -r requirements.txt
```

### "ChatKit not loading"
- Make sure `OPENAI_API_KEY` is set in `.env`
- Make sure `OPENAI_AGENT_ID` is set in `.env`
- Check browser console for errors

### "No knowledge base found"
The knowledge base auto-initializes on first run. Just wait a moment!

## Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment variables
vercel env add OPENAI_API_KEY
vercel env add OPENAI_AGENT_ID

# Deploy to production
vercel --prod
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for full deployment guide.

## What's Next?

- 📚 Read the full [README.md](README.md)
- 🤖 Configure your agent: [AGENT_SETUP.md](AGENT_SETUP.md)
- 🚀 Deploy to production: [DEPLOYMENT.md](DEPLOYMENT.md)
- 🔧 Customize the knowledge base in `tools/knowledge_base.py`
- 🎨 Customize the UI in `static/index.html`

## Need Help?

- Check the [README.md](README.md) for detailed docs
- Review [AGENT_SETUP.md](AGENT_SETUP.md) for agent configuration
- Open an issue on GitHub

---

**Happy Building! 🚀**

