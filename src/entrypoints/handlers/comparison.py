from typing import Any, Dict, List

from fastapi import Depends, HTTPException, Query

from src.config.dependencies import get_item_service
from src.domain.comparison import ItemComparison
from src.service_layer.services import ItemService


def compare_items(
    ids: List[int] = Query(
        ...,
        title="IDs dos itens",
        description="Lista de IDs dos itens a serem comparados",
        min_length=2,
        max_length=5,
    ),
    service: ItemService = Depends(get_item_service),
) -> Dict[str, Any]:
    """
    Compara itens especificados pelos IDs.

    Args:
        params: Parâmetros da comparação contendo os IDs dos itens
        service: Serviço de itens injetado

    Returns:
        Dicionário contendo a comparação detalhada dos itens

    Raises:
        HTTPException: Se algum item não for encontrado ou se houver IDs duplicados
    """
    # Remove duplicatas mantendo a ordem
    unique_ids = list(dict.fromkeys(ids))
    if len(unique_ids) != len(ids):
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
