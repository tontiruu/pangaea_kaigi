from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App Settings
    app_name: str = "Pangaea Kaigi API"
    api_version: str = "0.1.0"
    debug: bool = True

    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS Settings
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Database (必要に応じて設定)
    # database_url: str = ""

    # Security (必要に応じて設定)
    # secret_key: str = ""
    # jwt_secret: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # CORS_ORIGINSをカンマ区切りの文字列として読み込む
        @staticmethod
        def parse_env_var(field_name: str, raw_val: str):
            if field_name == "cors_origins":
                return [origin.strip() for origin in raw_val.split(",")]
            return raw_val


settings = Settings()
