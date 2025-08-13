from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, PositiveInt, field_validator


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, description="Nome do produto")
    image_url: HttpUrl = Field(..., description="URL da imagem do produto")
    description: str = Field(..., min_length=1, description="Descrição do produto")
    price: float = Field(..., gt=0, description="Preço positivo")
    rating: float = Field(..., ge=0, le=5, description="Nota entre 0 e 5")
    specifications: dict[str, str] = Field(
        default_factory=dict, description="Mapa de especificações"
    )

    @field_validator("name", "description", mode="before")
    def no_blank(cls, v: str):
        if not v.strip():
            raise ValueError("não pode ser vazio")
        return v

    @field_validator("price", mode="before")
    def positive_values(cls, v: float):
        if v is not None and v < 0:
            raise ValueError("must be a positive number")
        return v

    @field_validator("rating", mode="before")
    def rating_range(cls, v: float):
        if v is not None and (v < 0 or v > 5):
            raise ValueError("must be between 0 and 5")
        return v


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    name: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    rating: Optional[float] = Field(None, ge=0, le=5)
    specifications: Optional[dict[str, str]] = None


class Item(ItemBase):
    id: PositiveInt = Field(..., description="Identificador do item")
