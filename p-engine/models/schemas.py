"""Pydantic schemas for request/response validation."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class Item(BaseModel):
    """Item schema for basic CRUD operations."""

    name: str = Field(..., description="The item's name.", min_length=1)
    price: float = Field(..., description="The item's price.", gt=0)
    is_offer: Optional[bool] = Field(None, description="Whether the item is on offer.")

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: float) -> float:
        """Validate price is positive."""
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v


class VectorRequest(BaseModel):
    """Request schema for vector embedding generation."""

    text: str = Field(..., description="Text to generate embedding for", min_length=1)

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Validate text is not empty after stripping."""
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()


class VectorResponse(BaseModel):
    """Response schema for vector embedding."""

    text: str = Field(..., description="Original input text")
    vector: List[float] = Field(..., description="384-dimension embedding vector")

    class Config:
        json_schema_extra = {
            "example": {"text": "sample text", "vector": [0.1, 0.2, 0.3, "..."]}
        }


class SearchRequest(BaseModel):
    """Request schema for search operations."""

    query: str = Field(default="", description="Search query text")
    search_type: Literal["keyword", "semantic", "hybrid"] = Field(
        default="keyword", description="Type of search to perform"
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Trim whitespace from query."""
        return v.strip()


class AuditLog(BaseModel):
    """Schema for audit log document."""

    summary: str = Field(..., description="Summary of the audit log")
    description: str = Field(..., description="Detailed description")
    embedding_vector: Optional[List[float]] = Field(
        None, description="Vector embedding of the log"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "summary": "User login",
                "description": "User john@example.com logged in successfully",
                "embedding_vector": [0.1, 0.2, "..."],
            }
        }


class SearchResponse(BaseModel):
    """Response schema for search results."""

    results: List[AuditLog] = Field(..., description="List of matching audit logs")
    total: int = Field(..., description="Total number of results")

    class Config:
        json_schema_extra = {
            "example": {
                "results": [{"summary": "User login", "description": "User logged in"}],
                "total": 1,
            }
        }
