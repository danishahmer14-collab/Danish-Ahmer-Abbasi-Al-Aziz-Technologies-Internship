from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_api_key: str = ""
    llm_base_url: str = "https://api.x.ai/v1"
    llm_model: str = "grok-4"
    embedding_model: str = "all-MiniLM-L6-v2"
    chroma_dir: str = "./chroma_db"
    chunk_size: int = 800
    chunk_overlap: int = 120
    top_k: int = 4
    min_score: float = 0.15


def get_settings() -> Settings:
    return Settings()