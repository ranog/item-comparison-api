from typing import List, Optional, Protocol

from src.adapters.repository import ItemRepository
from src.domain.model import Item, ItemCreate, ItemUpdate


class ItemService(Protocol):
    """Define o contrato para serviços de itens."""

    def list_items(self, ids: Optional[List[int]] = None) -> List[Item]:
        """Lista itens ordenados, opcionalmente filtrados por IDs únicos."""
        ...

    def get_item(self, item_id: int) -> Optional[Item]:
        """Recupera um item específico."""
        ...

    def create_item(self, payload: ItemCreate) -> Item:
        """Cria um novo item com especificações normalizadas."""
        ...

    def replace_item(self, item_id: int, payload: ItemCreate) -> Optional[Item]:
        """Substitui um item existente com especificações normalizadas."""
        ...

    def update_item(self, item_id: int, payload: ItemUpdate) -> Optional[Item]:
        """Atualiza parcialmente um item com especificações normalizadas."""
        ...

    def delete_item(self, item_id: int) -> bool:
        """Remove um item."""
        ...


class DefaultItemService:
    """Implementação padrão do serviço de itens."""

    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def list_items(self, ids: Optional[List[int]] = None) -> List[Item]:
        """
        Lista itens ordenados para comparação.

        Regras de negócio:
        - Remove duplicatas dos IDs fornecidos
        - Ordena itens por ID para visualização consistente
        """
        if ids:
            # Remove duplicatas mantendo a ordem
            ids = list(dict.fromkeys(ids))

        items = self.repository.list_items(ids=ids)
        return sorted(items, key=lambda x: x.id)

    def get_item(self, item_id: int) -> Optional[Item]:
        """Recupera um item específico."""
        return self.repository.get_item(item_id)

    def create_item(self, payload: ItemCreate) -> Item:
        """
        Cria um novo item com especificações normalizadas.

        Regras de negócio:
        - Normaliza especificações para consistência
        """
        if payload.specifications:
            payload.specifications = {
                k.lower(): str(v).strip() for k, v in payload.specifications.items()
            }

        return self.repository.create_item(payload)

    def replace_item(self, item_id: int, payload: ItemCreate) -> Optional[Item]:
        """
        Substitui um item existente.

        Regras de negócio:
        - Verifica existência do item
        - Normaliza especificações
        """
        existing = self.repository.get_item(item_id)
        if not existing:
            return None

        if payload.specifications:
            payload.specifications = {
                k.lower(): str(v).strip() for k, v in payload.specifications.items()
            }

        return self.repository.replace_item(item_id, payload)

    def update_item(self, item_id: int, payload: ItemUpdate) -> Optional[Item]:
        """
        Atualiza parcialmente um item.

        Regras de negócio:
        - Verifica existência do item
        - Normaliza especificações
        """
        existing = self.repository.get_item(item_id)
        if not existing:
            return None

        if payload.specifications:
            payload.specifications = {
                k.lower(): str(v).strip() for k, v in payload.specifications.items()
            }

        return self.repository.update_item(item_id, payload)

    def delete_item(self, item_id: int) -> bool:
        """Remove um item."""
        return self.repository.delete_item(item_id)
