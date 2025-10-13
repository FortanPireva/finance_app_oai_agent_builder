# OpenAI Agent Builder Setup Guide

This guide walks you through setting up your OpenAI Agent for the FinTech Support Chatbot.

## Step 1: Access OpenAI Agent Builder

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Log in with your OpenAI account
3. Navigate to **Agent Builder** (or **Assistants** section)
4. Click **Create New Agent**

## Step 2: Configure Basic Agent Settings

### Agent Name
```
FinTechCo Support Assistant
```

### Model Selection
```
GPT-4 (recommended) or GPT-4-turbo
```

### Agent Instructions

Copy and paste these instructions:

```
You are an AI customer support assistant for FinTechCo, a financial technology investment platform.

ROLE:
You help customers with account questions, investment platform features, policies, procedures, and general support inquiries.

CAPABILITIES:
You have access to several tools to help customers:

1. search_knowledge_base - Search internal company knowledge base for policies, procedures, and FAQs
2. search_web - Search the internet for real-time market data or external information
3. calculate_compound_interest - Calculate investment growth with compound interest
4. analyze_investment_returns - Analyze investment performance and calculate metrics like CAGR

WORKFLOW:
1. For account/policy questions → ALWAYS use search_knowledge_base FIRST
2. For market data/external info → Use search_web
3. For calculations → Use the appropriate calculation tool
4. Combine information from multiple tools when needed

RESPONSE GUIDELINES:
✅ DO:
- Be professional, friendly, and helpful
- Search the knowledge base before using external sources
- Provide accurate information based on retrieved data
- Explain calculations step-by-step
- Cite sources when providing policy information
- Ask clarifying questions if the query is ambiguous

❌ DON'T:
- Give specific investment advice or stock recommendations
- Make guarantees about future investment performance
- Share information about other customers' accounts
- Execute transactions or make account changes
- Provide tax or legal advice

IMPORTANT LIMITATIONS:
- You cannot access individual customer account data
- You cannot make account changes or execute transactions
- For urgent security issues, direct users to call the 24/7 security line
- If you cannot answer after checking all tools, apologize and suggest contacting human support

TONE:
Maintain a professional yet approachable tone. Be empathetic to customer concerns while providing clear, actionable information.
```

## Step 3: Register Agent Tools

Add each of these four tools to your agent:

### Tool 1: search_knowledge_base

**Function Name:**
```
search_knowledge_base
```

**Description:**
```
Search the internal company knowledge base for policies, procedures, FAQs, and support information. Use this FIRST for any questions about accounts, products, services, or company policies.
```

**Parameters (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "The user's question or search query to look up in the knowledge base"
    }
  },
  "required": ["query"]
}
```

---

### Tool 2: search_web

**Function Name:**
```
search_web
```

**Description:**
```
Search the web for external information such as current market data, stock prices, cryptocurrency prices, financial news, or general information not available in the internal knowledge base. Use this for real-time or external data.
```

**Parameters (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "The search query to look up on the internet"
    }
  },
  "required": ["query"]
}
```

---

### Tool 3: calculate_compound_interest

**Function Name:**
```
calculate_compound_interest
```

**Description:**
```
Calculate compound interest for investments. Use this when users ask about investment growth, savings calculations, or want to project future values of investments. Formula: A = P(1 + r/n)^(nt)
```

**Parameters (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "principal": {
      "type": "number",
      "description": "The initial investment amount in dollars (e.g., 5000 for $5,000)"
    },
    "rate": {
      "type": "number",
      "description": "The annual interest rate as a percentage (e.g., 5 for 5% APY)"
    },
    "time": {
      "type": "number",
      "description": "The time period in years (can be decimal, e.g., 2.5 for 2.5 years)"
    },
    "compounds_per_year": {
      "type": "integer",
      "description": "Number of times interest is compounded per year (default: 12 for monthly). Common values: 1 (annual), 4 (quarterly), 12 (monthly), 365 (daily)"
    }
  },
  "required": ["principal", "rate", "time"]
}
```

---

### Tool 4: analyze_investment_returns

**Function Name:**
```
analyze_investment_returns
```

**Description:**
```
Analyze investment returns and calculate performance metrics including total return, CAGR (Compound Annual Growth Rate), and average annual return. Use this when users want to understand their investment performance over time.
```

**Parameters (JSON Schema):**
```json
{
  "type": "object",
  "properties": {
    "initial": {
      "type": "number",
      "description": "The initial investment amount in dollars"
    },
    "final": {
      "type": "number",
      "description": "The final investment value in dollars"
    },
    "years": {
      "type": "number",
      "description": "The number of years the investment was held (can be decimal)"
    }
  },
  "required": ["initial", "final", "years"]
}
```

## Step 4: Configure Additional Settings

### File Upload (Optional)
- Enable if you want users to upload documents
- The agent can then analyze uploaded files

### Code Interpreter (Optional)
- Enable if you want the agent to write and execute code
- Note: Our backend already provides calculation tools

### Knowledge Files (Optional)
- You can upload additional documents here
- These will be searchable by the agent
- Note: Our FAISS backend provides more efficient knowledge search

### Retrieval (Optional)
- Can enable for uploaded knowledge files
- Our implementation uses FAISS for better performance

## Step 5: Test Your Agent

1. Use the **Playground** or **Test** interface in Agent Builder
2. Try these test queries:
   ```
   - "How do I withdraw funds from my account?"
   - "What are your interest rates?"
   - "Calculate compound interest on $5,000 at 5% for 2 years"
   - "What's the current price of Bitcoin?"
   - "Analyze an investment that went from $10,000 to $15,000 in 3 years"
   ```
3. Verify the agent:
   - Calls the correct tools
   - Provides accurate responses
   - Has good conversational flow

## Step 6: Publish Your Agent

1. Click **Publish** or **Deploy**
2. Copy the **Agent ID** (starts with `wf_`)
   - Example: `wf_abc123def456`
3. Save this ID - you'll need it for deployment

## Step 7: Configure Domain Allowlist (Important!)

For ChatKit to work in production:

1. In OpenAI Platform, go to **Settings** → **Domains**
2. Add your domains:
   - Development: `http://localhost:8000`
   - Production: `your-app.vercel.app`
3. Save changes

**Without this step, ChatKit will refuse to connect!**

## Step 8: Update Your Application

Add the Agent ID to your `.env` file:

```env
OPENAI_AGENT_ID=wf_your_actual_agent_id_here
```

## Troubleshooting

### Agent not calling tools correctly

**Problem:** Agent responds without using tools

**Solution:**
- Make tool descriptions very clear about when to use them
- Add "ALWAYS search knowledge base first" in instructions
- Test with explicit queries like "Search the knowledge base for withdrawal info"

### Tool execution errors

**Problem:** "Tool execution failed" errors

**Solution:**
- Verify tool names match exactly (case-sensitive)
- Check parameter types match the schema
- Test tools directly via `/api/tools/test` endpoint

### Agent gives generic responses

**Problem:** Agent doesn't use retrieved information

**Solution:**
- Improve agent instructions to emphasize using tool results
- Add "Base your response on the information retrieved" in instructions
- Provide examples in the instructions

### Rate limit errors

**Problem:** "Rate limit exceeded" errors

**Solution:**
- Upgrade OpenAI plan for higher limits
- Implement caching in your backend
- Add rate limiting to your frontend

## Advanced Configuration

### Custom Greeting

Add a greeting message in Agent settings:
```
Hello! I'm your FinTechCo AI assistant. I can help you with:
• Account questions and procedures
• Investment platform features  
• Financial calculations
• Market information

How can I assist you today?
```

### Suggested Prompts

Add these as quick-start suggestions:
- "How do I withdraw funds?"
- "What are your account types?"
- "Calculate investment returns"
- "What are your trading fees?"

### Conversation Starters

Configure conversation starters in ChatKit:
```javascript
conversationStarters: [
  "How do I fund my account?",
  "Calculate compound interest",
  "What are your interest rates?",
  "Explain your fee structure"
]
```

## Best Practices

1. **Test Thoroughly**: Test all tool combinations before production
2. **Monitor Usage**: Check OpenAI dashboard for usage patterns
3. **Iterate Instructions**: Refine based on real user interactions
4. **Keep Knowledge Current**: Update knowledge base regularly
5. **Set Expectations**: Be clear about what the agent can/cannot do
6. **Graceful Degradation**: Handle tool failures gracefully
7. **Security**: Never expose sensitive customer data
8. **Compliance**: Ensure responses meet regulatory requirements

## Monitoring Your Agent

### OpenAI Dashboard
- View conversation logs
- Monitor API usage
- Track tool call frequency
- Analyze response quality

### Application Metrics
- Session count
- Average conversation length
- Tool usage statistics
- Error rates
- Response times

## Updating Your Agent

To update your agent:

1. Make changes in Agent Builder
2. Test changes thoroughly
3. Publish updated version
4. Agent ID remains the same
5. Changes are live immediately

Note: No need to redeploy your application when updating agent instructions or tools.

## Cost Optimization

### Reduce Costs:
1. Cache knowledge base searches
2. Use GPT-4-turbo (cheaper than GPT-4)
3. Optimize tool descriptions (fewer tokens)
4. Implement rate limiting
5. Use shorter system instructions where possible

### Monitor Costs:
- Check OpenAI usage dashboard daily
- Set up billing alerts
- Track cost per conversation
- Monitor tool call frequency

## Support

If you encounter issues:

1. Check OpenAI Agent Builder documentation
2. Review application logs
3. Test tools independently
4. Contact OpenAI support for agent-specific issues
5. Check this repo's GitHub issues

## Next Steps

After setup:
1. ✅ Test agent thoroughly
2. ✅ Configure domain allowlist
3. ✅ Add Agent ID to .env
4. ✅ Deploy to Vercel
5. ✅ Monitor initial usage
6. ✅ Gather feedback
7. ✅ Iterate and improve

---

**Need Help?** Refer to:
- [OpenAI Agent Builder Docs](https://platform.openai.com/docs/agents)
- [ChatKit Documentation](https://platform.openai.com/docs/chatkit)
- [Project README](README.md)
- [Deployment Guide](DEPLOYMENT.md)

