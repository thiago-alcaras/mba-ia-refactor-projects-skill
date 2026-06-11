================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask 3.0.0 + SQLAlchemy
Files:   9 analyzed | ~550 lines of code

## Summary
CRITICAL: 2 | HIGH: 3 | MEDIUM: 3 | LOW: 3

## Findings

### [CRITICAL] MD5 Password Hashing
File: models/user.py:30-31
Description: `hashlib.md5(pwd.encode()).hexdigest()` usado para hash de senhas. MD5 é criptograficamente quebrado desde 2004, sem salt, permite rainbow table attacks.
Impact: Senhas de todos os usuários vulneráveis a ataques de dicionário e rainbow tables.
Recommendation: Substituir por `werkzeug.security.generate_password_hash` (usa pbkdf2 com salt).

### [CRITICAL] Hardcoded Email Credentials
File: services/notification_service.py:8-10
Description: `self.email_user = 'taskmanager@gmail.com'` e `self.email_password = 'senha123'` hardcoded no código-fonte.
Impact: Credenciais de email expostas no repositório. Permite acesso à conta de email do sistema.
Recommendation: Mover para variáveis de ambiente.

### [HIGH] Hardcoded SECRET_KEY
File: app.py:13
Description: `app.config['SECRET_KEY'] = 'super-secret-key-123'` hardcoded diretamente no app.
Impact: Permite forjar sessões Flask e tokens de segurança.
Recommendation: Carregar de variável de ambiente com valor padrão apenas para desenvolvimento.

### [HIGH] Sensitive Data in Response (Password Exposure)
File: models/user.py:19-26
Description: Método `to_dict()` inclui campo `'password': self.password` na serialização. Endpoint GET /users/:id retorna o hash da senha na resposta JSON.
Impact: Hash de senha exposto permite ataques offline. Viola princípio de mínimo privilégio.
Recommendation: Remover campo password do `to_dict()`.

### [HIGH] Business Logic in Routes (No Controller Layer)
File: routes/task_routes.py:1-200
Description: Toda a lógica de negócio está diretamente nos route handlers — validação, acesso ao banco, formatação. Arquivo task_routes.py tem ~200 linhas com lógica de CRUD completa inline.
Impact: Impossível testar lógica de negócio sem HTTP server. Violação do MVC.
Recommendation: Extrair lógica para controllers (`TaskController`, `UserController`).

### [MEDIUM] Code Duplication (Overdue Check)
File: routes/task_routes.py:31-40, 72-80, routes/report_routes.py:39-45
Description: Lógica de verificação de overdue duplicada 4+ vezes com o mesmo pattern de if/else aninhado (7 linhas cada). O model já tem `is_overdue()` mas não é usado nos routes.
Impact: Bug fix precisa ser aplicado em 4+ lugares. Risco de inconsistência.
Recommendation: Usar `task.is_overdue()` do model em todos os lugares. Incluir no `to_dict()`.

### [MEDIUM] Unused Imports
File: routes/task_routes.py:7
Description: `import json, os, sys, time` — nenhum destes módulos é utilizado no arquivo. Também em utils/helpers.py com imports não utilizados (os, sys, math, hashlib).
Impact: Poluição de namespace, confusão para desenvolvedores, imports desnecessários.
Recommendation: Remover todos os imports não utilizados.

### [MEDIUM] Deprecated API Usage (datetime.utcnow)
File: models/task.py:17-18, routes/task_routes.py, routes/report_routes.py
Description: Uso extensivo de `datetime.utcnow()` que é deprecated desde Python 3.12. Deve usar `datetime.now(timezone.utc)`.
Impact: Warnings em Python 3.12+, será removido em versões futuras.
Recommendation: Substituir por `datetime.now(datetime.timezone.utc)`.

### [LOW] Bare Except Clauses
File: routes/task_routes.py:63, 89, routes/report_routes.py
Description: `except:` sem especificar tipo de exceção em múltiplos handlers. Captura SystemExit, KeyboardInterrupt, etc.
Impact: Erros silenciados, difícil diagnosticar problemas reais.
Recommendation: Usar `except Exception as e:` com logging adequado.

### [LOW] Print Statements Instead of Logging
File: routes/task_routes.py:140, routes/user_routes.py:85
Description: `print(f"Task criada: {task.id}")`, `print(f"ERRO: {str(e)}")` em vez de logging estruturado.
Impact: Sem controle de log levels, output misturado com stdout da aplicação.
Recommendation: Usar `logging.getLogger(__name__)` com níveis (info, error).

### [LOW] Verbose Boolean Returns
File: models/task.py:43-55, models/user.py:35-38
Description: Pattern repetido de `if condition: return True; else: return False` em vez de simplesmente `return condition`.
Impact: Código desnecessariamente verboso, dificulta leitura.
Recommendation: Simplificar para `return new_status in valid` e `return self.role == 'admin'`.

================================
Total: 11 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y

================================
PHASE 3: REFACTORING COMPLETE
================================
New Project Structure:
```
task-manager-api/
├── app.py                     (composition root with create_app factory)
├── database.py                (SQLAlchemy instance)
├── seed.py                    (data seeding script)
├── requirements.txt
├── config/
│   ├── __init__.py
│   └── settings.py            (env vars, no hardcoded secrets)
├── models/
│   ├── __init__.py
│   ├── task.py                (with is_overdue in to_dict)
│   ├── user.py                (werkzeug password hashing, no password in to_dict)
│   └── category.py
├── controllers/
│   ├── __init__.py
│   ├── task_controller.py     (business logic extracted)
│   ├── user_controller.py
│   └── report_controller.py
├── routes/
│   ├── __init__.py
│   ├── task_routes.py         (thin handlers)
│   ├── user_routes.py
│   └── report_routes.py
├── services/
│   ├── __init__.py
│   └── notification_service.py (credentials from env)
├── middlewares/
│   ├── __init__.py
│   └── error_handler.py      (centralized)
└── utils/
    ├── __init__.py
    └── helpers.py
```

Validation:
  ✓ Application boots without errors
  ✓ GET /health → 200
  ✓ GET /tasks → 200
  ✓ POST /tasks → 201
  ✓ GET /users → 200
  ✓ GET /reports/summary → 200
  ✓ All original endpoints respond correctly
  ✓ Zero CRITICAL anti-patterns remaining
  ✓ MD5 replaced with werkzeug secure hashing
  ✓ Credentials moved to environment variables
  ✓ Password removed from to_dict()
  ✓ Controllers layer added
================================
