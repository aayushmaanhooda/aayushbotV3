import asyncio
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langgraph.checkpoint.memory import InMemorySaver
from dataclasses import dataclass
from dotenv import load_dotenv
import os

# Import custom tools and functions
try:
    # Try relative imports first (when running from agents directory)
    from tools import now_tool, age_calculator, web_search_tool
    from rag import retrieve_context
    from hubmcp import get_mcp_tools
    from prompts import agent_system_prompt
except ImportError:
    # Fall back to absolute imports (when imported from app directory)
    from agents.tools import now_tool, age_calculator, web_search_tool
    from agents.rag import retrieve_context
    from agents.hubmcp import get_mcp_tools
    from agents.prompts import agent_system_prompt

load_dotenv()

username = os.getenv("GITHUB_USERNAME")


@dataclass
class Context:
    github_login: str


@dynamic_prompt
def login_prompt(request: ModelRequest):
    """Dynamic prompt that injects GitHub username into context."""
    login = getattr(request.runtime.context, "github_login", "unknown")
    return f"The GitHub Username we are talking about is: {login}"


async def create_unified_agent():
    """Create a unified agent with all tools: MCP, RAG, and custom tools."""

    # Get MCP GitHub tools
    print("🔧 Loading MCP GitHub tools...")
    mcp_tools = await get_mcp_tools()

    # Combine all tools
    all_tools = [
        # Custom utility tools
        now_tool,
        age_calculator,
        web_search_tool,
        # RAG tool for personal info
        retrieve_context,
    ] + list(mcp_tools)

    print(f"✅ Total tools loaded: {len(all_tools)}")

    # Initialize model and checkpointer
    model = init_chat_model("gpt-4o")
    checkpointer = InMemorySaver()

    # Create unified agent
    agent = create_agent(
        model=model,
        tools=all_tools,
        system_prompt=agent_system_prompt,
        middleware=[login_prompt],
        context_schema=Context,
        checkpointer=checkpointer,
    )

    print("✅ Unified Agent created successfully!")
    return agent


async def chat_loop():
    """Terminal-based chat interface for the unified agent."""

    # Create the agent
    agent = await create_unified_agent()

    # Configuration for conversation threading
    config = {"configurable": {"thread_id": "thread-1"}}

    print("\n" + "=" * 60)
    print("🤖 Aayushmaan's AI Assistant - Unified Agent")
    print("=" * 60)
    print("Type 'bye', 'exit', or 'quit' to end the conversation")
    print("=" * 60 + "\n")

    # Chat loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            # Exit conditions
            if user_input.lower() in ["bye", "exit", "quit"]:
                print("\n👋 Goodbye! Have a great day!")
                break

            # Skip empty inputs
            if not user_input:
                continue

            # Invoke agent
            response = await agent.ainvoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ]
                },
                config=config,
                context=Context(github_login=username),
            )

            # Display response
            assistant_message = response["messages"][-1].content
            print(f"\n🤖 Assistant: {assistant_message}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted! Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            continue


if __name__ == "__main__":
    # Run the async chat loop
    asyncio.run(chat_loop())
