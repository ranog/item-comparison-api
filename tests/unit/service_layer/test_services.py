from typing import List
from unittest.mock import Mock

import pytest
from pydantic import HttpUrl

from src.domain.item import Item, ItemCreate, ItemUpdate
from src.service_layer.services import DefaultItemService


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def service(mock_repository):
    return DefaultItemService(mock_repository)


@pytest.fixture
def sample_items() -> List[Item]:
    return [
        Item(
            id=2,
            name="Item B",
            image_url=HttpUrl("http://example.com/b.jpg"),
            description="Descrição B",
            price=20.0,
            rating=4.5,
            specifications={"cor": "azul"},
        ),
        Item(
            id=1,
            name="Item A",
            image_url=HttpUrl("http://example.com/a.jpg"),
            description="Descrição A",
            price=10.0,
            rating=4.0,
            specifications={"cor": "vermelho"},
        ),
    ]


def test_should_return_items_sorted_by_id(service, mock_repository, sample_items):
    mock_repository.list_items.return_value = sample_items

    result = service.list_items()

    assert [item.id for item in result] == [1, 2]
    mock_repository.list_items.assert_called_once_with(ids=None)


def test_should_remove_duplicate_ids_when_listing_items(service, mock_repository, sample_items):
    mock_repository.list_items.return_value = sample_items
    ids_with_duplicates = [1, 2, 1, 2]

    result = service.list_items(ids=ids_with_duplicates)

    mock_repository.list_items.assert_called_once_with(ids=[1, 2])
    assert len(result) == 2


def test_should_normalize_specifications_when_creating_item(service, mock_repository):
    payload = ItemCreate(
        name="Test Item",
        image_url=HttpUrl("http://example.com/test.jpg"),
        description="Test Description",
        price=10.0,
        rating=4.0,
        specifications={"COR": "  Azul  ", "TAMANHO": "  Grande  "},
    )
    expected_item = Item(
        id=1,
        name="Test Item",
        image_url=HttpUrl("http://example.com/test.jpg"),
        description="Test Description",
        price=10.0,
        rating=4.0,
        specifications={"cor": "Azul", "tamanho": "Grande"},
    )
    mock_repository.create_item.return_value = expected_item

    result = service.create_item(payload)

    assert result == expected_item
    mock_repository.create_item.assert_called_once()
    created_payload = mock_repository.create_item.call_args[0][0]
    assert created_payload.specifications == {"cor": "Azul", "tamanho": "Grande"}


def test_should_return_none_when_updating_nonexistent_item(service, mock_repository):
    mock_repository.get_item.return_value = None
    payload = ItemUpdate(name="New Name")

    result = service.update_item(1, payload)

    assert result is None
    mock_repository.update_item.assert_not_called()


def test_should_normalize_specifications_when_updating_item(service, mock_repository):
    existing_item = Item(
        id=1,
        name="Test Item",
        image_url=HttpUrl("http://example.com/test.jpg"),
        description="Test Description",
        price=10.0,
        rating=4.0,
        specifications={"cor": "Azul"},
    )
    mock_repository.get_item.return_value = existing_item

    payload = ItemUpdate(specifications={"COR": "  Verde  ", "TAMANHO": "  Médio  "})
    expected_item = Item(
        id=1,
        name="Test Item",
        image_url=HttpUrl("http://example.com/test.jpg"),
        description="Test Description",
        price=10.0,
        rating=4.0,
        specifications={"cor": "Verde", "tamanho": "Médio"},
    )
    mock_repository.update_item.return_value = expected_item

    result = service.update_item(1, payload)

    assert result == expected_item
    mock_repository.update_item.assert_called_once()
    update_payload = mock_repository.update_item.call_args[0][1]
    assert update_payload.specifications == {"cor": "Verde", "tamanho": "Médio"}


def test_should_return_none_when_replacing_nonexistent_item(service, mock_repository):
    mock_repository.get_item.return_value = None
    payload = ItemCreate(
        name="Test Item",
        image_url=HttpUrl("http://example.com/test.jpg"),
        description="Test Description",
        price=10.0,
        rating=4.0,
    )

    result = service.replace_item(1, payload)

    assert result is None
    mock_repository.replace_item.assert_not_called()


def test_should_normalize_specifications_when_replacing_item(service, mock_repository):
    existing_item = Item(
        id=1,
        name="Test Item",
        image_url=HttpUrl("http://example.com/test.jpg"),
        description="Test Description",
        price=10.0,
        rating=4.0,
        specifications={"cor": "Azul"},
    )
    mock_repository.get_item.return_value = existing_item

    payload = ItemCreate(
        name="New Item",
        image_url=HttpUrl("http://example.com/new.jpg"),
        description="New Description",
        price=20.0,
        rating=5.0,
        specifications={"COR": "  Preto  ", "TAMANHO": "  Grande  "},
    )
    expected_item = Item(
        id=1,
        name="New Item",
        image_url=HttpUrl("http://example.com/new.jpg"),
        description="New Description",
        price=20.0,
        rating=5.0,
        specifications={"cor": "Preto", "tamanho": "Grande"},
    )
    mock_repository.replace_item.return_value = expected_item

    result = service.replace_item(1, payload)

    assert result == expected_item
    mock_repository.replace_item.assert_called_once()
    replace_id, replace_payload = mock_repository.replace_item.call_args[0]
    assert replace_id == 1
    assert replace_payload.specifications == {"cor": "Preto", "tamanho": "Grande"}
