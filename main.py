"""EzBookkeeping MCP Server - Main entry point."""
from mcp.server.fastmcp import FastMCP
from src.tools.transactions import add_transaction, get_transactions
from src.resources.accounts import get_accounts, get_account_by_id

# Create the MCP server instance
mcp = FastMCP("EzBookkeeping")


# ============================================================================
# TOOLS (Write Operations)
# ============================================================================

@mcp.tool()
def create_transaction(
    amount: float,
    description: str,
    account_id: str,
    category_id: str,
    transaction_type: int = 1
) -> dict:
    """
    Create a new transaction in EzBookkeeping.
    
    Args:
        amount: Transaction amount in dollars (e.g., 45.99)
        description: Description of the transaction
        account_id: ID of the account
        category_id: ID of the category
        transaction_type: Type of transaction (1=Expense, 2=Income, 3=Transfer Out, 4=Transfer In)
    
    Returns:
        Dictionary with transaction details and confirmation
    """
    return add_transaction(
        amount=amount,
        description=description,
        account_id=account_id,
        category_id=category_id,
        transaction_type=transaction_type
    )


@mcp.tool()
def list_transactions(
    max_count: int = 50,
    account_id: str = None,
    category_id: str = None
) -> dict:
    """
    List recent transactions from EzBookkeeping.
    
    Args:
        max_count: Maximum number of transactions to return (default: 50)
        account_id: Optional - filter by account ID
        category_id: Optional - filter by category ID
    
    Returns:
        Dictionary with list of transactions
    """
    return get_transactions(
        max_count=max_count,
        account_id=account_id,
        category_id=category_id
    )


# ============================================================================
# RESOURCES (Read Operations)
# ============================================================================

@mcp.resource("ezbookkeeping://accounts")
def list_all_accounts() -> str:
    """
    Get all accounts from EzBookkeeping.
    
    Returns:
        JSON string with all accounts
    """
    import json
    result = get_accounts()
    return json.dumps(result, indent=2)


@mcp.resource("ezbookkeeping://accounts/{account_id}")
def get_account_details(account_id: str) -> str:
    """
    Get specific account details by ID.
    
    Args:
        account_id: Account ID
    
    Returns:
        JSON string with account details
    """
    import json
    result = get_account_by_id(account_id)
    return json.dumps(result, indent=2)


# ============================================================================
# PROMPTS (AI Templates)
# ============================================================================

@mcp.prompt()
def analyze_spending(period: str = "month") -> str:
    """
    Generate a prompt for analyzing spending patterns.
    
    Args:
        period: Time period to analyze (week, month, quarter, year)
    
    Returns:
        Prompt string for the LLM
    """
    return f"""Please analyze my spending for the {period} and provide:

1. Total spending by category
2. Top 5 expenses
3. Spending trends compared to previous {period}
4. Unusual or noteworthy transactions
5. Budget recommendations

Please be specific with amounts and percentages."""


@mcp.prompt()
def budget_review(category: str = "all") -> str:
    """
    Generate a prompt for budget review.
    
    Args:
        category: Category to review (or "all" for all categories)
    
    Returns:
        Prompt string for the LLM
    """
    if category == "all":
        return """Please review my overall budget and provide:

1. Budget vs actual spending by category
2. Categories where I'm over/under budget
3. Recommendations for adjusting budgets
4. Tips for staying within budget"""
    else:
        return f"""Please review my budget for the {category} category and provide:

1. Budget vs actual spending
2. Whether I'm on track for this category
3. Specific recommendations for this category
4. Comparison with similar periods"""
