# Referência: Análise de Projeto

## Heurísticas de Detecção de Linguagem

| Arquivo             | Linguagem   |
|---------------------|-------------|
| `requirements.txt`  | Python      |
| `setup.py` / `pyproject.toml` | Python |
| `package.json`      | JavaScript/Node.js |
| `Gemfile`           | Ruby        |
| `pom.xml` / `build.gradle` | Java |
| `go.mod`            | Go          |
| `Cargo.toml`        | Rust        |

## Heurísticas de Detecção de Framework

| Dependência          | Framework        |
|----------------------|------------------|
| `flask`              | Flask (Python)   |
| `django`             | Django (Python)  |
| `fastapi`            | FastAPI (Python) |
| `express`            | Express (Node.js)|
| `nestjs`             | NestJS (Node.js) |
| `rails`              | Rails (Ruby)     |
| `spring-boot`        | Spring Boot (Java)|

## Detecção de Banco de Dados

| Sinal                                    | Banco          |
|------------------------------------------|----------------|
| `sqlite3` import / `sqlite3` dependency  | SQLite         |
| `psycopg2` / `pg`                        | PostgreSQL     |
| `pymongo` / `mongoose`                   | MongoDB        |
| `mysql-connector` / `mysql2`             | MySQL          |
| `flask-sqlalchemy` / `sqlalchemy`        | SQLAlchemy ORM |
| `.db` file extension in config           | SQLite         |
| `:memory:` in connection string          | SQLite (in-memory) |

## Mapeamento de Arquitetura

### Indicadores de Monolito (sem separação)
- Todos os arquivos na raiz do projeto (sem pastas de domínio)
- Um único arquivo contém models + controllers + routes
- Arquivo com mais de 200 linhas misturando responsabilidades
- Menos de 5 arquivos de código-fonte total

### Indicadores de Separação Parcial
- Existem pastas como `models/`, `routes/`, `services/` mas:
  - Controllers ausentes (lógica nos routes)
  - Config misturado no app principal
  - Sem middleware de error handling separado

### Indicadores de MVC Adequado
- Pastas `models/`, `controllers/`, `views/` ou `routes/`
- Arquivo de configuração separado (`config/`)
- Error handling centralizado (`middlewares/`)
- Entry point limpo (composition root)

## Detecção de Domínio

Analisar nomes de tabelas/modelos, endpoints e variáveis para inferir o domínio:

| Sinais                                    | Domínio              |
|-------------------------------------------|----------------------|
| produtos, pedidos, carrinho, pagamento    | E-commerce           |
| courses, enrollments, students            | LMS / Educação       |
| tasks, categories, assignments, due_date  | Task Manager         |
| posts, comments, likes, followers         | Rede Social          |
| patients, appointments, doctors           | Saúde / Clínica      |
