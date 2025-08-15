# Arquitetura do Item Comparison API

## Diagrama de Componentes

```mermaid
graph TD
    subgraph Client
        A[Frontend Application]
    end

    subgraph API Gateway
        B[FastAPI Application]
    end

    subgraph Domain Layer
        C[Item Entity]
        D[Comparison Entity]
    end

    subgraph Service Layer
        E[Item Service]
        F[Comparison Service]
    end

    subgraph Repository Layer
        G[Item Repository]
    end

    subgraph Storage
        H[JSON Storage]
    end

    A -->|HTTP Requests| B
    B -->|Routes to| E
    B -->|Routes to| F
    E -->|Uses| C
    F -->|Uses| C
    F -->|Uses| D
    E -->|Uses| G
    G -->|Reads/Writes| H
```

## Fluxo de Dados

```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI
    participant Service as Service Layer
    participant Domain as Domain Layer
    participant Repo as Repository
    participant Storage as JSON Storage

    Client->>API: GET /items/compare?ids=[1,2]
    API->>Service: compare_items(ids)
    Service->>Repo: list_items(ids)
    Repo->>Storage: read_items()
    Storage-->>Repo: items data
    Repo-->>Service: Item objects
    Service->>Domain: compare_items(items)
    Domain-->>Service: comparison result
    Service-->>API: comparison data
    API-->>Client: JSON Response
```

## Estrutura de Dados

```mermaid
classDiagram
    class Item {
        +int id
        +str name
        +HttpUrl image_url
        +str description
        +float price
        +float rating
        +Dict specifications
        +validate()
    }

    class ItemComparison {
        +List~Item~ items
        +Dict price_analysis
        +Dict rating_analysis
        +Dict specifications_comparison
        +compare_items()
    }

    class ItemRepository {
        +Dict storage
        +get(id)
        +list()
        +save(item)
        +delete(id)
    }

    class ItemService {
        +ItemRepository repository
        +get_item(id)
        +list_items()
        +create_item(data)
        +update_item(id, data)
        +delete_item(id)
    }

    ItemComparison --> Item
    ItemService --> ItemRepository
    ItemService --> Item
```

## Fluxo de Requisições

```mermaid
flowchart LR
    A[Client] -->|HTTP Request| B(FastAPI Router)
    B -->|Validate Request| C{Handler}
    C -->|Process| D[Service Layer]
    D -->|Business Logic| E[Domain Layer]
    D -->|Data Access| F[Repository]
    F -->|Storage| G[(JSON File)]
    E -->|Response| D
    D -->|Response| C
    C -->|HTTP Response| B
    B -->|JSON| A
```

## Decisões Arquiteturais

### 1. Clean Architecture
- **Por quê?** Separação clara de responsabilidades, facilitando manutenção e testes
- **Benefício:** Mudanças em uma camada não afetam as outras
- **Impacto:** Código mais organizado e testável

### 2. FastAPI como Framework
- **Por quê?** Performance, tipagem estática e documentação automática
- **Benefício:** Desenvolvimento rápido e seguro
- **Impacto:** API bem documentada e fácil de usar

### 3. Pydantic para Validação
- **Por quê?** Integração nativa com FastAPI e validação robusta
- **Benefício:** Garantia de dados corretos
- **Impacto:** Menos código de validação manual

### 4. Armazenamento em JSON
- **Por quê?** Requisito do projeto para não usar banco de dados
- **Benefício:** Simplicidade e portabilidade
- **Impacto:** Fácil de entender e modificar

### 5. Testes em Múltiplas Camadas
- **Por quê?** Garantia de qualidade em todos os níveis
- **Benefício:** Confiabilidade do código
- **Impacto:** Mudanças seguras e documentadas

## Considerações de Segurança

1. **Validação de Entrada**
   - Todos os dados são validados via Pydantic
   - Proteção contra injeção de dados maliciosos

2. **Limites de Requisição**
   - Máximo de 5 itens por comparação
   - Previne sobrecarga do servidor

3. **URLs Seguras**
   - Validação de URLs de imagens
   - Apenas HTTPS permitido

## Considerações de Performance

1. **Otimizações**
   - Cache de resultados frequentes
   - Respostas compactas

2. **Limitações**
   - Armazenamento em JSON pode ser lento para grandes volumes
   - Recomendado para datasets pequenos/médios

## Evolução Futura

1. **Possíveis Melhorias**
   - Implementação de cache
   - Suporte a banco de dados
   - Autenticação e autorização
   - Sistema de rate limiting

2. **Pontos de Extensão**
   - Novos critérios de comparação
   - Suporte a mais tipos de produtos
   - API de busca avançada
