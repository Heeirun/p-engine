"""Service for handling vector embeddings."""

from typing import List
from sentence_transformers import SentenceTransformer

from ..config import settings


class EmbeddingService:
    """Service for generating and managing vector embeddings."""

    def __init__(self, model: SentenceTransformer):
        """
        Initialize the embedding service.

        Args:
            model: SentenceTransformer model instance
        """
        self.model = model
        self.dimension = settings.embedding_dimension

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate a vector embedding for the given text.

        Args:
            text: Input text to encode

        Returns:
            List of floats representing the embedding vector

        Raises:
            ValueError: If text is empty
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        text = text.strip()
        embedding = self.model.encode(text)
        return embedding.tolist()

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.

        Args:
            texts: List of input texts

        Returns:
            List of embedding vectors

        Raises:
            ValueError: If texts list is empty
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")

        # Strip whitespace from all texts
        cleaned_texts = [t.strip() for t in texts if t.strip()]

        if not cleaned_texts:
            raise ValueError("All texts are empty after stripping whitespace")

        embeddings = self.model.encode(cleaned_texts)
        return [emb.tolist() for emb in embeddings]

    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embedding vectors.

        Returns:
            Integer representing the embedding dimension
        """
        return self.dimension
