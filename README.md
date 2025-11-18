# EzBookkeeping MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0-green.svg)](https://modelcontextprotocol.io)

A comprehensive Model Context Protocol (MCP) server that integrates AI assistants with [EzBookkeeping](https://github.com/mayswind/ezbookkeeping), enabling natural language interactions for personal finance management.

> **Note:** This project is currently in active development. The server currently includes example/demo implementations. Full integration with the EzBookkeeping API is planned based on the comprehensive research documented in this repository.

## What is This?

This MCP server allows AI assistants like Claude to interact with your EzBookkeeping instance through natural language. Ask Claude to add transactions, check balances, analyze spending patterns, and generate financial reports - all through conversation.

**Example interactions:**
- "Add a $45 grocery expense to my checking account"
- "Show me my spending trends for this month"
- "What's my total balance across all accounts?"
- "Create a budget report for the last quarter"

## Features

### Current (Demo Implementation)

**Tools (Write Operations):**
- `add_transaction` - Add income or expense transactions
- `calculate_balance` - Calculate balance from transaction lists

**Resources (Read Operations):**
- `bookkeeping://summary/{period}` - Get financial summary for a period

**Prompts (AI Templates):**
- `create_financial_report` - Generate financial report prompts

### Planned (Full EzBookkeeping Integration)

Based on comprehensive API research (99 endpoints documented):

**Transaction Management:**
- Create, update, delete transactions
- Batch operations
- AI-powered receipt recognition
- Transaction statistics and trends
- Import/export functionality

**Account Management:**
- Manage accounts across 9 types (Cash, Credit Card, Investment, etc.)
- Multi-currency support
- Hierarchical accounts with sub-accounts

**Organization:**
- Category and tag management
- Transaction templates
- Recurring transactions

**Analytics:**
- Spending analysis and trends
- Budget tracking
- Financial summaries and reports

See [MCP_SERVER_DESIGN.md](MCP_SERVER_DESIGN.md) for the complete architecture plan.

## Installation

### Prerequisites
- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- (Optional) An EzBookkeeping instance for full API integration

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/theanirudhvyas/ezbookkeeping_mcp_server.git
cd ezbookkeeping_mcp_server
```

2. **Install dependencies:**
```bash
uv sync
```

3. **Configure (for full EzBookkeeping integration):**
```bash
cp .env.example .env
# Edit .env with your EzBookkeeping instance URL and API token
```

4. **Test the server:**
```bash
uv run mcp dev main.py
```

This opens the MCP Inspector at `http://localhost:5173` for interactive testing.

## Configuration

For full EzBookkeeping API integration, configure the following environment variables:

```bash
# Required
EZBOOKKEEPING_URL=https://your-instance.com
EZBOOKKEEPING_TOKEN=your_api_token_here

# Optional
EZBOOKKEEPING_TIMEZONE_OFFSET=0
EZBOOKKEEPING_DEFAULT_CURRENCY=USD
```

See `.env.example` for a complete configuration template.

## Usage with Claude Desktop

### Automatic Installation
```bash
uv run mcp install main.py
```

### Manual Configuration

Add to your Claude Desktop config file:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

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
      ],
      "env": {
        "EZBOOKKEEPING_URL": "https://your-instance.com",
        "EZBOOKKEEPING_TOKEN": "your_token"
      }
    }
  }
}
```

Restart Claude Desktop to load the server.

## Development

### Running the MCP Inspector

The MCP Inspector provides an interactive web interface for testing:

```bash
uv run mcp dev main.py
```

Opens at `http://localhost:5173` with:
- Tool testing with parameter forms
- Resource browsing
- Prompt generation
- Real-time request/response logs

### Running Tests

```bash
# Install dev dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=html
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
├── main.py                    # MCP server implementation
├── pyproject.toml             # Project configuration & dependencies
├── API_DOCUMENTATION.md       # Complete EzBookkeeping API reference (99 endpoints)
├── MCP_SERVER_DESIGN.md       # Architecture and implementation plan
├── QUICKSTART.md              # Quick reference guide
├── README.md                  # This file
├── CONTRIBUTING.md            # Contribution guidelines
├── CHANGELOG.md               # Version history
├── LICENSE                    # MIT License
├── .env.example               # Environment configuration template
├── .claude/                   # Claude Code configuration
│   └── CLAUDE.md              # MCP development best practices
├── tests/                     # Test suite (planned)
└── .venv/                     # Virtual environment (gitignored)
```

## Documentation

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete EzBookkeeping API reference with all 99 endpoints
- **[MCP_SERVER_DESIGN.md](MCP_SERVER_DESIGN.md)** - Comprehensive architecture, design decisions, and roadmap
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide for common operations
- **[.claude/CLAUDE.md](.claude/CLAUDE.md)** - MCP server development best practices

## Roadmap

### Phase 1: Foundation (Planned)
- [ ] HTTP client with authentication
- [ ] Token management and refresh
- [ ] Error handling and retry logic
- [ ] Timezone support

### Phase 2: Core Features (Planned)
- [ ] Transaction tools (add, update, delete)
- [ ] Account resources (list, get)
- [ ] Transaction resources (list, statistics)
- [ ] Category/tag resources

### Phase 3: Advanced Features (Planned)
- [ ] Batch operations
- [ ] Transaction templates
- [ ] AI receipt recognition integration
- [ ] Export functionality
- [ ] Exchange rate management

### Phase 4: Intelligence (Planned)
- [ ] Spending analysis prompts
- [ ] Budget tracking prompts
- [ ] Financial insights generation
- [ ] Duplicate detection
- [ ] Category suggestions

See [MCP_SERVER_DESIGN.md](MCP_SERVER_DESIGN.md) for detailed implementation plan.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- Implementing API endpoints
- Adding tests
- Improving error handling
- Documentation improvements
- Feature suggestions

## Support

- **Issues:** [GitHub Issues](https://github.com/theanirudhvyas/ezbookkeeping_mcp_server/issues)
- **Discussions:** [GitHub Discussions](https://github.com/theanirudhvyas/ezbookkeeping_mcp_server/discussions)
- **EzBookkeeping:** [Official Documentation](https://ezbookkeeping.mayswind.net)

## Related Projects

- [EzBookkeeping](https://github.com/mayswind/ezbookkeeping) - The personal bookkeeping application
- [Model Context Protocol](https://modelcontextprotocol.io) - MCP specification and documentation
- [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk) - Official Python SDK

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [EzBookkeeping](https://github.com/mayswind/ezbookkeeping) by [@mayswind](https://github.com/mayswind) for the excellent personal finance application
- [Model Context Protocol](https://modelcontextprotocol.io) by Anthropic for the integration framework
- The MCP community for tools and resources

## Disclaimer

This project is not officially affiliated with or endorsed by the EzBookkeeping project. It is an independent integration built using EzBookkeeping's public HTTP API.
