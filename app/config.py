from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration read from environment variables (or a local .env file)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str = ""
    openai_api_key: str = ""
    llm_model: str = "claude-haiku-5-5"
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536  # must match embedding_model
    database_url: str = "postgresql://app:app@localhost:5432/permissibility"


settings = Settings()
