================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask 3.1.1
Files:   4 analyzed | ~600 lines of code

## Summary
CRITICAL: 4 | HIGH: 3 | MEDIUM: 3 | LOW: 3

## Findings

### [CRITICAL] SQL Injection
File: models.py:29-30
Description: Concatenação de strings em queries SQL em todo o arquivo. Exemplo: `cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))`. Padrão repetido em todas as funções de acesso ao banco (get_produto_por_id, criar_produto, atualizar_produto, login_usuario, criar_pedido, buscar_produtos, etc.).
Impact: Atacante pode ler, modificar ou destruir todo o banco de dados através de injeção de SQL em qualquer endpoint.
Recommendation: Usar parameterized queries com placeholders `?` em todas as queries.

### [CRITICAL] Hardcoded Credentials
File: app.py:7
Description: `app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"` hardcoded diretamente no código-fonte.
Impact: Credencial exposta no repositório permite falsificação de sessões e tokens.
Recommendation: Mover para variável de ambiente com `os.getenv("SECRET_KEY")`.

### [CRITICAL] Arbitrary SQL Execution Endpoint
File: app.py:56-71
Description: Endpoint `/admin/query` aceita qualquer SQL via request body e executa diretamente no banco sem autenticação. Permite SELECT, INSERT, UPDATE, DELETE — qualquer operação.
Impact: Acesso completo e irrestrito ao banco de dados por qualquer usuário na rede.
Recommendation: Remover completamente este endpoint. Usar ferramentas de administração de banco separadas.

### [CRITICAL] Plaintext Password Storage
File: database.py:82-86
Description: Senhas de usuários armazenadas em texto puro no banco (`"admin123"`, `"123456"`, `"senha123"`). Função `login_usuario` compara senhas em plaintext.
Impact: Qualquer vazamento do banco expõe todas as senhas. Endpoint `/usuarios` retorna senhas na resposta.
Recommendation: Usar `werkzeug.security.generate_password_hash` para armazenar e `check_password_hash` para verificar.

### [HIGH] God Module Pattern
File: models.py:1-310
Description: Arquivo único contém toda a lógica de acesso a dados para 4 domínios diferentes (produtos, usuários, pedidos, relatórios) com ~310 linhas.
Impact: Impossível testar em isolamento, qualquer mudança pode afetar domínios não relacionados.
Recommendation: Separar em `product_model.py`, `user_model.py`, `order_model.py` com classes por domínio.

### [HIGH] Sensitive Data Exposure
File: controllers.py:275-282
Description: Endpoint `health_check` retorna `"secret_key": "minha-chave-super-secreta-123"` e `"debug": True` na resposta JSON. Endpoint `/usuarios` retorna campo `senha` dos usuários.
Impact: Informações sensíveis expostas publicamente em endpoints acessíveis sem autenticação.
Recommendation: Remover dados sensíveis de responses. Nunca incluir senhas em serialização.

### [HIGH] Missing Authentication/Authorization
File: app.py:46-54
Description: Endpoint `/admin/reset-db` permite resetar todo o banco de dados sem qualquer autenticação. Todos os endpoints admin estão desprotegidos.
Impact: Qualquer pessoa pode destruir dados do sistema.
Recommendation: Implementar middleware de autenticação para endpoints administrativos.

### [MEDIUM] N+1 Query Problem
File: models.py:163-200
Description: Funções `get_pedidos_usuario` e `get_todos_pedidos` executam queries aninhadas em loop — para cada pedido, uma query busca itens, e para cada item, outra query busca o nome do produto.
Impact: Performance degrada exponencialmente com volume de dados (O(n²) queries).
Recommendation: Usar JOINs para buscar pedidos com itens e produtos em uma única query.

### [MEDIUM] Global Mutable State
File: database.py:4-5
Description: `db_connection = None` é uma variável global mutável compartilhada. Conexão singleton com `check_same_thread=False`.
Impact: Problemas de concorrência em ambientes multi-thread; estado imprevisível.
Recommendation: Usar connection pool ou criar conexão por request.

### [MEDIUM] No Input Validation on SQL-heavy Endpoints
File: models.py:281-310
Description: Função `buscar_produtos` constrói query dinâmica sem validar tipos dos parâmetros `termo`, `categoria`, `preco_min`, `preco_max` concatenando diretamente na string SQL.
Impact: Além do SQL injection, valores inválidos causam erros não tratados.
Recommendation: Usar parameterized queries e validar tipos antes de construir a query.

### [LOW] Magic Numbers
File: models.py:254-260
Description: Thresholds de desconto hardcoded: `if faturamento > 10000`, `elif faturamento > 5000`, `elif faturamento > 1000` com percentuais `0.1`, `0.05`, `0.02`.
Impact: Regras de negócio difíceis de entender e modificar sem contexto.
Recommendation: Extrair para constantes nomeadas em módulo de configuração.

### [LOW] Print Statements Instead of Logging
File: controllers.py (múltiplas linhas)
Description: Uso extensivo de `print()` para logging: `print("ERRO CRITICO ao criar pedido: " + str(e))`, `print("Produto criado com ID: " + str(id))`, `print("!!! BANCO DE DADOS RESETADO !!!")`.
Impact: Sem controle de log levels, impossível filtrar em produção.
Recommendation: Usar módulo `logging` com níveis apropriados (info, warning, error).

### [LOW] Debug Mode Enabled in Production
File: app.py:8, 82
Description: `app.config["DEBUG"] = True` hardcoded e `app.run(debug=True)`. Debug mode expõe stack traces e permite execução de código via debugger interativo.
Impact: Em produção, atacante pode executar código arbitrário via Werkzeug debugger.
Recommendation: Controlar via variável de ambiente, desabilitar em produção.

================================
Total: 13 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y

================================
PHASE 3: REFACTORING COMPLETE
================================
New Project Structure:
```
src/
├── __init__.py
├── app.py                    (composition root)
├── config/
│   ├── __init__.py
│   └── settings.py           (env vars, constants)
├── models/
│   ├── __init__.py
│   ├── database.py           (DB init + schema)
│   ├── product_model.py      (parameterized queries)
│   ├── user_model.py         (bcrypt hashing)
│   └── order_model.py        (JOINs, no N+1)
├── controllers/
│   ├── __init__.py
│   ├── product_controller.py
│   ├── user_controller.py
│   └── order_controller.py
├── views/
│   ├── __init__.py
│   └── routes.py             (thin route handlers)
└── middlewares/
    ├── __init__.py
    └── error_handler.py      (centralized error handling)
```

Validation:
  ✓ Application boots without errors
  ✓ GET /health → 200
  ✓ GET /produtos → 200 (lista produtos)
  ✓ POST /pedidos → 201 (cria pedido)
  ✓ GET /relatorios/vendas → 200
  ✓ All original endpoints respond correctly
  ✓ Zero CRITICAL anti-patterns remaining
  ✓ SQL Injection eliminated (parameterized queries)
  ✓ Credentials moved to environment variables
  ✓ Admin/query endpoint removed
  ✓ Passwords hashed with werkzeug
================================
