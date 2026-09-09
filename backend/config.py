"""
Backend configuration -- loaded and validated via pydantic-settings.
"""

from typing import List, Optional, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded and validated from environment variables."""

    ML_SERVICE_URL: str = Field(
        default="http://localhost:8001",
        description="Base URL for the ML inference service",
    )
    ML_REQUEST_TIMEOUT: float = Field(
        default=10.0,
        description="Timeout in seconds for requests to the ML service",
    )
    DATABASE_URL: str = Field(
        default="sqlite:///./predictions.db",
        description="Database connection URL",
    )
    ALLOWED_ORIGINS: Union[List[str], str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins",
    )
    MODEL_VERSION: Optional[str] = Field(
        default=None,
        description="Default model version",
    )
    API_VERSION: str = Field(
        default="v1",
        description="API version tag",
    )
    DEBUG: bool = Field(
        default=False,
        description="Enable debug mode",
    )
    ENVIRONMENT: str = Field(
        default="development",
        description="Runtime environment: development | production | test",
    )
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level",
    )
    LOG_FORMAT: str = Field(
        default="human",
        description="Logging format: human | json",
    )

    # Authentication
    API_KEY: str = Field(
        default="dev-secret-key-123",
        description="API key required for protected endpoints",
    )

    # ML Resilience (Retry)
    ML_MAX_RETRIES: int = Field(
        default=3,
        description="Maximum number of retries for transient ML service errors",
    )
    ML_RETRY_BASE_DELAY: float = Field(
        default=0.1,
        description="Base delay in seconds for exponential backoff",
    )
    ML_RETRY_MAX_DELAY: float = Field(
        default=2.0,
        description="Maximum delay in seconds for exponential backoff",
    )

    # ML Resilience (Circuit Breaker)
    ML_CIRCUIT_FAILURE_THRESHOLD: int = Field(
        default=5,
        description="Number of consecutive failures to trip the circuit breaker OPEN",
    )
    ML_CIRCUIT_COOLDOWN_SECONDS: float = Field(
        default=30.0,
        description="Cooldown period in seconds before trying HALF_OPEN state",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("ML_SERVICE_URL")
    @classmethod
    def validate_ml_url(cls, v: str) -> str:
        v = v.strip()
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("ML_SERVICE_URL must start with http:// or https://")
        return v.rstrip("/")

    @field_validator("ML_REQUEST_TIMEOUT")
    @classmethod
    def validate_ml_timeout(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("ML_REQUEST_TIMEOUT must be greater than 0")
        return v

    @field_validator("ML_RETRY_BASE_DELAY", "ML_RETRY_MAX_DELAY", "ML_CIRCUIT_COOLDOWN_SECONDS")
    @classmethod
    def validate_positive_float(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Delay values must be greater than 0")
        return v

    @field_validator("ML_MAX_RETRIES", "ML_CIRCUIT_FAILURE_THRESHOLD")
    @classmethod
    def validate_positive_int(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Retry count and failure threshold must be greater than 0")
        return v

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if not v.strip():
                return ["http://localhost:3000", "http://localhost:5173"]
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        if isinstance(v, list):
            return [str(origin).strip() for origin in v if str(origin).strip()]
        return ["http://localhost:3000", "http://localhost:5173"]


settings = Settings()
