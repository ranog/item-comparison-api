# �️ Item Comparison API

Backend da aplicação **Item Comparison**, desenvolvido em [FastAPI](https://fastapi.tiangolo.com/). Esta API fornece detalhes de produtos para uso em uma funcionalidade de comparação de itens, oferecendo endpoints claros e eficientes.

## 📱 Sobre o Projeto

O **Item Comparison** é uma API que permite a comparação detalhada de produtos, fornecendo informações completas e estruturadas para uma experiência de comparação eficiente e intuitiva.

## 🎯 Funcionalidades Principais

### � Detalhes dos Produtos
- **Informações básicas** do produto (nome, descrição)
- **Imagens** através de URLs
- **Preços** atualizados
- **Avaliações** dos produtos
- **Especificações técnicas** detalhadas

### 🔍 Recursos de Comparação
- **Múltiplos itens** podem ser comparados simultaneamente
- **Comparação detalhada** de especificações
- **Visualização lado a lado** dos produtos
- **Diferenças destacadas** entre produtos

### 📊 Dados Estruturados
- **Formato consistente** para todos os produtos
- **Dados organizados** por categorias
- **Fácil integração** com frontends
- **Respostas otimizadas** para performance

### ⚡ Características Técnicas
A API oferece:
- **🚀 Performance** - Respostas rápidas e eficientes
- **📝 Documentação** - Swagger UI e ReDoc integrados
- **� Segurança** - Boas práticas de segurança
- **� Escalabilidade** - Estrutura preparada para crescimento
- **🛠️ Manutenibilidade** - Código bem organizado e documentado

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos

- Python 3.13.3 (gerenciado com `pyenv`)
- [Poetry](https://python-poetry.org/docs/#installation)
- Make (para usar os comandos simplificados)

## Instalação das Dependências do Projeto

### LINUX

### Instalar o pyenv
Para gerenciar versões do Python, instale o pyenv seguindo as instruções:
[https://github.com/pyenv/pyenv#installation](https://github.com/pyenv/pyenv#installation)

### Instalar dependências para compilar e instalar o Python
```bash
# Instalar dependências necessárias
sudo apt-get update
sudo apt-get install make gcc build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
    libffi-dev liblzma-dev
```

### Instalar e configurar Python com pyenv
```bash
# Instalar Python
pyenv install 3.13.3

# Definir versão do Python para o projeto
pyenv local 3.13.3

# Instalar dependências do Python
pip install --upgrade pip setuptools wheel poetry
```

### Configurar e ativar ambiente virtual
```bash
# Criar ambiente virtual com Poetry
poetry env use 3.13.3

# Ativar ambiente virtual
source $(poetry env info --path)/bin/activate

# Instalar dependências do projeto
make install-deps
```

### Executar o projeto
```bash
# Iniciar o servidor local
make run
```

### Acessar Swagger UI e ReDoc - Local

Após executar o projeto, a documentação interativa estará disponível nos seguintes endereços:

- Swagger UI: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
- ReDoc: [http://127.0.0.1:8080/redoc](http://127.0.0.1:8080/redoc)

### Collection Insomnia

Para facilitar os testes da API, disponibilizamos uma collection do Insomnia que pode ser importada:

1. Baixe o arquivo `insomnia-collection.yaml` da pasta `docs/`
2. No Insomnia:
   - Clique em `Create` > `Import from File`
   - Selecione o arquivo baixado
   - A collection será importada com todos os endpoints configurados

A collection inclui:
- Endpoints para criar itens
- Endpoints para comparação
- Exemplos de payloads
- Variáveis de ambiente pré-configuradas

## 📐 Arquitetura do Projeto

Para uma visão detalhada da arquitetura, incluindo diagramas e fluxos, consulte nossa [documentação de arquitetura](docs/architecture.md).

### Visão Geral
O projeto segue os princípios da Arquitetura Limpa (Clean Architecture), organizando o código em camadas bem definidas:

```
src/
├── domain/         # Regras de negócio e entidades
├── service_layer/  # Casos de uso e serviços
├── adapters/       # Adaptadores e repositórios
├── entrypoints/    # Controllers e rotas da API
└── config/         # Configurações da aplicação
```

### Camadas da Arquitetura

1. **Domain Layer (src/domain/)**
   - Contém as entidades core do negócio (Item, Comparison)
   - Define as regras de validação básicas
   - Independente de frameworks e tecnologias

2. **Service Layer (src/service_layer/)**
   - Implementa os casos de uso da aplicação
   - Orquestra as operações entre entidades
   - Gerencia a lógica de negócio complexa

3. **Adapters Layer (src/adapters/)**
   - Implementa a persistência de dados
   - Gerencia o repositório de itens
   - Adapta interfaces externas para o domínio

4. **Entrypoints Layer (src/entrypoints/)**
   - Define os endpoints da API
   - Gerencia requisições e respostas HTTP
   - Implementa os handlers para cada operação

### Endpoints Principais

#### Items API
- `GET /items` - Lista todos os itens
- `GET /items/{item_id}` - Obtém detalhes de um item
- `POST /items` - Cria um novo item
- `PUT /items/{item_id}` - Atualiza um item completamente
- `PATCH /items/{item_id}` - Atualiza um item parcialmente
- `DELETE /items/{item_id}` - Remove um item

#### Comparison API
- `GET /items/compare?ids=[...]` - Compara múltiplos itens

### Estrutura dos Dados

#### Item
```json
{
  "id": 1,
  "name": "string",
  "image_url": "http://example.com/image.jpg",
  "description": "string",
  "price": 0,
  "rating": 0,
  "specifications": {
    "additionalProp1": "string"
  }
}
```

#### Comparison Response
```json
{
  "items": [...],
  "price_analysis": {
    "lowest": 0,
    "highest": 0,
    "difference": 0
  },
  "rating_analysis": {
    "lowest": 0,
    "highest": 0,
    "average": 0
  },
  "specifications_comparison": {
    "property": {
      "item_name": "value"
    }
  }
}
```

## 🧪 Testes

O projeto possui uma suíte completa de testes:

### Estrutura de Testes
```
tests/
├── unit/            # Testes unitários
├── integration/     # Testes de integração
└── e2e/            # Testes end-to-end
```

### Executando os Testes
```bash
# Executar todos os testes
make tests
```

## 🔨 Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **Pydantic**: Validação de dados e serialização
- **Poetry**: Gerenciamento de dependências
- **Pytest**: Framework de testes
- **Ruff**: Linting e formatação de código
- **Pre-commit**: Hooks de git para qualidade de código
```
