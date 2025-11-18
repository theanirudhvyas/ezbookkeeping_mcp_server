from mcp.server.fastmcp import FastMCP
from typing import Optional
from datetime import datetime

# Create the MCP server instance
mcp = FastMCP("EZBookkeeping")

# Example Tool: Add a transaction
@mcp.tool()
def add_transaction(
    amount: float,
    description: str,
    category: str,
    transaction_type: str = "expense"
) -> dict:
    """
    Add a new transaction to the bookkeeping system.

    Args:
        amount: Transaction amount
        description: Description of the transaction
        category: Category (e.g., 'food', 'transport', 'salary')
        transaction_type: Type of transaction ('expense' or 'income')

    Returns:
        Dictionary with transaction details and confirmation
    """
    transaction = {
        "id": f"txn_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "amount": amount,
        "description": description,
        "category": category,
        "type": transaction_type,
        "date": datetime.now().isoformat()
    }
    return {
        "status": "success",
        "message": f"Transaction added: {transaction_type} of ${amount}",
        "transaction": transaction
    }

# Example Tool: Calculate total
@mcp.tool()
def calculate_balance(transactions: list[dict]) -> dict:
    """
    Calculate the balance from a list of transactions.

    Args:
        transactions: List of transaction dictionaries with 'amount' and 'type' fields

    Returns:
        Dictionary with income, expenses, and balance totals
    """
    income = sum(t["amount"] for t in transactions if t.get("type") == "income")
    expenses = sum(t["amount"] for t in transactions if t.get("type") == "expense")
    balance = income - expenses

    return {
        "income": income,
        "expenses": expenses,
        "balance": balance
    }

# Example Resource: Get bookkeeping summary
@mcp.resource("bookkeeping://summary/{period}")
def get_summary(period: str) -> str:
    """
    Get a bookkeeping summary for the specified period.

    Args:
        period: Time period ('today', 'week', 'month', 'year')

    Returns:
        Summary report as a string
    """
    return f"""
Bookkeeping Summary for {period}:
- Total Income: $0.00
- Total Expenses: $0.00
- Balance: $0.00

Note: This is a demo server. Connect to a real database for actual data.
"""

# Example Prompt: Generate financial report
@mcp.prompt()
def create_financial_report(period: str = "month", format: str = "detailed") -> str:
    """
    Generate a prompt for creating a financial report.

    Args:
        period: Time period for the report
        format: Report format ('summary' or 'detailed')

    Returns:
        Prompt string for the LLM
    """
    if format == "summary":
        return f"Please create a brief financial summary for the {period} including total income, expenses, and balance."
    else:
        return f"""Please create a detailed financial report for the {period} including:
1. Total income broken down by category
2. Total expenses broken down by category
3. Net balance
4. Key insights and spending patterns
5. Recommendations for improvement
"""
