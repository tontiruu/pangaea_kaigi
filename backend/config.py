from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, Field
from typing import Union


class Settings(BaseSettings):
    # App Settings
    app_name: str = "Pangaea Kaigi API"
    api_version: str = "0.1.0"
    debug: bool = True

    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS Settings - 文字列またはリストとして受け取る
    cors_origins: Union[str, list[str]] = Field(
        default="http://localhost:3000,http://127.0.0.1:3000"
    )

    # OpenAI Settings
    openai_api_key: str = ""

    # Dedalus Labs Settings
    dedalus_api_key: str = ""

    # MCP Integration Settings
    enable_context_retrieval: bool = True

    # Notion MCP Settings (オプション)
    notion_token: str = ""

    # Slack MCP Settings (オプション)
    slack_bot_token: str = ""
    slack_team_id: str = ""

    # Atlassian MCP Settings (オプション)
    atlassian_email: str = ""
    atlassian_api_token: str = ""
    atlassian_domain: str = ""

    # Database (必要に応じて設定)
    database_url: str = ""

    # Security (必要に応じて設定)
    secret_key: str = ""
    jwt_secret: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @field_validator("cors_origins", mode="after")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v


settings = Settings()
