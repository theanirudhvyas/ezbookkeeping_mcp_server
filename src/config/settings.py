"""Configuration management for EzBookkeeping MCP Server."""
import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseModel):
    """Application settings loaded from environment variables."""
    
    # Required settings
    ezbookkeeping_url: str = Field(
        default_factory=lambda: os.getenv("EZBOOKKEEPING_URL", ""),
        description="EzBookkeeping instance URL"
    )
    ezbookkeeping_token: str = Field(
        default_factory=lambda: os.getenv("EZBOOKKEEPING_TOKEN", ""),
        description="API token for authentication"
    )
    
    # Optional settings
    timezone_offset: int = Field(
        default_factory=lambda: int(os.getenv("EZBOOKKEEPING_TIMEZONE_OFFSET", "0")),
        description="Timezone offset in minutes"
    )
    default_currency: str = Field(
        default_factory=lambda: os.getenv("EZBOOKKEEPING_DEFAULT_CURRENCY", "USD"),
        description="Default currency code (ISO 4217)"
    )
    
    def validate_required(self) -> None:
        """Validate that required settings are present."""
        if not self.ezbookkeeping_url:
            raise ValueError(
                "EZBOOKKEEPING_URL is required. Set it in .env or environment variables."
            )
        if not self.ezbookkeeping_token:
            raise ValueError(
                "EZBOOKKEEPING_TOKEN is required. Set it in .env or environment variables."
            )


# Global settings instance
settings = Settings()
