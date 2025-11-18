"""Transaction management tools for EzBookkeeping."""
from typing import Optional
from src.utils.http_client import EzBookkeepingClient


def add_transaction(
    amount: float,
    description: str,
    account_id: str,
    category_id: str,
    transaction_type: int = 1,
    time: Optional[int] = None,
    tags: Optional[list[str]] = None
) -> dict:
    """
    Add a new transaction to EzBookkeeping.
    
    Args:
        amount: Transaction amount (positive number, will be converted to cents)
        description: Transaction description
        account_id: Account ID
        category_id: Category ID  
        transaction_type: Type (1: Expense, 2: Income, 3: Transfer Out, 4: Transfer In)
        time: Unix timestamp in milliseconds (default: now)
        tags: Optional list of tag IDs
        
    Returns:
        Dictionary with transaction details
    """
    with EzBookkeepingClient() as client:
        # Convert amount to cents (EzBookkeeping uses integer cents)
        amount_cents = int(amount * 100)
        
        data = {
            "amount": amount_cents,
            "description": description,
            "sourceAccountId": account_id,
            "categoryId": category_id,
            "type": transaction_type,
        }
        
        if time:
            data["time"] = time
        
        if tags:
            data["tagIds"] = tags
        
        result = client.post("/transactions/add.json", data)
        return {
            "success": True,
            "transaction_id": result.get("id"),
            "message": f"Transaction added: {description} - ${amount}",
            "details": result
        }


def get_transactions(
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    account_id: Optional[str] = None,
    category_id: Optional[str] = None,
    max_count: int = 50
) -> dict:
    """
    Get list of transactions with optional filters.
    
    Args:
        start_time: Start time (Unix timestamp in milliseconds)
        end_time: End time (Unix timestamp in milliseconds)
        account_id: Filter by account ID
        category_id: Filter by category ID
        max_count: Maximum number of transactions to return (default: 50)
        
    Returns:
        Dictionary with transactions list
    """
    with EzBookkeepingClient() as client:
        params = {"count": max_count}
        
        if start_time:
            params["minTime"] = start_time
        if end_time:
            params["maxTime"] = end_time
        if account_id:
            params["accountId"] = account_id
        if category_id:
            params["categoryId"] = category_id
        
        result = client.get("/transactions/list.json", params=params)
        
        # Convert amounts from cents to dollars for readability
        if "items" in result:
            for transaction in result["items"]:
                if "amount" in transaction:
                    transaction["amount_dollars"] = transaction["amount"] / 100
        
        return {
            "success": True,
            "count": len(result.get("items", [])),
            "transactions": result.get("items", [])
        }
