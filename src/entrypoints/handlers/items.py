from typing import List, Optional

from fastapi import HTTPException, Query, status

from src.adapters.repository import JsonItemRepository
from src.domain.model import ItemCreate, ItemUpdate
from src.service_layer.services import DefaultItemService

repository = JsonItemRepository()
service = DefaultItemService(repository)


def list_items(
    ids: Optional[List[int]] = Query(None, description="IDs dos itens a comparar"),
):
    items = service.list_items(ids=ids)
    return [item.model_dump() for item in items]


def get_item(item_id: int):
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} não encontrado",
        )
    return item.model_dump()


def create_item(payload: ItemCreate):
    item = service.create_item(payload)
    return item.model_dump()


def replace_item(item_id: int, payload: ItemCreate):
    item = service.replace_item(item_id, payload)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} não encontrado",
        )
    return item.model_dump()


def update_item(item_id: int, payload: ItemUpdate):
    item = service.update_item(item_id, payload)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} não encontrado",
        )
    return item.model_dump()


def delete_item(item_id: int):
    if not service.delete_item(item_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} não encontrado",
        )
    return None
