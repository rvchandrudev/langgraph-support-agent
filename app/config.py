from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    groq_api_key: str = ""

    llm_model:str = "llama-3.1-8b-instant"

    top_k:int = 4

settings = Settings()