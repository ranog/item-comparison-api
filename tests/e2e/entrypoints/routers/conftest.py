import os
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from src.adapters.repository import JsonItemRepository
from src.entrypoints.handlers.items import service
from src.main import app

# Caminhos para arquivos de teste
TEST_DATA_DIR = Path("tests/data")
TEST_ITEMS_FILE = TEST_DATA_DIR / "test_items.json"

# Garante que o diretório de teste existe
TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Garante que o arquivo de teste está vazio no início
if TEST_ITEMS_FILE.exists():
    os.remove(TEST_ITEMS_FILE)


@pytest.fixture
def test_repository() -> JsonItemRepository:
    return JsonItemRepository(TEST_ITEMS_FILE)


@pytest.fixture
def test_client(test_repository: JsonItemRepository) -> Generator[TestClient, None, None]:
    service.repository = test_repository

    client = TestClient(app)

    yield client
    if os.path.exists(TEST_ITEMS_FILE):
        os.remove(TEST_ITEMS_FILE)
