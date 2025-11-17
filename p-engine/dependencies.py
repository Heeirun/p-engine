"""Shared dependencies and dependency injection for the application."""

from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

from .config import settings


class DependencyContainer:
    """Container for shared application dependencies."""

    _elasticsearch: Elasticsearch | None = None
    _embedding_model: SentenceTransformer | None = None

    @classmethod
    def get_elasticsearch(cls) -> Elasticsearch:
        """Get or create Elasticsearch client instance."""
        if cls._elasticsearch is None:
            cls._elasticsearch = Elasticsearch(
                settings.elasticsearch_url,
                basic_auth=[
                    settings.elasticsearch_user,
                    settings.elasticsearch_password,
                ],
            )
        return cls._elasticsearch

    @classmethod
    def get_embedding_model(cls) -> SentenceTransformer:
        """Get or create SentenceTransformer model instance."""
        if cls._embedding_model is None:
            cls._embedding_model = SentenceTransformer(settings.embedding_model_name)
        return cls._embedding_model

    @classmethod
    def close(cls):
        """Close all connections and cleanup resources."""
        if cls._elasticsearch is not None:
            cls._elasticsearch.close()
            cls._elasticsearch = None
        cls._embedding_model = None


# Dependency functions for FastAPI
def get_elasticsearch() -> Elasticsearch:
    """FastAPI dependency for Elasticsearch client."""
    return DependencyContainer.get_elasticsearch()


def get_embedding_model() -> SentenceTransformer:
    """FastAPI dependency for embedding model."""
    return DependencyContainer.get_embedding_model()
