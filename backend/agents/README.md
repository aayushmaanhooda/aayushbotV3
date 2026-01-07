# Unified AI Agent for Aayushmaan's Assistant

A single, powerful agent that combines GitHub MCP tools, RAG (Retrieval Augmented Generation), and custom utility tools for a comprehensive chatbot experience.

## 🎯 Features

The unified agent includes:

### 1. **GitHub MCP Tools** (26 tools)
- Repository management (create, search, fork)
- File operations (create, update, get contents)
- Issue tracking (create, list, update, comment)
- Pull request management (create, merge, review)
- Code search and user search
- Commit history and activity tracking

### 2. **RAG (Personal Knowledge Base)**
- `retrieve_context`: Retrieves information about Aayushmaan's background, skills, experience, projects, and blogs
- Uses Pinecone vector store for semantic search
- Powered by OpenAI embeddings

### 3. **Custom Utility Tools**
- `now_tool`: Get current date/time (essential for "latest/oldest" queries)
- `age_calculator`: Calculate Aayushmaan's current age
- `web_search_tool`: Search the web for current events and information

## 📁 File Structure

```
agents/
├── agent.py          # Main unified agent with terminal chatbot
├── hubmcp.py         # MCP client setup and GitHub tools
├── rag.py            # RAG setup and retrieve_context tool
├── tools.py          # Custom utility tools
├── prompts.py        # System prompts for the agent
├── setup_rag.py      # One-time script to upload documents
└── ragProfile.pdf    # Personal knowledge base (PDF)
```

## 🚀 Setup

### Prerequisites

1. **Environment Variables** (`.env` file):
```env
# OpenAI
OPENAI_API_KEY=your_openai_key

# GitHub
GITHUB_ACCESS_TOKEN=your_github_token
GITHUB_USERNAME=your_username

# Pinecone
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX=your_index_name

# Tavily (for web search)
TAVILY_API_KEY=your_tavily_key
```

2. **Install Dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

3. **One-Time RAG Setup** (Upload documents to Pinecone):
```bash
cd backend/agents
python setup_rag.py
```
This uploads `ragProfile.pdf` to your Pinecone index. Only run this once!

## 💬 Usage

### Run the Unified Agent

```bash
cd backend/agents
python agent.py
```

This starts a terminal-based chatbot interface:

```
============================================================
🤖 Aayushmaan's AI Assistant - Unified Agent
============================================================
Type 'bye', 'exit', or 'quit' to end the conversation
============================================================

You: 
```

### Example Queries

**GitHub Queries:**
```
You: Show me the latest 3 repos
You: What are my most recent pull requests?
You: Search for Python repositories with AI
You: Create an issue in my project
```

**Personal Info Queries:**
```
You: Who is Aayushmaan?
You: What are his skills?
You: Tell me about his experience
You: What blogs has he written?
```

**Hybrid Queries:**
```
You: Show me his latest projects and background
You: What skills does he have and what repos showcase them?
```

**Utility Queries:**
```
You: What's the current date and time?
You: How old is Aayushmaan?
You: Search the web for latest AI news
```

## 🧠 How It Works

1. **Agent Initialization**: 
   - Loads all MCP GitHub tools asynchronously
   - Combines with RAG and custom tools
   - Creates a single unified agent with all capabilities

2. **Dynamic Context**: 
   - GitHub username is injected via middleware
   - Conversation history is maintained via InMemorySaver checkpointer

3. **Tool Selection**: 
   - The agent intelligently selects which tools to use based on the query
   - Can use multiple tools in sequence for complex queries

4. **Response Generation**: 
   - Processes tool outputs and generates natural language responses
   - Maintains conversation context for follow-up questions

## 🔧 Architecture

```
┌─────────────────────────────────────────────────────┐
│           Unified Agent (GPT-4o)                    │
├─────────────────────────────────────────────────────┤
│  System Prompt: agent_system_prompt                 │
│  Middleware: login_prompt (GitHub context)          │
│  Checkpointer: InMemorySaver (conversation history) │
└─────────────┬───────────────────────────────────────┘
              │
              ├── GitHub MCP Tools (26)
              │   └── Multi-Server MCP Client
              │
              ├── RAG Tool (1)
              │   └── Pinecone Vector Store
              │       └── OpenAI Embeddings
              │
              └── Custom Tools (3)
                  ├── now_tool
                  ├── age_calculator
                  └── web_search_tool
```

## 📝 Key Design Decisions

1. **Async Architecture**: MCP client requires async, so the entire chat loop is async
2. **Tool Separation**: Tools are organized by category for maintainability
3. **One-Time Document Upload**: RAG documents are uploaded once, not on every run
4. **Context Injection**: GitHub username is injected via middleware instead of hardcoding
5. **Conversation Memory**: InMemorySaver maintains context across messages

## 🐛 Troubleshooting

**Issue**: MCP tools not loading
- Check `GITHUB_ACCESS_TOKEN` in `.env`
- Ensure `npx` is installed and accessible

**Issue**: RAG returns empty results
- Run `python setup_rag.py` to upload documents
- Check `PINECONE_API_KEY` and `PINECONE_INDEX`

**Issue**: Web search not working
- Verify `TAVILY_API_KEY` in `.env`

## 🎨 Customization

### Add New Tools
Edit `tools.py` and add your tool decorated with `@tool`:
```python
@tool
def my_custom_tool(param: str) -> str:
    """Tool description for the LLM."""
    # Your logic here
    return result
```

### Modify System Prompt
Edit `prompts.py` to change the agent's behavior and personality.

### Change PDF Source
Replace `ragProfile.pdf` with your own PDF and run `python setup_rag.py` again.

## 📚 Dependencies

- `langchain` - Agent framework
- `langgraph` - Graph-based agent orchestration
- `langchain-mcp-adapters` - MCP protocol support
- `langchain-pinecone` - Vector store integration
- `langchain-openai` - OpenAI models and embeddings
- `langchain-community` - Additional tools and loaders
- `pinecone-client` - Pinecone database
- `python-dotenv` - Environment variable management

## 🤝 Contributing

To extend this agent:
1. Add new tools in respective files (`tools.py`, `rag.py`, etc.)
2. Update `agent.py` to include new tools
3. Modify `prompts.py` to guide the agent on when to use new tools
4. Update this README with usage examples

---

**Built with ❤️ for Aayushmaan's AI Assistant**

