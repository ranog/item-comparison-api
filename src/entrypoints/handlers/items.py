from typing import List, Optional

from fastapi import Depends, HTTPException, Query, status

from src.config.dependencies import get_item_service
from src.domain.item import ItemCreate, ItemUpdate
from src.service_layer.services import ItemService


def list_items(
    ids: Optional[List[int]] = Query(None, description="IDs dos itens a comparar"),
    service: ItemService = Depends(get_item_service),
):
    items = service.list_items(ids=ids)
    return [item.model_dump() for item in items]


def get_item(
    item_id: int,
    service: ItemService = Depends(get_item_service),
):
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} não encontrado",
        )
    return item.model_dump()


def create_item(
    payload: ItemCreate,
    service: ItemService = Depends(get_item_service),
):
    item = service.create_item(payload)
    return item.model_dump()


def replace_item(
    item_id: int,
    payload: ItemCreate,
    service: ItemService = Depends(get_item_service),
):
    item = service.replace_item(item_id, payload)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} não encontrado",
        )
    return item.model_dump()


def update_item(
    item_id: int,
    payload: ItemUpdate,
    service: ItemService = Depends(get_item_service),
):
    item = service.update_item(item_id, payload)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} não encontrado",
        )
    return item.model_dump()


def delete_item(
    item_id: int,
    service: ItemService = Depends(get_item_service),
):
    if not service.delete_item(item_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} não encontrado",
        )
    return None
