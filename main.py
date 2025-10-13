"""
FastAPI application for FinTech Support Chatbot
Integrates OpenAI Agent Builder and ChatKit
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional, Dict, Any
import config
from tools import (
    search_knowledge_base,
    search_web,
    get_market_data,
    calculate_compound_interest,
    analyze_investment_returns
)

# Initialize FastAPI app
app = FastAPI(
    title="FinTech Support Chatbot",
    description="AI-powered customer support with RAG and agent tools",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS if config.ENVIRONMENT == "development" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)


# Pydantic models
class SessionRequest(BaseModel):
    """Request model for creating a chat session"""
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class SessionResponse(BaseModel):
    """Response model for chat session"""
    session_id: str
    client_secret: str
    agent_id: str


class ClientSecretResponse(BaseModel):
    """Response model for client secret"""
    client_secret: str


class RefreshRequest(BaseModel):
    """Request model for refreshing client secret"""
    currentClientSecret: str


class ToolCallRequest(BaseModel):
    """Request model for testing tool calls"""
    tool_name: str
    parameters: Dict[str, Any]


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - serves the landing page"""
    return FileResponse("static/index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": config.ENVIRONMENT,
        "agent_configured": bool(config.OPENAI_AGENT_ID),
    }


# ChatKit session endpoint
@app.post("/api/chatkit/session", response_model=SessionResponse)
async def create_chatkit_session(request: SessionRequest = SessionRequest()):
    """
    Create a new ChatKit session for the agent.
    Returns a client secret that the frontend uses to connect to the agent.
    """
    try:
        if not config.OPENAI_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY in environment."
            )
        
        if not config.OPENAI_AGENT_ID:
            raise HTTPException(
                status_code=500,
                detail="Agent ID not configured. Please set OPENAI_AGENT_ID in environment."
            )
        
        # Note: As of the implementation, OpenAI's ChatKit/Agent Builder API
        # for session creation might differ. This is a conceptual implementation.
        # You would use the actual SDK method like:
        # session = client.beta.agents.sessions.create(agent_id=config.OPENAI_AGENT_ID)
        
        # For now, returning the agent_id and a placeholder structure
        # In production, this would call the actual OpenAI Agent API
        
        # Placeholder response - replace with actual OpenAI API call
        return SessionResponse(
            session_id=f"session_{request.user_id or 'anonymous'}",
            client_secret=config.OPENAI_API_KEY,  # In production, this would be a session token
            agent_id=config.OPENAI_AGENT_ID
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@app.post("/api/chatkit/start", response_model=ClientSecretResponse)
async def start_chatkit_session():
    """
    Start a new ChatKit session and return a client secret.
    This is called when the user first opens the chat.
    """
    try:
        if not config.OPENAI_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY in environment."
            )
        
        if not config.OPENAI_AGENT_ID:
            raise HTTPException(
                status_code=500,
                detail="Agent ID not configured. Please set OPENAI_AGENT_ID in environment."
            )
        
        # Note: In production, this would call the OpenAI Agent API to create a new session
        # and return a proper client secret. For now, returning the API key as a placeholder.
        # The actual implementation would be:
        # session = client.beta.agents.sessions.create(agent_id=config.OPENAI_AGENT_ID)
        # return ClientSecretResponse(client_secret=session.client_secret)
        
        return ClientSecretResponse(client_secret=config.OPENAI_API_KEY)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start session: {str(e)}")


@app.post("/api/chatkit/refresh", response_model=ClientSecretResponse)
async def refresh_chatkit_session(request: RefreshRequest):
    """
    Refresh an existing ChatKit session and return a new client secret.
    This is called when the current client secret expires.
    """
    try:
        if not config.OPENAI_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY in environment."
            )
        
        if not config.OPENAI_AGENT_ID:
            raise HTTPException(
                status_code=500,
                detail="Agent ID not configured. Please set OPENAI_AGENT_ID in environment."
            )
        
        # Note: In production, this would call the OpenAI Agent API to refresh the session
        # using the current client secret and return a new one.
        # The actual implementation would be:
        # session = client.beta.agents.sessions.refresh(
        #     agent_id=config.OPENAI_AGENT_ID,
        #     client_secret=request.currentClientSecret
        # )
        # return ClientSecretResponse(client_secret=session.client_secret)
        
        return ClientSecretResponse(client_secret=config.OPENAI_API_KEY)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh session: {str(e)}")


# Tool testing endpoints (for development/debugging)
@app.post("/api/tools/test")
async def test_tool(request: ToolCallRequest):
    """
    Test endpoint to manually invoke agent tools.
    Useful for development and debugging.
    """
    tool_map = {
        "search_knowledge_base": search_knowledge_base,
        "search_web": search_web,
        "get_market_data": get_market_data,
        "calculate_compound_interest": calculate_compound_interest,
        "analyze_investment_returns": analyze_investment_returns,
    }
    
    if request.tool_name not in tool_map:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown tool: {request.tool_name}. Available tools: {list(tool_map.keys())}"
        )
    
    try:
        tool_func = tool_map[request.tool_name]
        result = tool_func(**request.parameters)
        return {"tool": request.tool_name, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tool execution failed: {str(e)}")


@app.get("/api/knowledge-base/stats")
async def knowledge_base_stats():
    """Get statistics about the knowledge base"""
    from tools.knowledge_base import kb
    return {
        "total_documents": len(kb.documents),
        "index_size": kb.index.ntotal if kb.index else 0,
        "dimension": kb.dimension
    }


# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


# Agent tool definitions (for OpenAI Agent Builder registration)
AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search the internal knowledge base for company policies, procedures, FAQs, and support information. Use this first for any questions about account management, products, or services.",
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
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for external information like current market data, news, or information not available in the internal knowledge base. Use this for real-time data or general information.",
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
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_compound_interest",
            "description": "Calculate compound interest for investments. Useful when users ask about investment growth, savings calculations, or interest calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "principal": {
                        "type": "number",
                        "description": "The initial investment amount in dollars"
                    },
                    "rate": {
                        "type": "number",
                        "description": "The annual interest rate as a percentage (e.g., 5 for 5%)"
                    },
                    "time": {
                        "type": "number",
                        "description": "The time period in years"
                    },
                    "compounds_per_year": {
                        "type": "integer",
                        "description": "Number of times interest is compounded per year (default: 12 for monthly)"
                    }
                },
                "required": ["principal", "rate", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_investment_returns",
            "description": "Analyze investment returns and calculate metrics like CAGR and total return percentage. Use when users want to understand their investment performance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "initial": {
                        "type": "number",
                        "description": "Initial investment amount in dollars"
                    },
                    "final": {
                        "type": "number",
                        "description": "Final investment value in dollars"
                    },
                    "years": {
                        "type": "number",
                        "description": "Number of years invested"
                    }
                },
                "required": ["initial", "final", "years"]
            }
        }
    }
]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=config.PORT, reload=True)

