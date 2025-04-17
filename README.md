# Sistema de Pedidos Northwind MVC

Este projeto demonstra um sistema simples de gerenciamento de pedidos usando o banco de dados Northwind, implementado com duas abordagens: SQL puro (psycopg2) e SQLAlchemy ORM.

## Pré-requisitos

- Python 3.13
- Servidor PostgreSQL em execução
- Banco de dados Northwind instalado no PostgreSQL

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/yourusername/MVC-psycopg2-vs-SqlAlchemy.git
cd MVC-psycopg2-vs-SqlAlchemy
```

2. Instale o pipenv caso ainda não tenha:
```bash
pip install pipenv
```

3. Instale as dependências:
```bash
pipenv install
```

4. Configure a conexão com o banco de dados:
Edite o arquivo `src/connect.py` e atualize as configurações de conexão:

```python
# Para conexão psycopg
database_connection = psycopg.connect(
    host='localhost',
    dbname='northwind',
    user='seu_usuario',
    password='sua_senha',
    autocommit=False
)

# String de conexão para SQLAlchemy
DATA_BASE_CONNECTION_STRING = 'postgresql://seu_usuario:sua_senha@localhost:5432/northwind'
```

## Executando a Aplicação

1. Ative o ambiente virtual:
```bash
pipenv shell
```

2. Inicie a aplicação:
```bash
python src/main.py
```

## Como Usar

### Criando um Novo Pedido

1. Na janela principal, você verá várias abas. Escolha entre:
   - "Criar Pedido (Driver)" - Usa SQL puro
   - "Criar Pedido (ORM)" - Usa SQLAlchemy

2. Preencha os campos necessários:
   - ID do Cliente (ex: "ALFKI")
   - ID do Produto (ex: 1)
   - Quantidade (ex: 5)
   - ID do Funcionário (ex: 1)

3. Clique em "Criar Pedido" para enviar

### Visualizando Relatórios de Pedidos

1. Vá para a aba "Relatório de Pedido"
2. Digite o ID do Pedido
3. Clique em "Buscar Pedido" para ver os detalhes

### Gerando Ranking de Funcionários

1. Vá para a aba "Ranking de Funcionários"
2. Digite o intervalo de datas:
   - Data Inicial (AAAA-MM-DD)
   - Data Final (AAAA-MM-DD)
3. Clique em "Gerar Ranking" para ver as métricas de desempenho

## Nota de Segurança

A aplicação inclui uma demonstração de vulnerabilidade de SQL injection:
- Na aba "Criar Pedido (Driver)", há um alternador para "Modo SQL Injection"
- Quando ativado (🔓), o sistema fica vulnerável a SQL injection
- Quando desativado (🔒), o sistema usa consultas parametrizadas

**Atenção**: O modo SQL injection é apenas para fins educacionais e nunca deve ser usado em ambientes de produção.

## Estrutura do Projeto

- `src/`
  - `controllers/` - Lógica de negócios
  - `models/` - Camada de acesso a dados
    - `dtos/` - Objetos de Transferência de Dados
    - `model_orm/` - Modelos SQLAlchemy
    - `utils/` - Funções auxiliares
  - `main.py` - Aplicação GUI
  - `connect.py` - Configuração de conexão com banco de dados