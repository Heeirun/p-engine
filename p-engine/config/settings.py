"""Application settings and configuration."""

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "P-Engine"
    debug: bool = False

    # CORS
    cors_origins: List[str] = ["http://localhost:5173"]

    # Elasticsearch
    elasticsearch_url: str = "http://localhost:9200"
    elasticsearch_user: str = "elastic"
    elasticsearch_password: str = "b1V4R0Re"
    elasticsearch_index: str = "audit_logs"

    # Embedding Model
    embedding_model_name: str = "all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    # Search
    default_search_type: str = "keyword"
    knn_k: int = 10
    knn_num_candidates: int = 100

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra fields in .env file


settings = Settings()
