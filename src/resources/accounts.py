"""Account resources for EzBookkeeping."""
from src.utils.http_client import EzBookkeepingClient


def get_accounts() -> dict:
    """
    Get all accounts from EzBookkeeping.
    
    Returns:
        Dictionary with accounts list
    """
    with EzBookkeepingClient() as client:
        result = client.get("/accounts/list.json")
        
        # Convert balances from cents to dollars for readability
        if isinstance(result, list):
            for account in result:
                if "balance" in account:
                    account["balance_dollars"] = account["balance"] / 100
                # Process sub-accounts
                if "subAccounts" in account:
                    for sub in account["subAccounts"]:
                        if "balance" in sub:
                            sub["balance_dollars"] = sub["balance"] / 100
        
        return {
            "success": True,
            "count": len(result) if isinstance(result, list) else 0,
            "accounts": result
        }


def get_account_by_id(account_id: str) -> dict:
    """
    Get specific account details by ID.
    
    Args:
        account_id: Account ID
        
    Returns:
        Dictionary with account details
    """
    with EzBookkeepingClient() as client:
        # Get all accounts and find the one we want
        all_accounts = client.get("/accounts/list.json")
        
        def find_account(accounts, target_id):
            for account in accounts:
                if account.get("id") == target_id:
                    if "balance" in account:
                        account["balance_dollars"] = account["balance"] / 100
                    return account
                # Check sub-accounts
                if "subAccounts" in account:
                    sub_account = find_account(account["subAccounts"], target_id)
                    if sub_account:
                        return sub_account
            return None
        
        account = find_account(all_accounts if isinstance(all_accounts, list) else [], account_id)
        
        if not account:
            raise Exception(f"Account not found: {account_id}")
        
        return {
            "success": True,
            "account": account
        }
