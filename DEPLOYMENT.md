# Deployment Guide - FinTech Support Chatbot

This guide provides step-by-step instructions for deploying your FinTech Support Chatbot to Vercel.

## Prerequisites

Before deploying, ensure you have:

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI** (optional but recommended):
   ```bash
   npm install -g vercel
   ```
3. **OpenAI API Key**: From [platform.openai.com](https://platform.openai.com)
4. **OpenAI Agent ID**: Created in OpenAI Agent Builder

## Local Setup with uv

### 1. Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd finance_app

# Run setup script
chmod +x setup.sh
./setup.sh
```

### 3. Configure Environment Variables

Edit `.env` file:

```env
OPENAI_API_KEY=sk-your-actual-api-key
OPENAI_AGENT_ID=wf-your-agent-workflow-id
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:8000
```

### 4. Run Locally

Using uv:
```bash
uv run uvicorn main:app --reload --port 8000
```

Or activate the virtual environment first:
```bash
source .venv/bin/activate
uvicorn main:app --reload --port 8000
```

Visit: http://localhost:8000

## Setting Up OpenAI Agent Builder

### 1. Create Your Agent

1. Go to [platform.openai.com](https://platform.openai.com)
2. Navigate to Agent Builder
3. Create a new agent with the following configuration:

**Agent Instructions:**
```
You are an AI customer support assistant for FinTechCo, a financial technology company.

Your role is to help customers with:
- Account questions and procedures
- Investment platform features
- Policy and compliance information
- Basic financial calculations
- General support inquiries

You have access to several tools:
1. search_knowledge_base - Search internal company knowledge base (use this FIRST)
2. search_web - Search the internet for real-time data or external information
3. calculate_compound_interest - Calculate investment growth with compound interest
4. analyze_investment_returns - Analyze investment performance metrics

Always:
- Be professional, friendly, and helpful
- Search the knowledge base first before using external sources
- Provide accurate information based on retrieved data
- When performing calculations, explain your work
- If you cannot find an answer, apologize and suggest contacting human support

Never:
- Give specific investment advice or recommendations
- Make guarantees about investment performance
- Share information about other customers
- Execute transactions or make account changes
```

### 2. Register Agent Tools

Add these function tools to your agent:

**search_knowledge_base:**
```json
{
  "name": "search_knowledge_base",
  "description": "Search the internal knowledge base for company policies, procedures, FAQs, and support information.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The user's question or search query"
      }
    },
    "required": ["query"]
  }
}
```

**search_web:**
```json
{
  "name": "search_web",
  "description": "Search the web for external information like market data or news.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The search query"
      }
    },
    "required": ["query"]
  }
}
```

**calculate_compound_interest:**
```json
{
  "name": "calculate_compound_interest",
  "description": "Calculate compound interest for investments.",
  "parameters": {
    "type": "object",
    "properties": {
      "principal": {"type": "number", "description": "Initial investment ($)"},
      "rate": {"type": "number", "description": "Annual interest rate (%)"},
      "time": {"type": "number", "description": "Time period (years)"},
      "compounds_per_year": {"type": "integer", "description": "Compounding frequency"}
    },
    "required": ["principal", "rate", "time"]
  }
}
```

**analyze_investment_returns:**
```json
{
  "name": "analyze_investment_returns",
  "description": "Analyze investment returns and calculate metrics like CAGR.",
  "parameters": {
    "type": "object",
    "properties": {
      "initial": {"type": "number", "description": "Initial investment ($)"},
      "final": {"type": "number", "description": "Final value ($)"},
      "years": {"type": "number", "description": "Years invested"}
    },
    "required": ["initial", "final", "years"]
  }
}
```

### 3. Publish Your Agent

1. Test your agent in the Agent Builder interface
2. Click "Publish" or "Deploy"
3. Copy the Agent ID (starts with `wf_`)
4. Save this ID for deployment

## Deploying to Vercel

### Method 1: Using Vercel CLI (Recommended)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Set Environment Variables:**
   ```bash
   vercel env add OPENAI_API_KEY
   vercel env add OPENAI_AGENT_ID
   ```
   
   Enter your values when prompted.

5. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

### Method 2: Using Vercel Dashboard

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo>
   git push -u origin main
   ```

2. **Import to Vercel:**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repository
   - Vercel will auto-detect the Python framework

3. **Configure Environment Variables:**
   - In Vercel dashboard → Settings → Environment Variables
   - Add:
     - `OPENAI_API_KEY` = your OpenAI API key
     - `OPENAI_AGENT_ID` = your agent workflow ID
     - `ENVIRONMENT` = production

4. **Deploy:**
   - Click "Deploy"
   - Wait for deployment to complete

### Method 3: Vercel Deploy Button

Add this to your README for one-click deployment:

```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=<your-repo-url>&env=OPENAI_API_KEY,OPENAI_AGENT_ID)
```

## Post-Deployment Configuration

### 1. Configure OpenAI Domain Allowlist

Important: ChatKit requires domain allowlisting for security.

1. Go to OpenAI Platform → Settings → Domains
2. Add your Vercel domain: `your-app.vercel.app`
3. Save changes

Without this, ChatKit will refuse to connect!

### 2. Test Your Deployment

1. Visit your Vercel URL
2. Click the chat button (💬)
3. Ask a test question: "What are your account types?"
4. Verify the agent responds correctly

### 3. Monitor Logs

View logs in Vercel dashboard:
- Functions → View Logs
- Check for any errors
- Monitor API usage

## Troubleshooting

### ChatKit Not Loading

**Issue:** "Unable to connect to OpenAI ChatKit"

**Solutions:**
- Verify `OPENAI_API_KEY` is set correctly
- Verify `OPENAI_AGENT_ID` is correct (starts with `wf_`)
- Check domain is allowlisted in OpenAI settings
- Check browser console for errors

### Knowledge Base Not Found

**Issue:** "No relevant information found"

**Solutions:**
- The knowledge base initializes on first run
- Check logs to ensure FAISS index was created
- Verify file system permissions
- May need to pre-build knowledge base in build step

### Import Errors

**Issue:** Module import failures

**Solutions:**
- Ensure `requirements.txt` includes all dependencies
- Check Python version (requires >=3.9)
- Clear Vercel cache and redeploy

### Tool Execution Errors

**Issue:** Agent tools not working

**Solutions:**
- Verify tool names match exactly between agent config and code
- Check tool function signatures
- Review agent logs in OpenAI platform
- Test tools locally first using `/api/tools/test` endpoint

## Performance Optimization

### 1. FAISS Index Caching

For production, consider:
- Pre-building FAISS index
- Storing index in Vercel Blob Storage or S3
- Loading index on cold start

### 2. API Rate Limiting

Implement rate limiting:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/chatkit/session")
@limiter.limit("10/minute")
async def create_session():
    ...
```

### 3. Caching Responses

Add caching for knowledge base queries:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def search_knowledge_base(query: str) -> str:
    ...
```

## Monitoring and Analytics

### 1. Add Analytics

Track usage with Vercel Analytics:
```bash
npm install @vercel/analytics
```

### 2. Error Tracking

Consider adding Sentry or similar:
```bash
uv pip install sentry-sdk
```

### 3. Usage Metrics

Monitor:
- Session count
- Query patterns
- Tool usage frequency
- Response times
- OpenAI API costs

## Scaling Considerations

### For High Traffic:

1. **Upgrade Vercel Plan**: Pro or Enterprise for more resources
2. **Database for Sessions**: Add Redis or PostgreSQL for session persistence
3. **Load Balancing**: Vercel handles this automatically
4. **CDN**: Vercel provides global CDN by default
5. **Background Jobs**: Use Vercel Cron for periodic tasks

## Security Checklist

- [ ] Environment variables are secured (not in code)
- [ ] API keys use project-specific scopes
- [ ] Domain allowlist is configured
- [ ] CORS is properly configured
- [ ] Rate limiting is implemented
- [ ] Input validation on all endpoints
- [ ] HTTPS only (Vercel enforces this)
- [ ] Code interpreter has restricted permissions

## Cost Estimation

**OpenAI Costs:**
- Embeddings: ~$0.0001 per 1K tokens
- GPT-4 Chat: ~$0.03 per 1K tokens
- Agent execution: Variable based on tool usage

**Vercel Costs:**
- Hobby: Free (personal projects)
- Pro: $20/month (commercial use)
- Enterprise: Custom pricing

**Estimated Monthly Cost (1000 users):**
- OpenAI API: $50-200
- Vercel: $20 (Pro plan)
- Total: $70-220/month

## Support

For issues or questions:
- Check logs in Vercel dashboard
- Review OpenAI Agent Builder docs
- Test tools locally first
- Open an issue on GitHub

## Next Steps

After deployment:
1. Monitor initial usage
2. Gather user feedback
3. Expand knowledge base
4. Add more agent capabilities
5. Implement analytics
6. Set up monitoring alerts

