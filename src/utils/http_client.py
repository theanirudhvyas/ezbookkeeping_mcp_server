"""HTTP client for EzBookkeeping API."""
import httpx
from typing import Any, Optional
from src.config.settings import settings


class EzBookkeepingClient:
    """HTTP client for interacting with EzBookkeeping API."""
    
    def __init__(self):
        """Initialize the client with settings."""
        settings.validate_required()
        
        self.base_url = settings.ezbookkeeping_url.rstrip('/')
        self.token = settings.ezbookkeeping_token
        self.timezone_offset = settings.timezone_offset
        
        # Create httpx client
        self.client = httpx.Client(
            base_url=f"{self.base_url}/api/v1",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "X-Timezone-Offset": str(self.timezone_offset)
            },
            timeout=30.0
        )
    
    def get(self, path: str, params: Optional[dict] = None) -> dict[str, Any]:
        """
        Make GET request to EzBookkeeping API.
        
        Args:
            path: API endpoint path (without /api/v1 prefix)
            params: Optional query parameters
            
        Returns:
            Response data from API
            
        Raises:
            Exception: If request fails or API returns error
        """
        response = self.client.get(path, params=params)
        return self._handle_response(response)
    
    def post(self, path: str, data: Optional[dict] = None) -> dict[str, Any]:
        """
        Make POST request to EzBookkeeping API.
        
        Args:
            path: API endpoint path (without /api/v1 prefix)
            data: Request body data
            
        Returns:
            Response data from API
            
        Raises:
            Exception: If request fails or API returns error
        """
        response = self.client.post(path, json=data)
        return self._handle_response(response)
    
    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """
        Handle API response and extract data.
        
        Args:
            response: HTTP response object
            
        Returns:
            Response data from API
            
        Raises:
            Exception: If API returns error
        """
        try:
            data = response.json()
        except Exception:
            response.raise_for_status()
            raise Exception(f"Invalid JSON response: {response.text}")
        
        # Check for API-level errors
        if not data.get("success", False):
            error_msg = data.get("errorMessage", "Unknown error")
            error_code = data.get("errorCode", "N/A")
            raise Exception(f"API Error {error_code}: {error_msg}")
        
        return data.get("result", {})
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
