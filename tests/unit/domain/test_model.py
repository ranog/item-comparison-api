import pytest
from pydantic import ValidationError

from src.domain.item import Item, ItemBase, ItemCreate, ItemUpdate


def test_valid_item_base():
    item = ItemBase(
        name="Smartphone",
        image_url="https://example.com/image.jpg",
        description="Um smartphone moderno",
        price=999.99,
        rating=4.5,
        specifications={"cor": "preto", "armazenamento": "128GB"},
    )

    assert item.name == "Smartphone"
    assert str(item.image_url) == "https://example.com/image.jpg"
    assert item.description == "Um smartphone moderno"
    assert abs(item.price - 999.99) < 0.001
    assert abs(item.rating - 4.5) < 0.001
    assert item.specifications == {"cor": "preto", "armazenamento": "128GB"}


def test_empty_name():
    with pytest.raises(ValidationError) as error:
        ItemBase(
            name="",
            image_url="https://example.com/image.jpg",
            description="Descrição",
            price=100.0,
            rating=4.0,
        )
    assert "não pode ser vazio" in str(error.value)


def test_empty_description():
    with pytest.raises(ValidationError) as exc_info:
        ItemBase(
            name="Nome",
            image_url="https://example.com/image.jpg",
            description="",
            price=100.0,
            rating=4.0,
        )
    assert "não pode ser vazio" in str(exc_info.value)


def test_invalid_price():
    with pytest.raises(ValidationError) as error:
        ItemBase(
            name="Nome",
            image_url="https://example.com/image.jpg",
            description="Descrição",
            price=-10.0,
            rating=4.0,
        )
    assert "must be a positive number" in str(error.value)


@pytest.mark.parametrize(
    "rating",
    [
        5.1,
        -0.1,
    ],
)
def test_invalid_rating(rating):
    with pytest.raises(ValidationError) as error:
        ItemBase(
            name="Nome",
            image_url="https://example.com/image.jpg",
            description="Descrição",
            price=100.0,
            rating=rating,
        )
    assert "must be between 0 and 5" in str(error.value)


def test_invalid_image_url():
    with pytest.raises(ValidationError):
        ItemBase(
            name="Nome",
            image_url="invalid-url",
            description="Descrição",
            price=100.0,
            rating=4.0,
        )


def test_create_item():
    item = ItemCreate(
        name="Produto",
        image_url="https://example.com/image.jpg",
        description="Descrição do produto",
        price=199.99,
        rating=4.5,
    )

    assert isinstance(item, ItemCreate)
    assert item.name == "Produto"


def test_update_item_partial():
    item = ItemUpdate(name="Novo Nome")

    assert item.name == "Novo Nome"
    assert item.description is None
    assert item.price is None
    assert item.rating is None
    assert item.specifications is None


def test_update_item_full():
    item = ItemUpdate(
        name="Produto Atualizado",
        image_url="https://example.com/new-image.jpg",
        description="Nova descrição",
        price=299.99,
        rating=4.8,
        specifications={"cor": "azul"},
    )

    assert item.name == "Produto Atualizado"
    assert str(item.image_url) == "https://example.com/new-image.jpg"
    assert item.specifications == {"cor": "azul"}


def test_invalid_update_price():
    with pytest.raises(ValidationError) as error:
        ItemUpdate(price=-10.0)

    assert "must be a positive number" in str(error.value)


def test_create_item_with_id():
    item = Item(
        id=1,
        name="Produto Final",
        image_url="https://example.com/image.jpg",
        description="Descrição final",
        price=399.99,
        rating=4.9,
        specifications={"marca": "Exemplo"},
    )

    assert item.id == 1
    assert isinstance(item.id, int)
    assert item.name == "Produto Final"


@pytest.mark.parametrize(
    "id",
    [
        0,
        -1,
    ],
)
def test_invalid_id(id):
    with pytest.raises(ValidationError) as error:
        Item(
            id=id,
            name="Produto",
            image_url="https://example.com/image.jpg",
            description="Descrição",
            price=100.0,
            rating=4.0,
        )
    assert "Input should be greater than 0" in str(error.value)
