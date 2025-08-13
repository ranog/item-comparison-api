from functools import lru_cache
from pathlib import Path

from fastapi import Depends

from src.adapters.repository import JsonItemRepository, ItemRepository
from src.service_layer.services import DefaultItemService, ItemService


@lru_cache()
def get_repository() -> ItemRepository:
    """
    Retorna uma instância única do repositório.
    """
    return JsonItemRepository(Path("data/items.json"))


def get_item_service(
    repository: ItemRepository = Depends(get_repository),
) -> ItemService:
    """
    Retorna uma instância do serviço de itens.
    """
    return DefaultItemService(repository)
