"""Controller for search and embedding endpoints."""

from typing import List, Dict, Any, Literal
from fastapi import APIRouter, Depends, HTTPException, status, Query
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

from ..models import VectorResponse
from ..dependencies import get_elasticsearch, get_embedding_model
from ..services import EmbeddingService, SearchService

router = APIRouter(tags=["search"])


def get_embedding_service(
    model: SentenceTransformer = Depends(get_embedding_model)
) -> EmbeddingService:
    """
    Get embedding service instance.

    Args:
        model: SentenceTransformer model from dependencies

    Returns:
        EmbeddingService instance
    """
    return EmbeddingService(model)


def get_search_service(
    es_client: Elasticsearch = Depends(get_elasticsearch),
    embedding_service: EmbeddingService = Depends(get_embedding_service)
) -> SearchService:
    """
    Get search service instance.

    Args:
        es_client: Elasticsearch client from dependencies
        embedding_service: Embedding service from dependencies

    Returns:
        SearchService instance
    """
    return SearchService(es_client, embedding_service)


@router.get("/get_vector/", response_model=VectorResponse, status_code=status.HTTP_200_OK)
def get_vector(
    text: str = Query(..., min_length=1, description="Text to generate embedding for"),
    embedding_service: EmbeddingService = Depends(get_embedding_service)
):
    """
    Generate a 384-dimension vector embedding for the given text.

    Args:
        text: Input text to generate embedding for
        embedding_service: Service for generating embeddings

    Returns:
        VectorResponse with text and embedding vector

    Raises:
        HTTPException: If text is empty or invalid
    """
    try:
        embedding = embedding_service.generate_embedding(text)
        return VectorResponse(text=text, vector=embedding)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/search", status_code=status.HTTP_200_OK)
def search_logs(
    query: str = Query(default="", description="Search query text"),
    search_type: Literal["keyword", "semantic", "hybrid"] = Query(
        default="keyword",
        description="Type of search to perform"
    ),
    search_service: SearchService = Depends(get_search_service)
) -> List[Dict[str, Any]]:
    """
    Search audit logs in Elasticsearch.

    Args:
        query: Search query text
        search_type: Type of search ('keyword', 'semantic', or 'hybrid')
        search_service: Service for performing searches

    Returns:
        List of matching audit log documents

    Raises:
        HTTPException: If search type is invalid or search fails
    """
    try:
        results = search_service.search(query=query, search_type=search_type)
        return results
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )
