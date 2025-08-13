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
