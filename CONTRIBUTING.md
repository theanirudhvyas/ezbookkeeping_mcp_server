# Contributing to EzBookkeeping MCP Server

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Assume good intentions

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When filing a bug report, include:**
- Clear, descriptive title
- Steps to reproduce the behavior
- Expected vs actual behavior
- Environment details (OS, Python version, uv version)
- Relevant logs or error messages
- Screenshots if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**When suggesting an enhancement:**
- Use a clear, descriptive title
- Provide detailed description of the proposed functionality
- Explain why this enhancement would be useful
- List any alternative solutions you've considered

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the coding standards** (see below)
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Ensure tests pass** before submitting
6. **Write clear commit messages** following conventional commits

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ezbookkeeping_mcp_server.git
cd ezbookkeeping_mcp_server

# Install dependencies
uv sync

# Run tests
uv run pytest

# Run the MCP Inspector for testing
uv run mcp dev main.py
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Code Organization

```python
# Good
@mcp.tool()
def create_transaction(
    amount: float,
    description: str,
    category_id: str,
    account_id: str
) -> dict:
    """
    Create a new transaction in EzBookkeeping.

    Args:
        amount: Transaction amount (positive for income, negative for expense)
        description: Transaction description
        category_id: Category ID
        account_id: Account ID

    Returns:
        Dictionary with transaction details and creation status
    """
    # Implementation
    pass
```

### Documentation Standards

- All functions must have docstrings (Google style)
- Include type hints for all parameters and return values
- Document exceptions that can be raised
- Add inline comments for complex logic
- Update README.md for new features

### Testing Standards

- Write tests for all new functionality
- Aim for 80%+ code coverage
- Use descriptive test names
- Include both positive and negative test cases

```python
def test_create_transaction_success():
    """Test successful transaction creation with valid data."""
    pass

def test_create_transaction_invalid_amount():
    """Test transaction creation fails with invalid amount."""
    pass
```

## Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(transactions): add batch delete functionality

Implements batch deletion of transactions using the EzBookkeeping
/data-management/clear.json endpoint.

Closes #123
```

```
fix(auth): handle token refresh errors gracefully

- Add retry logic for token refresh
- Improve error messages
- Add logging for debugging

Fixes #456
```

## Pull Request Process

1. **Update documentation** - Ensure README.md, CHANGELOG.md, and code comments reflect your changes

2. **Add tests** - New features must include tests

3. **Pass CI checks** - All tests must pass and code must pass linting

4. **Update CHANGELOG.md** - Add your changes under "Unreleased"

5. **Request review** - Tag relevant maintainers

6. **Address feedback** - Respond to review comments promptly

7. **Squash commits** (if needed) - Maintainers may ask you to squash commits before merging

## Project Structure

```
ezbookkeeping_mcp_server/
├── main.py                   # Main MCP server entry point
├── tools/                    # Tool implementations (planned)
│   ├── transactions.py
│   ├── accounts.py
│   └── categories.py
├── resources/                # Resource implementations (planned)
│   ├── accounts.py
│   └── transactions.py
├── prompts/                  # Prompt templates (planned)
├── utils/                    # Utility functions (planned)
│   ├── auth.py
│   └── http_client.py
├── tests/                    # Test suite
│   ├── test_tools.py
│   ├── test_resources.py
│   └── test_auth.py
└── docs/                     # Additional documentation
```

## Implementation Priorities

See [MCP_SERVER_DESIGN.md](MCP_SERVER_DESIGN.md) for the full roadmap. Current priorities:

### Phase 1: Foundation
1. HTTP client with authentication
2. Token management and refresh
3. Error handling framework
4. Timezone support

### Phase 2: Core Features
1. Transaction tools (add, update, delete)
2. Account resources (list, get)
3. Category/tag resources

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=html

# Run specific test file
uv run pytest tests/test_transactions.py

# Run with verbose output
uv run pytest -v

# Run and show print statements
uv run pytest -s
```

## MCP Inspector Testing

Always test your changes with the MCP Inspector:

```bash
uv run mcp dev main.py
```

Test checklist:
- [ ] All tools execute without errors
- [ ] Resources return expected data
- [ ] Prompts generate useful output
- [ ] Error handling works correctly
- [ ] Authentication flow works

## Documentation

### README Updates

When adding features, update:
- Features list
- Usage examples
- Configuration options
- Troubleshooting section

### API Documentation

When implementing endpoints:
1. Reference [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
2. Include endpoint path in docstring
3. Document all parameters
4. Include example usage

### Code Comments

```python
# Good: Explains WHY
# Use batch endpoint to reduce API calls when deleting 100+ transactions
result = batch_delete_transactions(transaction_ids)

# Bad: Explains WHAT (obvious from code)
# Call batch delete function
result = batch_delete_transactions(transaction_ids)
```

## Getting Help

- **Questions:** Open a [GitHub Discussion](https://github.com/YOUR_USERNAME/ezbookkeeping_mcp_server/discussions)
- **Bugs:** File an [issue](https://github.com/YOUR_USERNAME/ezbookkeeping_mcp_server/issues)
- **Chat:** Join discussions in existing issues/PRs

## Recognition

Contributors will be:
- Listed in README.md acknowledgments
- Mentioned in release notes
- Given credit in git commit co-authors when applicable

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions help make this project better for everyone. We appreciate your time and effort!
