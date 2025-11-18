# EZBookkeeping MCP Server

A Model Context Protocol (MCP) server for bookkeeping and financial management. This server provides tools, resources, and prompts for managing transactions and generating financial reports.

## Features

### Tools
- `add_transaction` - Add income or expense transactions
- `calculate_balance` - Calculate balance from transaction lists

### Resources
- `bookkeeping://summary/{period}` - Get financial summary for a period

### Prompts
- `create_financial_report` - Generate financial report prompts

## Installation

### Prerequisites
- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

1. Clone the repository:
```bash
cd ezbookkeeping_mcp_server
```

2. Install dependencies:
```bash
uv sync
```

## Development

### Run the server with MCP Inspector
The MCP Inspector provides a web interface to test your server:

```bash
uv run mcp dev main.py
```

This will start the inspector at `http://localhost:5173` where you can:
- Test tools with different parameters
- Browse available resources
- Try out prompts
- View server logs

### Install in Claude Desktop

To use this server with Claude Desktop:

```bash
uv run mcp install main.py
```

Or manually add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "ezbookkeeping": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/ezbookkeeping_mcp_server",
        "run",
        "mcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

## Usage Examples

### Adding a Transaction
```python
# Using the add_transaction tool
add_transaction(
    amount=50.00,
    description="Grocery shopping",
    category="food",
    transaction_type="expense"
)
```

### Calculating Balance
```python
# Using the calculate_balance tool
transactions = [
    {"amount": 1000, "type": "income"},
    {"amount": 50, "type": "expense"},
    {"amount": 30, "type": "expense"}
]
calculate_balance(transactions)
# Returns: {"income": 1000, "expenses": 80, "balance": 920}
```

### Getting a Summary
Access the resource URI:
```
bookkeeping://summary/month
```

## Project Structure

```
ezbookkeeping_mcp_server/
├── main.py              # MCP server implementation
├── pyproject.toml       # Project configuration
├── uv.lock             # Dependency lock file
├── .venv/              # Virtual environment
└── README.md           # This file
```

## Next Steps

This is a basic example server. To make it production-ready, consider:

1. **Database Integration**: Connect to SQLite, PostgreSQL, or MongoDB
2. **Authentication**: Add user authentication and authorization
3. **Data Persistence**: Store transactions permanently
4. **Advanced Features**:
   - Budget tracking and alerts
   - Category management
   - Recurring transactions
   - Export to CSV/PDF
   - Multi-currency support
5. **Testing**: Add pytest tests
6. **Error Handling**: Improve validation and error messages

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Guide](https://github.com/modelcontextprotocol/python-sdk#fastmcp)

## License

MIT
