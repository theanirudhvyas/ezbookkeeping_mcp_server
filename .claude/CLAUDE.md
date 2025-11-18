# EZBookkeeping MCP Server - Development Guide

## MCP Server Development Best Practices

### Core Architecture

**Server Setup**
```python
from mcp.server.fastmcp import FastMCP

# Create server instance
mcp = FastMCP("ServerName")

# With lifespan management for resources
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan():
    # Startup: initialize DB, load configs, etc.
    db = await connect_database()
    yield {"db": db}  # Dependencies available to tools
    # Shutdown: cleanup
    await db.close()

mcp = FastMCP("ServerName", lifespan=lifespan)
```

**Transport Mechanisms**
- `stdio`: For local processes (recommended for Claude Desktop)
- `HTTP/SSE`: For networked communication

### Tools Design

Tools perform actions with side effects (like POST/PUT endpoints).

**Best Practices:**
```python
@mcp.tool()
def create_task(
    title: str,
    description: str,
    priority: int = 1,
    tags: list[str] | None = None
) -> dict:
    """
    Create a new task.

    Args:
        title: Task title (required)
        description: Detailed description (required)
        priority: Priority level 1-5 (default: 1)
        tags: Optional list of tags

    Returns:
        Dictionary with task details and ID
    """
    # Type annotations drive schema generation
    # Use descriptive names and docstrings
    # Return structured data (dict, Pydantic models, dataclass)
    pass
```

**Structured Output with Pydantic:**
```python
from pydantic import BaseModel

class TaskResult(BaseModel):
    id: str
    status: str
    created_at: str

@mcp.tool()
def create_task(title: str) -> TaskResult:
    """Return type enforces schema validation"""
    return TaskResult(id="123", status="created", created_at="2025-01-01")
```

**Context Access:**
```python
from mcp.server.fastmcp import Context

@mcp.tool()
async def long_operation(ctx: Context) -> str:
    """Access logging and progress reporting"""
    ctx.info("Starting operation...")
    await ctx.report_progress(50, 100)
    ctx.debug("Processing step 2...")
    return "Done"
```

### Resources Pattern

Resources expose read-only data (like GET endpoints).

**Static Resources:**
```python
@mcp.resource("config://settings")
def get_settings() -> str:
    """Expose configuration data"""
    return '{"theme": "dark", "version": "1.0"}'
```

**Template Resources (Parameterized):**
```python
@mcp.resource("file://documents/{path}")
def read_file(path: str) -> str:
    """
    Read file by path.

    URI params automatically map to function parameters.
    Stored as resource templates, accessible via pattern matching.
    """
    return f"Contents of {path}"
```

**Resource Guidelines:**
- Use for data retrieval without side effects
- Template URIs with `{parameter}` syntax
- Keep responses focused and cacheable
- Return strings, bytes, or JSON-serializable data

### Prompts

Create reusable prompt templates for common LLM tasks.

```python
@mcp.prompt()
def analyze_code(
    language: str = "python",
    focus: str = "security"
) -> str:
    """Generate code analysis prompt"""
    focuses = {
        "security": "security vulnerabilities and best practices",
        "performance": "performance bottlenecks and optimizations",
        "style": "code style and readability issues"
    }
    return f"Analyze this {language} code for {focuses.get(focus)}."
```

### Error Handling

**Type Validation:**
- FastMCP validates return types automatically
- Invalid returns trigger clear validation errors
- Use type hints extensively for automatic schema generation

**Custom Error Responses:**
```python
from mcp.types import CallToolResult

@mcp.tool()
def risky_operation(param: str) -> CallToolResult:
    """Return CallToolResult for full control"""
    if not param:
        return CallToolResult(
            content=[{"type": "text", "text": "Error: param required"}],
            isError=True
        )
    return CallToolResult(
        content=[{"type": "text", "text": "Success"}]
    )
```

### Security Best Practices

1. **Authentication & Authorization**
   - Implement OAuth 2.0 for sensitive operations
   - Use TLS for all network communication
   - Validate and sanitize all inputs
   - Apply least privilege principle

2. **Input Validation**
   ```python
   @mcp.tool()
   def delete_file(path: str) -> str:
       # Prevent path traversal
       if ".." in path or path.startswith("/"):
           raise ValueError("Invalid path")
       # Validate against allowed patterns
       if not path.startswith("workspace/"):
           raise ValueError("Access denied")
       return f"Deleted {path}"
   ```

3. **Sensitive Data**
   - Never log API keys, tokens, or credentials
   - Use environment variables for secrets
   - Redact sensitive info in responses

### Code Organization

**Project Structure:**
```
my-mcp-server/
├── main.py              # FastMCP server definition
├── tools/               # Tool implementations
│   ├── __init__.py
│   ├── database.py
│   └── api_calls.py
├── resources/           # Resource handlers
│   └── data_loaders.py
├── config.py           # Configuration
├── pyproject.toml      # Dependencies
└── tests/              # Tests
    └── test_tools.py
```

**Separation of Concerns:**
```python
# tools/database.py
async def create_user_in_db(name: str, email: str):
    """Business logic separate from MCP"""
    pass

# main.py
from tools.database import create_user_in_db

@mcp.tool()
async def create_user(name: str, email: str) -> dict:
    """Thin MCP integration layer"""
    result = await create_user_in_db(name, email)
    return {"status": "created", "user": result}
```

### Performance Optimization

1. **Caching:**
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=100)
   def expensive_computation(param: str) -> str:
       """Cache results for frequent calls"""
       pass
   ```

2. **Streaming Responses:**
   - Use for large datasets or long operations
   - Provide progress updates via `Context.report_progress()`

3. **Circuit Breakers:**
   - Fail fast when dependencies are unavailable
   - Return cached/fallback data when possible

### Development & Testing

**MCP Inspector (Development):**
```bash
# Test server interactively
uv run mcp dev main.py

# Opens http://localhost:5173 with:
# - Tool testing with parameters
# - Resource browsing
# - Prompt generation
# - Request/response logs
```

**Integration Testing:**
```python
# tests/test_tools.py
import pytest
from main import mcp

@pytest.mark.asyncio
async def test_create_task():
    result = await mcp._tool_manager.call_tool(
        "create_task",
        {"title": "Test", "description": "Test task"}
    )
    assert result["status"] == "created"
```

### Claude Desktop Integration

**Installation:**
```bash
uv run mcp install main.py
```

**Manual Configuration:**
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/server",
        "run",
        "mcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

### MCP Server Best Practices Summary

**DO:**
- Use descriptive names and comprehensive docstrings
- Leverage type annotations for automatic schema generation
- Return structured data (Pydantic, dataclass, dict)
- Separate business logic from MCP integration
- Validate and sanitize all inputs
- Use lifespan management for resource initialization
- Test with MCP Inspector before deployment
- Version your server and document changes

**DON'T:**
- Mix tools (side effects) with resources (read-only)
- Return untyped complex objects (use annotations)
- Hardcode secrets or credentials
- Allow arbitrary file/path access without validation
- Skip error handling and input validation
- Create monolithic tool functions (keep focused)
- Forget to document parameters and return types

## Project-Specific Notes

### Current Implementation
- Server name: "EZBookkeeping"
- Tools: add_transaction, calculate_balance
- Resources: bookkeeping://summary/{period}
- Prompts: create_financial_report

### Dependencies
- Python >=3.14
- mcp[cli] >=1.21.2
- uv for dependency management
