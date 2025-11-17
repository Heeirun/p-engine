"""Service for handling search operations."""

from typing import Any, Dict, List

from elasticsearch import Elasticsearch

from ..config import settings
from .embedding_service import EmbeddingService


class SearchService:
    """Service for searching audit logs in Elasticsearch."""

    def __init__(self, es_client: Elasticsearch, embedding_service: EmbeddingService):
        """
        Initialize the search service.

        Args:
            es_client: Elasticsearch client instance
            embedding_service: Service for generating embeddings
        """
        self.es = es_client
        self.embedding_service = embedding_service
        self.index_name = settings.elasticsearch_index

    def search(
        self, query: str = "", search_type: str = "keyword"
    ) -> List[Dict[str, Any]]:
        """
        Search audit logs using the specified search type.

        Args:
            query: Search query text
            search_type: Type of search ('keyword', 'semantic', or 'hybrid')

        Returns:
            List of matching documents

        Raises:
            ValueError: If search_type is invalid
        """
        if search_type == "keyword":
            return self._keyword_search(query)
        elif search_type == "semantic":
            return self._semantic_search(query)
        elif search_type == "hybrid":
            return self._hybrid_search(query)
        else:
            raise ValueError(
                f"Invalid search_type: {search_type}. "
                "Must be 'keyword', 'semantic', or 'hybrid'"
            )

    def _keyword_search(self, query: str) -> List[Dict[str, Any]]:
        """
        Perform keyword-based search.

        Args:
            query: Search query text

        Returns:
            List of matching documents
        """
        if not query:
            # Return all logs if query is empty
            es_query = {"query": {"match_all": {}}}
        else:
            es_query = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["summary", "description"],
                    }
                }
            }

        return self._execute_search(es_query)

    def _semantic_search(self, query: str) -> List[Dict[str, Any]]:
        """
        Perform semantic (vector-based) search.

        Args:
            query: Search query text

        Returns:
            List of matching documents

        Raises:
            ValueError: If query is empty
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty for semantic search")

        query_vector = self.embedding_service.generate_embedding(query)

        es_query = {
            "knn": {
                "field": "embedding_vector",
                "query_vector": query_vector,
                "k": settings.knn_k,
                "num_candidates": settings.knn_num_candidates,
            }
        }

        return self._execute_search(es_query)

    def _hybrid_search(self, query: str) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining keyword and semantic search.

        Args:
            query: Search query text

        Returns:
            List of matching documents

        Raises:
            ValueError: If query is empty
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty for hybrid search")

        query_vector = self.embedding_service.generate_embedding(query)

        es_query = {
            "query": {
                "multi_match": {"query": query, "fields": ["summary", "description"]}
            },
            "knn": {
                "field": "embedding_vector",
                "query_vector": query_vector,
                "k": settings.knn_k,
                "num_candidates": settings.knn_num_candidates,
            },
            "rank": {"rrf": {}},
        }

        return self._execute_search(es_query)

    def _execute_search(self, es_query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute the Elasticsearch query.

        Args:
            es_query: Elasticsearch query dictionary

        Returns:
            List of document sources from search results
        """
        response = self.es.search(index=self.index_name, body=es_query)
        hits = [hit["_source"] for hit in response["hits"]["hits"]]
        return hits

    def get_all_logs(self, size: int = 100) -> List[Dict[str, Any]]:
        """
        Get all audit logs.

        Args:
            size: Maximum number of logs to return

        Returns:
            List of all audit log documents
        """
        es_query = {"query": {"match_all": {}}, "size": size}
        return self._execute_search(es_query)
