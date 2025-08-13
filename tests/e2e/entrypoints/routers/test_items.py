from typing import Dict

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.domain.item import Item


@pytest.fixture
def valid_item() -> Dict:
    return {
        "name": "Test Item",
        "image_url": "http://example.com/test.jpg",
        "description": "Test Description",
        "price": 10.0,
        "rating": 4.0,
        "specifications": {"cor": "azul", "tamanho": "M"},
    }


@pytest.fixture
def created_item(test_client: TestClient, valid_item: Dict) -> Item:
    response = test_client.post("/items", json=valid_item)
    return Item(**response.json())


def test_should_create_new_item(test_client: TestClient, valid_item: Dict):
    response = test_client.post("/items", json=valid_item)

    response_json = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_json["name"] == valid_item["name"]
    assert response_json["image_url"] == valid_item["image_url"]
    assert response_json["description"] == valid_item["description"]
    assert response_json["price"] == valid_item["price"]
    assert response_json["rating"] == valid_item["rating"]
    assert response_json["specifications"] == valid_item["specifications"]


def test_should_return_400_when_creating_item_with_invalid_data(test_client: TestClient):
    invalid_item = {
        "name": "",
        "image_url": "not-a-url",
        "description": "Test Description",
        "price": -10.0,
        "rating": 6.0,
    }

    response = test_client.post("/items", json=invalid_item)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_should_get_item_by_id(test_client: TestClient, created_item: Item):
    response = test_client.get(f"/items/{created_item.id}")

    assert response.status_code == status.HTTP_200_OK
    retrieved_item = Item(**response.json())
    assert retrieved_item == created_item


def test_should_return_404_when_getting_nonexistent_item(test_client: TestClient):
    response = test_client.get("/items/999999")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_should_list_all_items(test_client: TestClient, created_item: Item):
    response = test_client.get("/items")

    assert response.status_code == status.HTTP_200_OK
    items = [Item(**item) for item in response.json()]
    assert len(items) >= 1
    assert created_item in items


def test_should_list_items_by_ids(test_client: TestClient, created_item: Item):
    response = test_client.get(f"/items?ids={created_item.id}")

    assert response.status_code == status.HTTP_200_OK
    items = [Item(**item) for item in response.json()]
    assert len(items) == 1
    assert items[0] == created_item


def test_should_update_item_completely(
    test_client: TestClient, created_item: Item, valid_item: Dict
):
    new_data = valid_item.copy()
    new_data.update(
        {
            "name": "Updated Item",
            "description": "Updated Description",
            "price": 20.0,
            "specifications": {"cor": "verde", "tamanho": "G"},
        }
    )

    response = test_client.put(f"/items/{created_item.id}", json=new_data)

    assert response.status_code == status.HTTP_200_OK
    updated_item = Item(**response.json())
    assert updated_item.id == created_item.id
    assert updated_item.name == new_data["name"]
    assert updated_item.description == new_data["description"]
    assert updated_item.price == new_data["price"]
    assert updated_item.specifications == new_data["specifications"]


def test_should_update_item_partially(test_client: TestClient, created_item: Item):
    partial_update = {
        "name": "Partially Updated Item",
        "price": 15.0,
    }

    response = test_client.patch(f"/items/{created_item.id}", json=partial_update)

    assert response.status_code == status.HTTP_200_OK
    updated_item = Item(**response.json())
    assert updated_item.id == created_item.id
    assert updated_item.name == partial_update["name"]
    assert updated_item.price == partial_update["price"]
    # Campos não atualizados devem permanecer iguais
    assert updated_item.description == created_item.description
    assert updated_item.image_url == created_item.image_url
    assert updated_item.rating == created_item.rating
    assert updated_item.specifications == created_item.specifications


def test_should_delete_item(test_client: TestClient, created_item: Item):
    response = test_client.delete(f"/items/{created_item.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = test_client.get(f"/items/{created_item.id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_should_return_404_when_deleting_nonexistent_item(test_client: TestClient):
    response = test_client.delete("/items/999999")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_should_normalize_specifications_on_create(test_client: TestClient, valid_item: Dict):
    valid_item["specifications"] = {
        "COR": "  Azul  ",
        "TAMANHO": "  Grande  ",
    }

    response = test_client.post("/items", json=valid_item)

    assert response.status_code == status.HTTP_201_CREATED
    created_item = Item(**response.json())
    assert created_item.specifications == {
        "cor": "Azul",
        "tamanho": "Grande",
    }


def test_should_normalize_specifications_on_update(test_client: TestClient, created_item: Item):
    update_data = {
        "specifications": {
            "COR": "  Verde  ",
            "TAMANHO": "  Médio  ",
        }
    }

    response = test_client.patch(f"/items/{created_item.id}", json=update_data)

    assert response.status_code == status.HTTP_200_OK
    updated_item = Item(**response.json())
    assert updated_item.specifications == {
        "cor": "Verde",
        "tamanho": "Médio",
    }
