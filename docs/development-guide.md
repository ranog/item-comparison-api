# Guia de Desenvolvimento

## Configuração do Ambiente

1. **Requisitos de Sistema**
   - Python 3.13.3
   - Poetry
   - Make
   - Git

2. **Configuração Inicial**
   ```bash
   # Clone o repositório
   git clone https://github.com/ranog/item-comparison-api.git
   cd item-comparison-api

   # Configure o Python
   pyenv install 3.13.3
   pyenv local 3.13.3

   # Configure o Poetry
   poetry env use 3.13.3
   poetry install
   ```

## Convenções de Código

### 1. Estilo de Código
- Use type hints em todas as funções
- Docstrings em todas as classes e métodos públicos
- Linhas com máximo de 100 caracteres
- Nomes de variáveis descritivos

### 2. Estrutura dos Commits
```
type(scope): description

[optional body]

[optional footer]
```

**Tipos de Commits:**
- feat: Nova funcionalidade
- fix: Correção de bug
- docs: Documentação
- style: Formatação
- refactor: Refatoração de código
- test: Testes
- chore: Manutenção

### 3. Branches
- main: Produção
- develop: Desenvolvimento
- feature/*: Novas funcionalidades
- fix/*: Correções
- docs/*: Documentação

## Processo de Desenvolvimento

### 1. Criando Nova Funcionalidade
1. Crie uma branch: `git checkout -b feature/nome-feature`
2. Implemente os testes
3. Implemente a funcionalidade
4. Execute os testes: `make tests`
5. Verifique a cobertura: `make coverage`
6. Formate o código: `make format`
7. Commit e push

### 2. Testes
- Testes unitários para lógica isolada
- Testes de integração para fluxos
- Testes e2e para APIs
- Mínimo de 90% de cobertura

### 3. Documentação
- Atualize o README.md se necessário
- Documente novas APIs
- Atualize diagramas se mudar a arquitetura

## Exemplos

### 1. Adicionando Novo Endpoint

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/new-endpoint")
async def new_endpoint():
    """
    Documentação do endpoint.
    
    Returns:
        dict: Descrição do retorno
    """
    return {"message": "Hello"}
```

### 2. Adicionando Nova Entidade

```python
from pydantic import BaseModel, Field

class NewEntity(BaseModel):
    """
    Documentação da entidade.
    """
    id: int = Field(..., description="ID único")
    name: str = Field(..., description="Nome")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Example"
            }
        }
```

### 3. Adicionando Novo Teste

```python
import pytest
from fastapi.testclient import TestClient

def test_new_feature(test_client: TestClient):
    """
    Teste da nova funcionalidade.
    """
    response = test_client.get("/new-endpoint")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}
```

## Solução de Problemas

### 1. Problemas Comuns

#### Poetry não encontra ambiente virtual
```bash
poetry env list  # Verifique ambientes
poetry env remove python  # Remova se necessário
poetry env use python3.13  # Crie novo ambiente
```

#### Testes falhando
1. Verifique se todas as dependências estão instaladas
2. Verifique se o ambiente virtual está ativo
3. Execute `pytest -v` para ver detalhes

#### Problemas de formatação
```bash
make format  # Formata o código
pre-commit run --all-files  # Verifica todos os arquivos
```

### 2. Debugging

1. Use o debugger do VS Code
2. Adicione logs temporários
3. Use `pytest -vv --pdb` para debug de testes

## Checklist de PR

- [ ] Testes implementados
- [ ] Cobertura de código mantida
- [ ] Documentação atualizada
- [ ] Código formatado
- [ ] Convenções de commit seguidas
- [ ] Branch atualizada com main
