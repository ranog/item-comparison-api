import json
from pathlib import Path
from typing import Generator

import pytest
from pydantic import HttpUrl

from src.adapters.repository import JsonItemRepository
from src.domain.model import ItemCreate, ItemUpdate


@pytest.fixture
def temp_json_file(tmp_path) -> Generator[Path, None, None]:
    json_file = tmp_path / "test_items.json"
    yield json_file
    if json_file.exists():
        json_file.unlink()


@pytest.fixture
def repository(temp_json_file: Path) -> JsonItemRepository:
    return JsonItemRepository(temp_json_file)


@pytest.fixture
def sample_item() -> ItemCreate:
    return ItemCreate(
        name="Test Item",
        image_url=HttpUrl("https://example.com/image.jpg"),
        description="Test Description",
        price=99.99,
        rating=4.5,
        specifications={"color": "blue", "size": "M"},
    )


def test_should_create_item_successfully(repository: JsonItemRepository, sample_item: ItemCreate):
    item = repository.create_item(sample_item)

    assert item.id == 1
    assert item.name == sample_item.name
    assert str(item.image_url) == str(sample_item.image_url)
    assert item.description == sample_item.description
    assert abs(item.price - sample_item.price) < 0.001
    assert abs(item.rating - sample_item.rating) < 0.001
    assert item.specifications == sample_item.specifications


def test_should_return_item_when_it_exists(repository: JsonItemRepository, sample_item: ItemCreate):
    created = repository.create_item(sample_item)

    retrieved = repository.get_item(created.id)

    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.name == created.name


def test_should_return_none_when_item_not_found(repository: JsonItemRepository):
    assert repository.get_item(999) is None


def test_should_return_empty_list_when_no_items_exist(repository: JsonItemRepository):
    assert repository.list_items() == []


def test_should_return_filtered_items_when_ids_provided(
    repository: JsonItemRepository, sample_item: ItemCreate
):
    item1 = repository.create_item(sample_item)
    repository.create_item(
        ItemCreate(
            name="Another Item",
            image_url=HttpUrl("https://example.com/image2.jpg"),
            description="Another Description",
            price=199.99,
            rating=4.0,
        )
    )

    filtered = repository.list_items(ids=[item1.id])

    assert len(filtered) == 1
    assert filtered[0].id == item1.id


def test_should_update_item_partially_when_it_exists(
    repository: JsonItemRepository, sample_item: ItemCreate
):
    created = repository.create_item(sample_item)
    update_data = ItemUpdate(name="Updated Name", price=199.99)

    updated = repository.update_item(created.id, update_data)

    assert updated is not None
    assert updated.id == created.id
    assert updated.name == "Updated Name"
    assert abs(updated.price - 199.99) < 0.001
    assert updated.description == created.description


def test_should_replace_item_completely_when_it_exists(
    repository: JsonItemRepository, sample_item: ItemCreate
):
    created = repository.create_item(sample_item)
    new_data = ItemCreate(
        name="Replaced Item",
        image_url=HttpUrl("https://example.com/new.jpg"),
        description="New Description",
        price=299.99,
        rating=5.0,
    )

    replaced = repository.replace_item(created.id, new_data)

    assert replaced is not None
    assert replaced.id == created.id
    assert replaced.name == new_data.name
    assert str(replaced.image_url) == str(new_data.image_url)


def test_should_delete_item_when_it_exists(repository: JsonItemRepository, sample_item: ItemCreate):
    created = repository.create_item(sample_item)

    assert repository.delete_item(created.id) is True
    assert repository.get_item(created.id) is None


def test_should_return_false_when_deleting_non_existing_item(repository: JsonItemRepository):
    assert repository.delete_item(999) is False


def test_should_persist_data_to_file_correctly(
    repository: JsonItemRepository, sample_item: ItemCreate, temp_json_file: Path
):
    created = repository.create_item(sample_item)

    assert temp_json_file.exists()

    with open(temp_json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["id"] == created.id
    assert data[0]["name"] == created.name


def test_should_handle_invalid_json_file_gracefully(temp_json_file: Path):
    temp_json_file.write_text("invalid json content")

    repository = JsonItemRepository(temp_json_file)

    assert repository.list_items() == []


def test_should_generate_sequential_ids_for_new_items(
    repository: JsonItemRepository, sample_item: ItemCreate
):
    item1 = repository.create_item(sample_item)
    item2 = repository.create_item(sample_item)
    item3 = repository.create_item(sample_item)

    assert item1.id == 1
    assert item2.id == 2
    assert item3.id == 3


def test_should_maintain_consistency_during_concurrent_operations(
    repository: JsonItemRepository, sample_item: ItemCreate
):
    number_of_items = 5
    items = []
    for _ in range(number_of_items):
        items.append(repository.create_item(sample_item))

    all_items = repository.list_items()

    assert len(all_items) == number_of_items
    assert len({item.id for item in all_items}) == number_of_items
