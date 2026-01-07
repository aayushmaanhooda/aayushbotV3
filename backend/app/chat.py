"""
Chat endpoint using the unified agent
"""

import asyncio
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import sys
from pathlib import Path

# Add backend directory to Python path so we can import agents
backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))

from agents.agent import create_unified_agent, Context
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("GITHUB_USERNAME")


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    thread_id: Optional[str] = "default-thread"


class ChatResponse(BaseModel):
    response: str
    thread_id: str


# Global agent instance (initialized on first request)
_agent = None
_agent_lock = asyncio.Lock()


async def get_agent():
    """Get or create the unified agent instance."""
    global _agent

    async with _agent_lock:
        if _agent is None:
            print("🤖 Initializing unified agent...")
            print(f"📝 System prompt version: Using latest prompt from prompts.py")
            _agent = await create_unified_agent()
            print("✅ Agent ready!")
        return _agent


async def reset_agent():
    """Force reset the agent instance (clears cache)."""
    global _agent
    async with _agent_lock:
        if _agent is not None:
            print("🔄 Resetting agent instance...")
            _agent = None
            print("✅ Agent reset complete. Will reinitialize on next chat request.")


async def chat_with_agent(request: ChatRequest) -> ChatResponse:
    """
    Process a chat request using the unified agent.

    Args:
        request: ChatRequest with messages and thread_id

    Returns:
        ChatResponse with the agent's response
    """
    try:
        # Get the agent instance
        agent = await get_agent()

        # Convert Pydantic messages to LangChain format
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        # Configure with thread_id for conversation persistence
        config = {"configurable": {"thread_id": request.thread_id}}

        # Invoke the agent
        response = await agent.ainvoke(
            {"messages": messages},
            config=config,
            context=Context(github_login=username),
        )

        # Extract the assistant's response
        assistant_message = response["messages"][-1].content

        return ChatResponse(response=assistant_message, thread_id=request.thread_id)

    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")
