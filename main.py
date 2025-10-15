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


class MessageRequest(BaseModel):
    """Request model for sending a message"""
    thread_id: str
    content: str
    role: str = "user"
    file_ids: Optional[list[str]] = None


class RunRequest(BaseModel):
    """Request model for running the assistant"""
    thread_id: str
    instructions: Optional[str] = None


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
    Creates a thread for the conversation and returns session details.
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
        
        # Create a new thread for this conversation session
        # Each thread represents a conversation context with the assistant
        thread = client.beta.threads.create(
            metadata={
                "user_id": request.user_id or "anonymous",
                **(request.metadata or {})
            }
        )
        
        # Return the thread ID as the session ID
        # The thread ID is used to maintain conversation context
        return SessionResponse(
            session_id=thread.id,
            client_secret=config.OPENAI_API_KEY,  # Backend uses API key; frontend shouldn't expose this
            agent_id=config.OPENAI_AGENT_ID
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@app.post("/api/chatkit/start", response_model=ClientSecretResponse)
async def start_chatkit_session():
    """
    Start a new ChatKit session and return a client secret.
    This is called when the user first opens the chat.
    Note: In a production environment, you should generate a temporary token
    instead of exposing the API key directly to the frontend.
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
        
        # For ChatKit frontend integration, return the API key
        # WARNING: In production, implement a token-based auth system
        # to avoid exposing your API key directly to the frontend
        # Consider using JWT tokens or OpenAI's session tokens
        return ClientSecretResponse(client_secret=config.OPENAI_API_KEY)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start session: {str(e)}")


@app.post("/api/chatkit/refresh", response_model=ClientSecretResponse)
async def refresh_chatkit_session(request: RefreshRequest):
    """
    Refresh an existing ChatKit session and return a new client secret.
    This is called when the current client secret expires.
    Note: With the current implementation using API keys, tokens don't expire.
    In production, implement proper token rotation with JWT or session tokens.
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
        
        # Verify the current client secret is valid
        if request.currentClientSecret != config.OPENAI_API_KEY:
            raise HTTPException(
                status_code=401,
                detail="Invalid client secret provided"
            )
        
        # In production, generate and return a new token
        # For now, return the same API key
        return ClientSecretResponse(client_secret=config.OPENAI_API_KEY)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh session: {str(e)}")


@app.post("/api/chatkit/message")
async def send_message(request: MessageRequest):
    """
    Send a message to a thread.
    This adds a user message to the conversation thread.
    """
    try:
        if not config.OPENAI_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured."
            )
        
        # Create a message in the thread
        message = client.beta.threads.messages.create(
            thread_id=request.thread_id,
            role=request.role,
            content=request.content,
            file_ids=request.file_ids or []
        )
        
        return {
            "message_id": message.id,
            "thread_id": request.thread_id,
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")


@app.post("/api/chatkit/run")
async def run_assistant(request: RunRequest):
    """
    Run the assistant on a thread to generate a response.
    This processes all messages in the thread and generates an assistant response.
    """
    try:
        if not config.OPENAI_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured."
            )
        
        if not config.OPENAI_AGENT_ID:
            raise HTTPException(
                status_code=500,
                detail="Agent ID not configured."
            )
        
        # Create a run to process the thread with the assistant
        run = client.beta.threads.runs.create(
            thread_id=request.thread_id,
            assistant_id=config.OPENAI_AGENT_ID,
            instructions=request.instructions
        )
        
        return {
            "run_id": run.id,
            "thread_id": request.thread_id,
            "status": run.status,
            "assistant_id": run.assistant_id,
            "created_at": run.created_at
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run assistant: {str(e)}")


@app.get("/api/chatkit/run/{thread_id}/{run_id}")
async def get_run_status(thread_id: str, run_id: str):
    """
    Get the status of a run.
    Use this to poll for run completion and get the assistant's response.
    """
    try:
        if not config.OPENAI_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured."
            )
        
        # Retrieve the run status
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        
        response = {
            "run_id": run.id,
            "status": run.status,
            "thread_id": run.thread_id,
            "assistant_id": run.assistant_id,
            "created_at": run.created_at,
            "completed_at": run.completed_at,
            "failed_at": run.failed_at,
            "cancelled_at": run.cancelled_at,
            "expires_at": run.expires_at
        }
        
        # If run requires action (function calling), include required actions
        if run.status == "requires_action":
            response["required_action"] = run.required_action
        
        # If completed, retrieve the latest messages
        if run.status == "completed":
            messages = client.beta.threads.messages.list(
                thread_id=thread_id,
                order="desc",
                limit=1
            )
            if messages.data:
                latest_message = messages.data[0]
                response["latest_message"] = {
                    "id": latest_message.id,
                    "role": latest_message.role,
                    "content": latest_message.content
                }
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get run status: {str(e)}")


@app.get("/api/chatkit/messages/{thread_id}")
async def get_thread_messages(thread_id: str, limit: int = 20, order: str = "desc"):
    """
    Get messages from a thread.
    Retrieve the conversation history for a given thread.
    """
    try:
        if not config.OPENAI_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured."
            )
        
        # Retrieve messages from the thread
        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            order=order,
            limit=limit
        )
        
        return {
            "thread_id": thread_id,
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "created_at": msg.created_at,
                    "file_ids": msg.file_ids
                }
                for msg in messages.data
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get messages: {str(e)}")


@app.post("/api/chatkit/tool-output")
async def submit_tool_output(thread_id: str, run_id: str, tool_outputs: list[Dict[str, Any]]):
    """
    Submit tool outputs when the assistant requires action.
    This is used when the assistant calls functions/tools and needs the results.
    """
    try:
        if not config.OPENAI_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured."
            )
        
        # Submit tool outputs to continue the run
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )
        
        return {
            "run_id": run.id,
            "status": run.status,
            "thread_id": thread_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit tool output: {str(e)}")


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

