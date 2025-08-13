import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from tempfile import mkstemp
from typing import Any, Dict, List, Optional, Protocol

from src.domain.item import Item, ItemCreate, ItemUpdate


class ItemRepository(Protocol):
    """Define o contrato para repositórios de itens."""

    def list_items(self, ids: Optional[List[int]] = None) -> List[Item]:
        """Lista todos os itens ou filtra por IDs específicos."""
        ...

    def get_item(self, item_id: int) -> Optional[Item]:
        """Recupera um item pelo ID."""
        ...

    def create_item(self, payload: ItemCreate) -> Item:
        """Cria um novo item."""
        ...

    def replace_item(self, item_id: int, payload: ItemCreate) -> Optional[Item]:
        """Substitui um item existente."""
        ...

    def update_item(self, item_id: int, payload: ItemUpdate) -> Optional[Item]:
        """Atualiza parcialmente um item existente."""
        ...

    def delete_item(self, item_id: int) -> bool:
        """Remove um item pelo ID."""
        ...


class BaseFileRepository(ABC):
    """Implementação base para repositórios baseados em arquivo."""

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def _ensure_file(self) -> None:
        """Garante que o arquivo de dados existe."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write_all([])

    def _read_all(self) -> List[Dict[str, Any]]:
        """Lê todos os dados do arquivo."""
        self._ensure_file()
        with open(self.file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
        return data if isinstance(data, list) else []

    def _write_all(self, items: List[Dict[str, Any]]) -> None:
        """Escreve dados no arquivo de forma segura usando arquivo temporário."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = mkstemp(
            dir=str(self.file_path.parent),
            prefix="items_",
            suffix=".tmp",
        )
        try:
            # Converte objetos complexos para seu formato serializável
            serializable_items = []
            for item in items:
                if "image_url" in item and hasattr(item["image_url"], "__str__"):
                    item = dict(item)  # Cria uma cópia para não modificar o original
                    item["image_url"] = str(item["image_url"])
                serializable_items.append(item)

            with os.fdopen(fd, "w", encoding="utf-8") as tmp:
                json.dump(serializable_items, tmp, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.file_path)
        except Exception:
            os.unlink(tmp_path)
            raise

    @abstractmethod
    def _next_id(self, items: List[Dict[str, Any]]) -> int:
        """Gera o próximo ID disponível."""
        ...


class JsonItemRepository(BaseFileRepository, ItemRepository):
    """Implementação do repositório de itens usando arquivo JSON."""

    def __init__(self, file_path: Optional[Path] = None):
        """Inicializa o repositório com o caminho do arquivo."""
        super().__init__(
            file_path or Path(os.getenv("DATA_FILE", "data/items.json")),
        )

    def _next_id(self, items: List[Dict[str, Any]]) -> int:
        """Gera o próximo ID disponível."""
        return max((it.get("id", 0) for it in items), default=0) + 1

    def list_items(self, ids: Optional[List[int]] = None) -> List[Item]:
        """Lista todos os itens ou filtra por IDs específicos."""
        raw = self._read_all()
        if ids:
            raw = [it for it in raw if it.get("id") in ids]
        return [Item(**it) for it in raw]

    def get_item(self, item_id: int) -> Optional[Item]:
        """Recupera um item pelo ID."""
        for it in self._read_all():
            if it.get("id") == item_id:
                return Item(**it)
        return None

    def create_item(self, payload: ItemCreate) -> Item:
        """Cria um novo item."""
        items = self._read_all()
        # Converte para dict e força a conversão de HttpUrl para str
        new = payload.model_dump(exclude_none=True)
        new["id"] = self._next_id(items)
        item = Item(**new)
        items.append(item.model_dump(exclude_none=True))
        self._write_all(items)
        return item

    def replace_item(self, item_id: int, payload: ItemCreate) -> Optional[Item]:
        """Substitui um item existente."""
        items = self._read_all()
        for idx, it in enumerate(items):
            if it.get("id") == item_id:
                updated = payload.model_dump(exclude_none=True)
                updated["id"] = item_id
                item = Item(**updated)
                items[idx] = item.model_dump(exclude_none=True)
                self._write_all(items)
                return item
        return None

    def update_item(self, item_id: int, payload: ItemUpdate) -> Optional[Item]:
        """Atualiza parcialmente um item existente."""
        items = self._read_all()
        for idx, it in enumerate(items):
            if it.get("id") == item_id:
                merged = {
                    **it,
                    **payload.model_dump(exclude_unset=True, exclude_none=True),
                }
                item = Item(**merged)
                items[idx] = item.model_dump(exclude_none=True)
                self._write_all(items)
                return item
        return None

    def delete_item(self, item_id: int) -> bool:
        """Remove um item pelo ID."""
        items = self._read_all()
        new_items = [it for it in items if it.get("id") != item_id]
        if len(new_items) == len(items):
            return False
        self._write_all(new_items)
        return True
