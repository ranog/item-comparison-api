from pathlib import Path
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.adapters.repository import JsonItemRepository
from src.config.app import create_app
from src.config.dependencies import get_item_service
from src.service_layer.services import DefaultItemService

# Configura o caminho do arquivo de teste
TEST_DATA_DIR = Path("tests/data")
TEST_ITEMS_FILE = TEST_DATA_DIR / "test_items.json"


@pytest.fixture(scope="session", autouse=True)
def test_app() -> FastAPI:
    """
    Cria uma instância da aplicação específica para testes.
    """
    # Garante que o diretório de teste existe
    TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Cria um novo repositório específico para testes
    repository = JsonItemRepository(TEST_ITEMS_FILE)
    service = DefaultItemService(repository)

    # Cria a aplicação
    app = create_app()

    # Sobrescreve a dependência do serviço
    app.dependency_overrides[get_item_service] = lambda: service

    return app


@pytest.fixture
def test_client(test_app: FastAPI) -> Generator[TestClient, None, None]:
    """
    Cria um cliente de teste.
    """
    client = TestClient(test_app)

    # Garante que o arquivo de teste está limpo antes de cada teste
    if TEST_ITEMS_FILE.exists():
        TEST_ITEMS_FILE.unlink()

    yield client

    # Limpa o arquivo após o teste
    if TEST_ITEMS_FILE.exists():
        TEST_ITEMS_FILE.unlink()
