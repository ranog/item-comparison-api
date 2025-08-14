from typing import Dict, List

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def sample_items() -> List[Dict]:
    """Cria uma lista de itens para comparação."""
    return [
        {
            "name": "Produto A",
            "image_url": "http://example.com/imageA.jpg",
            "description": "Descrição do Produto A",
            "price": 100.0,
            "rating": 4.5,
            "specifications": {"cor": "azul", "tamanho": "M", "peso": "1kg"},
        },
        {
            "name": "Produto B",
            "image_url": "http://example.com/imageB.jpg",
            "description": "Descrição do Produto B",
            "price": 150.0,
            "rating": 4.8,
            "specifications": {"cor": "verde", "tamanho": "G", "peso": "1.2kg"},
        },
        {
            "name": "Produto C",
            "image_url": "http://example.com/imageC.jpg",
            "description": "Descrição do Produto C",
            "price": 80.0,
            "rating": 4.0,
            "specifications": {"cor": "vermelho", "tamanho": "P", "peso": "0.8kg"},
        },
    ]


def test_should_compare_items_successfully(
    test_client: TestClient,
    sample_items: List[Dict],
):
    created_items = []
    for item in sample_items[:2]:
        response = test_client.post("/items", json=item)
        assert response.status_code == 201
        created_items.append(response.json())

    items = [item["id"] for item in created_items]
    response = test_client.get("/items/compare", params={"ids": items})

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "description": "Descrição do Produto A",
                "id": 1,
                "image_url": "http://example.com/imageA.jpg",
                "name": "Produto A",
                "price": 100.0,
                "rating": 4.5,
                "specifications": {
                    "cor": "azul",
                    "peso": "1kg",
                    "tamanho": "M",
                },
            },
            {
                "description": "Descrição do Produto B",
                "id": 2,
                "image_url": "http://example.com/imageB.jpg",
                "name": "Produto B",
                "price": 150.0,
                "rating": 4.8,
                "specifications": {
                    "cor": "verde",
                    "peso": "1.2kg",
                    "tamanho": "G",
                },
            },
        ],
        "price_analysis": {
            "difference": 50.0,
            "highest": 150.0,
            "lowest": 100.0,
        },
        "rating_analysis": {
            "average": 4.65,
            "highest": 4.8,
            "lowest": 4.5,
        },
        "specifications_comparison": {
            "cor": {
                "Produto A": "azul",
                "Produto B": "verde",
            },
            "peso": {
                "Produto A": "1kg",
                "Produto B": "1.2kg",
            },
            "tamanho": {
                "Produto A": "M",
                "Produto B": "G",
            },
        },
    }


def test_should_return_422_when_comparing_less_than_two_items(
    test_client: TestClient,
    sample_items: List[Dict],
):
    response = test_client.post("/items", json=sample_items[0])
    assert response.status_code == 201
    item = response.json()

    response = test_client.get("/items/compare", params={"ids": [item["id"]]})

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {
                    "actual_length": 1,
                    "field_type": "List",
                    "min_length": 2,
                },
                "input": [
                    "1",
                ],
                "loc": [
                    "query",
                    "ids",
                ],
                "msg": "List should have at least 2 items after validation, not 1",
                "type": "too_short",
            },
        ],
    }


def test_should_return_422_when_comparing_more_than_five_items(
    test_client: TestClient,
    sample_items: List[Dict],
):
    created_items = []
    for i in range(6):
        item = dict(sample_items[0])
        item["name"] = f"Produto {i + 1}"
        response = test_client.post("/items", json=item)
        assert response.status_code == 201
        created_items.append(response.json())

    response = test_client.get(
        "/items/compare",
        params={"ids": [item["id"] for item in created_items]},
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {
                    "actual_length": 6,
                    "field_type": "List",
                    "max_length": 5,
                },
                "input": [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                ],
                "loc": [
                    "query",
                    "ids",
                ],
                "msg": "List should have at most 5 items after validation, not 6",
                "type": "too_long",
            },
        ],
    }


def test_should_return_400_when_comparing_duplicate_items(
    test_client: TestClient,
    sample_items: List[Dict],
):
    response = test_client.post("/items", json=sample_items[0])
    assert response.status_code == 201
    item = response.json()

    response = test_client.get(
        "/items/compare",
        params={"ids": [item["id"], item["id"]]},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "IDs duplicados não são permitidos na comparação",
    }


def test_should_return_404_when_item_not_found(
    test_client: TestClient,
    sample_items: List[Dict],
):
    response = test_client.post("/items", json=sample_items[0])
    assert response.status_code == 201
    item = response.json()

    response = test_client.get(
        "/items/compare",
        params={"ids": [item["id"], 999]},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Itens não encontrados: {999}",
    }
