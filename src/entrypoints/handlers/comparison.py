from typing import Any, Dict, List

from fastapi import Depends, HTTPException, Query

from src.domain.comparison import ItemComparison
from src.service_layer.services import ItemService
from src.config.dependencies import get_item_service



def compare_items(
    item_ids: List[int] = Query(
        ...,
        title="IDs dos itens",
        description="Lista de IDs dos itens a serem comparados",
        min_items=2,
        max_items=5,
    ),
    service: ItemService = Depends(get_item_service),
) -> Dict[str, Any]:
    """
    Compara itens especificados pelos IDs.

    Args:
        item_ids: Lista de IDs dos itens a serem comparados (mín: 2, máx: 5)
        service: Serviço de itens injetado

    Returns:
        Dicionário contendo a comparação detalhada dos itens

    Raises:
        HTTPException: Se algum item não for encontrado ou se houver IDs duplicados
    """
    # Remove duplicatas mantendo a ordem
    unique_ids = list(dict.fromkeys(item_ids))
    if len(unique_ids) != len(item_ids):
        raise HTTPException(
            status_code=400,
            detail="IDs duplicados não são permitidos na comparação",
        )

    # Busca todos os itens
    items = service.list_items(ids=unique_ids)

    # Verifica se todos os itens foram encontrados
    found_ids = {item.id for item in items}
    missing_ids = set(unique_ids) - found_ids
    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Itens não encontrados: {missing_ids}",
        )

    # Realiza a comparação
    return ItemComparison.compare_items(items)
