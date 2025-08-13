import os
from pathlib import Path

import pytest

# Configura o ambiente de teste antes de qualquer teste
TEST_DATA_DIR = Path("tests/data")
TEST_ITEMS_FILE = TEST_DATA_DIR / "test_items.json"

# Garante que o diretório de teste existe
TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture(autouse=True)
def setup_test_environment():
    """
    Configura o ambiente de teste.
    Este fixture é executado automaticamente antes de cada teste.
    """
    # Guarda o valor original da variável de ambiente
    original_data_file = os.environ.get("DATA_FILE")
    
    # Configura a variável de ambiente para usar o arquivo de teste
    os.environ["DATA_FILE"] = str(TEST_ITEMS_FILE)
    
    # Garante que o arquivo de teste está vazio no início
    if TEST_ITEMS_FILE.exists():
        os.remove(TEST_ITEMS_FILE)
    
    yield
    
    # Limpa o arquivo de teste
    if TEST_ITEMS_FILE.exists():
        os.remove(TEST_ITEMS_FILE)
    
    # Restaura o valor original da variável de ambiente
    if original_data_file:
        os.environ["DATA_FILE"] = original_data_file
    else:
        os.environ.pop("DATA_FILE", None)
