"""Controller for item-related endpoints."""

from typing import Optional

from fastapi import APIRouter, status

from ..models import Item

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{item_id}", status_code=status.HTTP_200_OK)
def read_item(item_id: int, q: Optional[str] = None):
    """
    Read an item by ID.

    Args:
        item_id: The ID of the item to retrieve
        q: Optional query parameter

    Returns:
        Dictionary with item_id and optional query parameter
    """
    return {"item_id": item_id, "q": q}


@router.put("/{item_id}", status_code=status.HTTP_200_OK)
def update_item(item_id: int, item: Item):
    """
    Update an item by ID.

    Args:
        item_id: The ID of the item to update
        item: Item data to update

    Returns:
        Dictionary with updated item information
    """
    return {
        "item_name": item.name,
        "item_id": item_id,
        "price": item.price,
        "is_offer": item.is_offer,
    }
