# 🚀 Getting Started - FinTech Support Chatbot

Welcome! This guide will get you up and running in **5 minutes**.

## ✅ What's Been Built

A complete, production-ready AI chatbot with:

- ✨ **FastAPI Backend** - RESTful API with ChatKit integration
- 🤖 **OpenAI Agent** - Intelligent agent with tool usage
- 📚 **FAISS Vector DB** - Semantic search over knowledge base
- 💬 **ChatKit UI** - Beautiful chat interface (plug-and-play)
- 🧮 **Smart Tools** - Calculations, web search, knowledge retrieval
- ⚡ **uv Integration** - Ultra-fast package management
- 🚀 **Vercel Ready** - One-click deployment configuration

## 🎯 Quick Start (5 Minutes)

### Step 1: Install uv (30 seconds)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Setup Project (1 minute)

```bash
# Make setup script executable and run it
chmod +x setup.sh
./setup.sh
```

This will:
- Create virtual environment using uv
- Install all dependencies (super fast!)
- Create necessary directories
- Generate `.env` from template

### Step 3: Get OpenAI Credentials (2 minutes)

You need two things:

1. **OpenAI API Key** - Get from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. **OpenAI Agent ID** - Create agent (see below)

### Step 4: Configure Environment (30 seconds)

Edit `.env` file:

```bash
nano .env  # or use your favorite editor
```

Add your credentials:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_AGENT_ID=wf-your-agent-id-here
```

### Step 5: Run the Application (30 seconds)

```bash
./dev.sh
```

Or manually:

```bash
uv run uvicorn main:app --reload
```

### Step 6: Test It! (1 minute)

1. Open browser: **http://localhost:8000**
2. Click the chat button (💬) in bottom-right
3. Ask: **"How do I withdraw funds from my account?"**
4. Watch the magic happen! ✨

## 🎨 Creating Your OpenAI Agent

Don't have an Agent ID yet? No problem!

### Quick Setup (5 minutes)

1. Go to [platform.openai.com](https://platform.openai.com)
2. Navigate to **Agent Builder**
3. Click **Create New Agent**
4. Copy these instructions:

```
You are an AI customer support assistant for FinTechCo. You have access to:
- search_knowledge_base (for policies and procedures)
- search_web (for market data)
- calculate_compound_interest (for calculations)
- analyze_investment_returns (for analysis)

Always search the knowledge base first, then use other tools as needed.
```

5. Add the 4 tools (detailed instructions in [AGENT_SETUP.md](AGENT_SETUP.md))
6. Click **Publish**
7. Copy the Agent ID (starts with `wf_`)
8. Add it to your `.env` file

**Full detailed guide**: [AGENT_SETUP.md](AGENT_SETUP.md)

## 📁 Project Structure

```
finance_app/
├── 🎯 Core Application
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   └── run.py               # Run script
│
├── 🛠️ Agent Tools
│   └── tools/
│       ├── knowledge_base.py    # FAISS search
│       ├── web_search.py        # External search
│       └── code_interpreter.py  # Calculations
│
├── 🎨 Frontend
│   └── static/
│       └── index.html       # Landing page + ChatKit
│
├── 📚 Documentation
│   ├── README.md            # Full documentation
│   ├── QUICKSTART.md        # Quick start
│   ├── AGENT_SETUP.md       # Agent configuration
│   ├── DEPLOYMENT.md        # Deployment guide
│   ├── PROJECT_OVERVIEW.md  # Architecture overview
│   └── UV_GUIDE.md          # uv usage guide
│
└── 🚀 Deployment
    ├── vercel.json          # Vercel config
    ├── setup.sh             # Setup script
    └── dev.sh               # Dev server
```

## 🧪 Test Your Setup

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "environment": "development",
  "agent_configured": true
}
```

### 2. Test Knowledge Base

```bash
curl -X POST http://localhost:8000/api/tools/test \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "search_knowledge_base", "parameters": {"query": "withdrawal"}}'
```

### 3. Test Calculator

```bash
curl -X POST http://localhost:8000/api/tools/test \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "calculate_compound_interest", "parameters": {"principal": 5000, "rate": 5, "time": 2}}'
```

### 4. Test in Browser

Visit http://localhost:8000 and try these queries:

- ✅ "What are your account types?"
- ✅ "Calculate $5,000 at 5% for 2 years"
- ✅ "How do I withdraw funds?"
- ✅ "What's the current Bitcoin price?"

## 🚀 Deploy to Vercel (5 Minutes)

### Prerequisites

```bash
npm install -g vercel
```

### Deploy Steps

```bash
# 1. Login to Vercel
vercel login

# 2. Deploy
vercel

# 3. Set environment variables
vercel env add OPENAI_API_KEY
vercel env add OPENAI_AGENT_ID

# 4. Deploy to production
vercel --prod
```

### Important: Configure Domain Allowlist

After deploying:

1. Go to OpenAI Platform → Settings → Domains
2. Add your Vercel URL: `your-app.vercel.app`
3. Save

**Without this, ChatKit won't work in production!**

**Full deployment guide**: [DEPLOYMENT.md](DEPLOYMENT.md)

## 📖 Documentation Guide

Read in this order:

1. **GETTING_STARTED.md** ← You are here!
2. **AGENT_SETUP.md** - Configure your OpenAI Agent
3. **README.md** - Complete feature documentation
4. **DEPLOYMENT.md** - Production deployment
5. **UV_GUIDE.md** - Learn uv commands
6. **PROJECT_OVERVIEW.md** - Architecture deep dive

## ⚡ uv Quick Reference

```bash
# Install packages (10-100x faster than pip!)
uv pip install package-name

# Run application
uv run uvicorn main:app --reload

# Update dependencies
uv pip install --upgrade -r requirements.txt

# List packages
uv pip list
```

**Full uv guide**: [UV_GUIDE.md](UV_GUIDE.md)

## 🎯 What Can Your Chatbot Do?

### 1. Answer Policy Questions
- Account procedures
- Withdrawal process
- Interest rates
- Fee structures

### 2. Perform Calculations
- Compound interest
- Investment returns
- CAGR analysis
- ROI calculations

### 3. Fetch External Data
- Market prices
- News information
- General knowledge
- Real-time data

### 4. Analyze Data
- Investment performance
- Return metrics
- Growth projections
- Financial analysis

## 🔧 Customization

### Add Your Own Documents

Edit `tools/knowledge_base.py`:

```python
sample_docs = [
    {
        "title": "Your Custom Document",
        "content": "Your content here..."
    },
    # Add more documents
]
```

Restart the app to rebuild the FAISS index.

### Customize the UI

Edit `static/index.html`:

- Change colors in the `<style>` section
- Modify hero text
- Update feature cards
- Add your logo

### Add More Tools

1. Create function in `tools/` directory
2. Register in `main.py` AGENT_TOOLS
3. Add to agent in OpenAI Agent Builder
4. Restart application

## 🐛 Troubleshooting

### "uv: command not found"

```bash
# Reinstall uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Reload shell
source ~/.bashrc  # or ~/.zshrc
```

### "ChatKit not loading"

1. Check `.env` has both API key and Agent ID
2. Verify domain is allowlisted in OpenAI
3. Check browser console for errors
4. Confirm agent is published

### "Module not found"

```bash
# Reinstall dependencies
uv pip install -r requirements.txt
```

### "Port already in use"

```bash
# Use different port
uv run uvicorn main:app --reload --port 8080
```

## 💡 Tips for Success

1. **Test Locally First** - Always test thoroughly before deploying
2. **Use uv** - It's much faster than pip!
3. **Monitor Costs** - Keep an eye on OpenAI API usage
4. **Update Knowledge Base** - Keep documents current
5. **Iterate on Agent** - Refine instructions based on usage
6. **Add Monitoring** - Track usage and errors
7. **Secure Your Keys** - Never commit `.env` to git

## 📊 What's Using uv?

This project extensively uses uv for:

- ✅ Virtual environment creation (`uv venv`)
- ✅ Package installation (`uv pip install`)
- ✅ Running the application (`uv run`)
- ✅ Dependency management
- ✅ Setup automation (`setup.sh`)
- ✅ Development workflow (`dev.sh`)

**Result**: Setup and package operations are **10-100x faster**! ⚡

## 🎓 Learning Resources

### Beginner Track
1. Run through this guide
2. Test the chat interface
3. Read README.md
4. Customize the UI

### Intermediate Track
1. Configure your own agent (AGENT_SETUP.md)
2. Add custom documents
3. Test all tools
4. Deploy to Vercel

### Advanced Track
1. Study architecture (PROJECT_OVERVIEW.md)
2. Add custom tools
3. Implement monitoring
4. Scale for production

## 🤝 Getting Help

### Documentation
- Start with README.md for complete docs
- Check DEPLOYMENT.md for deployment issues
- Review AGENT_SETUP.md for agent problems
- See UV_GUIDE.md for uv questions

### Community
- GitHub Issues
- OpenAI Community Forum
- FastAPI Discord
- Stack Overflow

## ✨ What's Next?

After getting it running:

1. ✅ **Test thoroughly** - Try various queries
2. ✅ **Customize content** - Add your documents
3. ✅ **Configure agent** - Refine instructions
4. ✅ **Deploy** - Get it live on Vercel
5. ✅ **Monitor** - Track usage and costs
6. ✅ **Iterate** - Improve based on feedback

## 🎉 You're Ready!

You now have a production-ready AI chatbot that can:

- 🤖 Answer customer questions intelligently
- 📚 Search your knowledge base semantically
- 🌐 Fetch real-time external data
- 🧮 Perform complex calculations
- 💬 Provide a beautiful chat interface
- ⚡ Run blazingly fast with uv
- 🚀 Deploy to Vercel in minutes

**Need help?** Check the other documentation files or open an issue!

---

**Built with ❤️ using FastAPI, OpenAI Agent Builder, ChatKit, FAISS, and uv**

**Happy Building! 🚀**

