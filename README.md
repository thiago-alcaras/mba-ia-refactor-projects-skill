# Skill de Auditoria e Refatoração Arquitetural

Skill para Claude Code que automatiza a análise, auditoria e refatoração de projetos backend para o padrão MVC. Agnóstica de tecnologia — funciona com Python/Flask e Node.js/Express.

## Análise Manual

### Projeto 1 — code-smells-project (Python/Flask)

| # | Severidade | Problema | Arquivo:Linha | Justificativa |
|---|-----------|----------|---------------|---------------|
| 1 | CRITICAL | SQL Injection via concatenação de strings | models.py:29-30 | Todas as queries usam `"... WHERE id = " + str(id)` — permite execução de SQL arbitrário via input |
| 2 | CRITICAL | Credenciais hardcoded | app.py:7 | SECRET_KEY em plaintext no código-fonte exposta no repositório |
| 3 | CRITICAL | Endpoint de SQL arbitrário sem auth | app.py:56-71 | `/admin/query` executa qualquer SQL recebido no body |
| 4 | CRITICAL | Senhas armazenadas em plaintext | database.py:82-86 | Banco populado com senhas sem hash, login compara em texto puro |
| 5 | HIGH | God Module (models.py com 310 linhas) | models.py:1-310 | 4 domínios (produtos, usuários, pedidos, relatórios) em um único arquivo |
| 6 | HIGH | Dados sensíveis expostos em endpoints | controllers.py:275-282 | health_check retorna secret_key; /usuarios retorna senhas |
| 7 | MEDIUM | N+1 queries em listagem de pedidos | models.py:163-200 | 3 níveis de cursor aninhados: pedidos → itens → produtos |
| 8 | LOW | Magic numbers em regras de desconto | models.py:254-260 | Thresholds (10000, 5000, 1000) e percentuais (0.1, 0.05) soltos |
| 9 | LOW | Print statements em vez de logging | controllers.py (múltiplas) | `print("ERRO CRITICO...")` sem níveis de log |

### Projeto 2 — ecommerce-api-legacy (Node.js/Express)

| # | Severidade | Problema | Arquivo:Linha | Justificativa |
|---|-----------|----------|---------------|---------------|
| 1 | CRITICAL | Credenciais de produção hardcoded | src/utils.js:1-7 | dbPass, paymentGatewayKey, smtpUser em plaintext |
| 2 | CRITICAL | God Class (AppManager) | src/AppManager.js:1-130 | DB, rotas, checkout, pagamento, relatórios — tudo em 1 classe |
| 3 | CRITICAL | Dados de cartão logados em console | src/AppManager.js:46 | Número do cartão + API key do gateway impressos em log |
| 4 | HIGH | Hash de senha inseguro (badCrypto) | src/utils.js:18-23 | Base64 iterado não é criptografia; trivialmente reversível |
| 5 | HIGH | Dados órfãos em DELETE de usuário | src/AppManager.js:117-121 | Delete não remove enrollments/payments — integridade quebrada |
| 6 | MEDIUM | N+1 queries no relatório financeiro | src/AppManager.js:76-113 | Para cada curso, busca enrollments, para cada enrollment busca user e payment |
| 7 | LOW | Variáveis de 1 caractere | src/AppManager.js:30-35 | `u`, `e`, `p`, `cid`, `cc` — ilegível |

### Projeto 3 — task-manager-api (Python/Flask)

| # | Severidade | Problema | Arquivo:Linha | Justificativa |
|---|-----------|----------|---------------|---------------|
| 1 | CRITICAL | MD5 para hash de senha | models/user.py:30-31 | MD5 quebrado desde 2004, sem salt — rainbow table attack trivial |
| 2 | CRITICAL | Credenciais SMTP hardcoded | services/notification_service.py:8-10 | Email e senha em plaintext no código |
| 3 | HIGH | SECRET_KEY hardcoded | app.py:13 | `'super-secret-key-123'` permite forjar sessões |
| 4 | HIGH | to_dict() expõe password hash | models/user.py:19-26 | Hash retornado em GET /users — permite ataque offline |
| 5 | HIGH | Lógica de negócio nos routes | routes/task_routes.py:1-200 | Sem controller layer, routes com 200+ linhas de lógica |
| 6 | MEDIUM | Duplicação da lógica overdue (4x) | routes/task_routes.py:31-40 | Mesmo if/else de 7 linhas repetido em 4 locais |
| 7 | MEDIUM | Imports não utilizados | routes/task_routes.py:7 | `import json, os, sys, time` — nenhum usado |
| 8 | LOW | Bare except clauses | routes/task_routes.py:63 | `except:` captura tudo incluindo SystemExit |

---

## Construção da Skill

### Decisões de Design

A skill foi estruturada com um `SKILL.md` principal que funciona como prompt sequencial (3 fases) e 5 arquivos de referência Markdown que fornecem conhecimento de domínio:

1. **01-project-analysis.md** — Heurísticas de detecção de linguagem, framework, banco de dados e padrão arquitetural via análise de arquivos de configuração
2. **02-anti-patterns-catalog.md** — 15 anti-patterns catalogados com sinais de detecção concretos e acionáveis
3. **03-report-template.md** — Template padronizado para relatório de auditoria
4. **04-architecture-guidelines.md** — Definição do padrão MVC alvo com responsabilidades de cada camada
5. **05-refactoring-playbook.md** — 10 transformações com exemplos antes/depois

### Anti-patterns Incluídos

| Anti-pattern | Severidade | Por quê |
|-------------|-----------|---------|
| SQL Injection | CRITICAL | Presente no code-smells-project (todas as queries) |
| Hardcoded Credentials | CRITICAL | Presente nos 3 projetos |
| Arbitrary SQL Execution | CRITICAL | Presente no code-smells-project |
| God Class / God Module | HIGH | Presente no code-smells + ecommerce-api |
| Insecure Password Handling | HIGH | Presente nos 3 projetos (plaintext, MD5, badCrypto) |
| Sensitive Data Exposure | HIGH | Presente nos 3 projetos |
| Missing Auth/Authorization | HIGH | Presente no code-smells-project |
| N+1 Queries | MEDIUM | Presente no code-smells + ecommerce-api |
| Code Duplication | MEDIUM | Presente no task-manager-api |
| Business Logic in Routes | MEDIUM | Presente no task-manager-api |
| Deprecated API Usage | MEDIUM | datetime.utcnow no task-manager |
| Magic Numbers | LOW | Presente no code-smells-project |
| Poor Naming | LOW | Presente no ecommerce-api |
| Print Instead of Logging | LOW | Presente nos 3 projetos |
| Unused Imports | LOW | Presente no task-manager-api |

### Agnosticismo de Tecnologia

A skill detecta a stack automaticamente via arquivo de dependências:
- `requirements.txt` → Python
- `package.json` → Node.js
- Dependências internas → Framework (Flask, Express)

Os sinais de detecção no catálogo incluem patterns para ambas as linguagens (ex: SQL injection com string concat em Python E template literals em JS). O playbook tem exemplos antes/depois para ambas as stacks.

### Desafios Encontrados

1. **Projeto parcialmente organizado (task-manager-api)**: Já tinha models/routes/services, mas sem controllers e com problemas de segurança graves. A skill precisa identificar problemas mesmo em código "razoavelmente" organizado.
2. **Validação pós-refatoração**: Garantir que todos os endpoints continuam funcionando após reestruturação requer testes automatizados no final da Fase 3.

---

## Resultados

### Resumo dos Relatórios

| Projeto | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---------|----------|------|--------|-----|-------|
| code-smells-project | 4 | 3 | 3 | 3 | 13 |
| ecommerce-api-legacy | 3 | 3 | 2 | 3 | 11 |
| task-manager-api | 2 | 3 | 3 | 3 | 11 |

### Comparação Antes/Depois

#### code-smells-project

**Antes:**
```
code-smells-project/
├── app.py          (monolito, routes + config + admin)
├── controllers.py  (toda lógica HTTP)
├── database.py     (conexão global)
├── models.py       (todo acesso a dados, 310 linhas)
└── requirements.txt
```

**Depois:**
```
code-smells-project/
├── src/
│   ├── app.py                    (composition root, 44 linhas)
│   ├── config/settings.py        (env vars + constantes)
│   ├── models/
│   │   ├── database.py           (schema + seed)
│   │   ├── product_model.py      (queries parametrizadas)
│   │   ├── user_model.py         (bcrypt hashing)
│   │   └── order_model.py        (JOINs, sem N+1)
│   ├── controllers/
│   │   ├── product_controller.py
│   │   ├── user_controller.py
│   │   └── order_controller.py
│   ├── views/routes.py           (handlers finos)
│   └── middlewares/error_handler.py
└── requirements.txt
```

#### ecommerce-api-legacy

**Antes:**
```
ecommerce-api-legacy/
├── src/
│   ├── app.js          (15 linhas, apenas boot)
│   ├── AppManager.js   (God Class, 130 linhas)
│   └── utils.js        (credenciais + badCrypto)
└── package.json
```

**Depois:**
```
ecommerce-api-legacy/
├── src/
│   ├── app.js                    (composition root)
│   ├── config/settings.js        (env vars)
│   ├── models/
│   │   ├── database.js           (Promise wrappers)
│   │   ├── userModel.js          (bcrypt)
│   │   ├── courseModel.js
│   │   ├── enrollmentModel.js
│   │   ├── paymentModel.js
│   │   └── auditModel.js
│   ├── controllers/
│   │   ├── checkoutController.js
│   │   ├── courseController.js
│   │   └── userController.js
│   ├── routes/index.js
│   └── middlewares/
│       ├── errorHandler.js
│       └── logger.js
└── package.json
```

#### task-manager-api

**Antes:**
```
task-manager-api/
├── app.py              (hardcoded SECRET_KEY)
├── database.py
├── seed.py
├── models/             (MD5 hashing, password em to_dict)
├── routes/             (200+ linhas com lógica de negócio)
├── services/           (credenciais SMTP hardcoded)
└── utils/
```

**Depois:**
```
task-manager-api/
├── app.py              (create_app factory)
├── database.py
├── seed.py
├── config/settings.py  (env vars)
├── models/             (werkzeug hashing, password removido de to_dict)
├── controllers/        (lógica extraída dos routes)
├── routes/             (handlers finos, <15 linhas cada)
├── services/           (credenciais via env vars)
├── middlewares/        (error handler centralizado)
└── utils/
```

### Checklist de Validação

#### Projeto 1 — code-smells-project
- [x] Linguagem detectada corretamente (Python)
- [x] Framework detectado corretamente (Flask 3.1.1)
- [x] Domínio descrito corretamente (E-commerce API)
- [x] Número de arquivos: 4 analisados
- [x] Relatório com mínimo 5 findings (13 total)
- [x] Pelo menos 1 CRITICAL (4 encontrados)
- [x] Estrutura MVC implementada
- [x] Configuração via env vars
- [x] SQL parametrizado
- [x] Senhas com hash seguro
- [x] Aplicação inicia sem erros
- [x] Endpoints originais respondem

#### Projeto 2 — ecommerce-api-legacy
- [x] Linguagem detectada corretamente (JavaScript)
- [x] Framework detectado corretamente (Express 4.18.2)
- [x] Domínio descrito corretamente (LMS com checkout)
- [x] Número de arquivos: 3 analisados
- [x] Relatório com mínimo 5 findings (11 total)
- [x] Pelo menos 1 CRITICAL (3 encontrados)
- [x] Estrutura MVC implementada
- [x] Credenciais removidas do código
- [x] bcrypt substitui badCrypto
- [x] Aplicação inicia sem erros
- [x] Endpoints originais respondem

#### Projeto 3 — task-manager-api
- [x] Linguagem detectada corretamente (Python)
- [x] Framework detectado corretamente (Flask 3.0.0 + SQLAlchemy)
- [x] Domínio descrito corretamente (Task Manager)
- [x] Número de arquivos: 9 analisados
- [x] Relatório com mínimo 5 findings (11 total)
- [x] Pelo menos 1 CRITICAL (2 encontrados)
- [x] Controllers layer adicionada
- [x] MD5 substituído por werkzeug
- [x] Password removido do to_dict
- [x] Aplicação inicia sem erros
- [x] Endpoints originais respondem

### Validação de Execução

```
# Projeto 1 - code-smells-project
$ python -c "from src.app import app; c=app.test_client(); print(c.get('/health').status_code)"
200

# Projeto 2 - ecommerce-api-legacy
$ node -e "require('./src/app')" → LMS API running on port 3000
$ curl http://localhost:3000/health → {"status":"ok","service":"ecommerce-api-legacy"}

# Projeto 3 - task-manager-api
$ python -c "from app import app; c=app.test_client(); print(c.get('/health').status_code)"
200
```

---

## Como Executar

### Pré-requisitos

- **Claude Code** instalado e configurado (ou Gemini CLI / OpenAI Codex)
- Python 3.10+ (para projetos Flask)
- Node.js 18+ (para projeto Express)

### Executar a Skill

```bash
# Projeto 1
cd code-smells-project
claude "/refactor-arch"

# Projeto 2
cd ../ecommerce-api-legacy
claude "/refactor-arch"

# Projeto 3
cd ../task-manager-api
claude "/refactor-arch"
```

### Validar Refatoração

```bash
# Projeto 1
cd code-smells-project
pip install -r requirements.txt
python -c "from src.app import app; app.test_client().get('/health')"

# Projeto 2
cd ecommerce-api-legacy
npm install
npm start
# Em outro terminal: curl http://localhost:3000/health

# Projeto 3
cd task-manager-api
pip install -r requirements.txt
python seed.py
python -c "from app import app; app.test_client().get('/health')"
```

---

## Estrutura do Repositório

```
mba-ia-refactor-projects-skill/
├── README.md
├── code-smells-project/
│   ├── .claude/skills/refactor-arch/   ← SKILL
│   │   ├── SKILL.md
│   │   ├── 01-project-analysis.md
│   │   ├── 02-anti-patterns-catalog.md
│   │   ├── 03-report-template.md
│   │   ├── 04-architecture-guidelines.md
│   │   └── 05-refactoring-playbook.md
│   ├── src/                            ← CÓDIGO REFATORADO
│   ├── app.py                          (original, mantido para referência)
│   ├── models.py                       (original)
│   ├── controllers.py                  (original)
│   └── database.py                     (original)
├── ecommerce-api-legacy/
│   ├── .claude/skills/refactor-arch/   ← CÓPIA DA SKILL
│   ├── src/                            ← CÓDIGO REFATORADO
│   └── package.json
├── task-manager-api/
│   ├── .claude/skills/refactor-arch/   ← CÓPIA DA SKILL
│   ├── app.py                          ← REFATORADO
│   ├── config/                         ← NOVO
│   ├── controllers/                    ← NOVO
│   ├── middlewares/                    ← NOVO
│   ├── models/                         ← REFATORADO
│   ├── routes/                         ← REFATORADO
│   └── services/                       ← REFATORADO
└── reports/
    ├── audit-project-1.md
    ├── audit-project-2.md
    └── audit-project-3.md
```
