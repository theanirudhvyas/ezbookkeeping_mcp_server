# Quick Start Guide

## Running the Server

### Development Mode (with MCP Inspector)
```bash
uv run mcp dev main.py
```
Opens a web UI at http://localhost:5173 to test your server interactively.

### Install in Claude Desktop
```bash
uv run mcp install main.py
```
Or manually configure in `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "ezbookkeeping": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/viki/code/ezbookkeeping_mcp_server",
        "run",
        "mcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

## Available Capabilities

### Tools

#### add_transaction
Add a transaction to the bookkeeping system.
```python
Parameters:
- amount: float (required)
- description: str (required)  
- category: str (required)
- transaction_type: str (default: "expense", options: "expense" or "income")

Example:
add_transaction(
    amount=45.99,
    description="Lunch at cafe",
    category="food",
    transaction_type="expense"
)
```

#### calculate_balance
Calculate totals from a list of transactions.
```python
Parameters:
- transactions: list[dict] (required)
  Each transaction should have "amount" and "type" fields

Example:
calculate_balance([
    {"amount": 2000, "type": "income"},
    {"amount": 50, "type": "expense"}
])
# Returns: {"income": 2000, "expenses": 50, "balance": 1950}
```

### Resources

#### bookkeeping://summary/{period}
Get a summary report for a time period.
```
URI pattern: bookkeeping://summary/{period}
Parameters:
- period: str (e.g., "today", "week", "month", "year")

Example:
bookkeeping://summary/month
```

### Prompts

#### create_financial_report
Generate a prompt for creating financial reports.
```python
Parameters:
- period: str (default: "month")
- format: str (default: "detailed", options: "summary" or "detailed")

Example:
create_financial_report(period="week", format="summary")
```

## Testing

Run the MCP Inspector to test all capabilities:
```bash
uv run mcp dev main.py
```

The inspector lets you:
- Call tools with different parameters
- Access resources by URI
- Generate prompts
- View request/response logs

## Next Steps

1. **Add Database**: Replace in-memory data with SQLite/PostgreSQL
2. **Add More Tools**: Create tools for budgets, reports, exports
3. **Add More Resources**: Expose transaction history, categories, etc.
4. **Error Handling**: Add validation and better error messages
5. **Testing**: Add pytest tests for your tools and resources
