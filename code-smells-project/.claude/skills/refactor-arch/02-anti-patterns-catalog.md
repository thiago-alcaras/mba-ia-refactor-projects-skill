# Referência: Catálogo de Anti-Patterns

## 1. [CRITICAL] SQL Injection

**Sinais de detecção:**
- Concatenação de strings em queries SQL: `"SELECT * FROM x WHERE id = " + str(id)`
- f-strings em queries: `f"SELECT * FROM x WHERE id = {id}"`
- Template strings em queries JS: `` `SELECT * FROM x WHERE id = ${id}` ``
- Ausência de parameterized queries / prepared statements

**Impacto:** Atacante pode ler, modificar ou destruir todo o banco de dados.

**Severidade:** CRITICAL

---

## 2. [CRITICAL] Hardcoded Credentials

**Sinais de detecção:**
- `SECRET_KEY = "..."` com valor literal no código
- Senhas de banco em variáveis: `dbPass = "senha_super_secreta"`
- API keys no código: `paymentGatewayKey = "pk_live_..."`
- Credenciais SMTP hardcoded: `email_password = "senha123"`
- Senhas de seed em texto claro sem hash

**Impacto:** Credenciais expostas no repositório permitem acesso não autorizado.

**Severidade:** CRITICAL

---

## 3. [CRITICAL] Arbitrary Code/SQL Execution Endpoint

**Sinais de detecção:**
- Endpoint que executa SQL arbitrário recebido do request body
- `eval()` ou `exec()` com input do usuário
- Endpoint `/admin/query` sem autenticação que aceita SQL livre

**Impacto:** Acesso irrestrito ao banco de dados, permite qualquer operação.

**Severidade:** CRITICAL

---

## 4. [HIGH] God Class / God Module

**Sinais de detecção:**
- Arquivo/classe com mais de 200 linhas contendo múltiplos domínios
- Um arquivo mistura models de produtos, usuários, pedidos, relatórios
- Classe única que gerencia DB, rotas, lógica de negócio e utilitários
- Mais de 5 responsabilidades distintas no mesmo módulo

**Impacto:** Impossível testar em isolamento, qualquer mudança pode quebrar tudo.

**Severidade:** HIGH

---

## 5. [HIGH] Insecure Password Handling

**Sinais de detecção:**
- Senhas armazenadas em texto puro (plaintext)
- Uso de MD5 ou SHA1 para hash de senhas (sem salt)
- Função de hash caseira (`badCrypto`)
- `hashlib.md5(pwd.encode()).hexdigest()` para senhas
- Endpoint que retorna senha do usuário na resposta

**Impacto:** Vazamento do banco expõe todas as senhas dos usuários.

**Severidade:** HIGH

---

## 6. [HIGH] Sensitive Data Exposure

**Sinais de detecção:**
- Endpoint de health/status retorna `secret_key` ou credenciais
- API de listagem de usuários retorna campo `senha`/`password`
- Logs com dados de cartão de crédito
- `console.log` com chaves de API ou tokens
- `to_dict()` que inclui campo de senha

**Impacto:** Informações sensíveis acessíveis por qualquer requisição.

**Severidade:** HIGH

---

## 7. [HIGH] Missing Authentication/Authorization

**Sinais de detecção:**
- Endpoints administrativos sem verificação de auth (ex: `/admin/reset-db`)
- Operações destrutivas (DELETE, reset) sem middleware de autenticação
- Ausência completa de JWT, session, ou qualquer mecanismo de auth
- Endpoints de relatório financeiro sem controle de acesso

**Impacto:** Qualquer pessoa pode executar operações privilegiadas.

**Severidade:** HIGH

---

## 8. [MEDIUM] N+1 Query Problem

**Sinais de detecção:**
- Loop que executa query individual para cada item de uma lista
- `cursor.execute()` dentro de `for item in items:`
- `Model.query.get(id)` dentro de loop iterando resultados
- Queries aninhadas: cursor dentro de cursor dentro de cursor

**Impacto:** Performance degrada exponencialmente com volume de dados.

**Severidade:** MEDIUM

---

## 9. [MEDIUM] Code Duplication

**Sinais de detecção:**
- Mesmo bloco de lógica repetido em 3+ locais (ex: verificação de overdue)
- Serialização manual repetida (construir dict campo a campo) em vez de usar `to_dict()`
- Validações idênticas copiadas entre endpoints
- Lógica de formatação duplicada

**Impacto:** Mudanças precisam ser feitas em múltiplos lugares, risco de inconsistência.

**Severidade:** MEDIUM

---

## 10. [MEDIUM] Business Logic in Routes/Controllers Layer

**Sinais de detecção:**
- Cálculos de desconto, validações de estoque, regras de negócio dentro da camada de rotas
- Route handlers com mais de 30 linhas de lógica
- Acesso direto ao banco dentro de route handlers (sem model/service layer)

**Impacto:** Impossível reutilizar lógica, dificulta testes unitários.

**Severidade:** MEDIUM

---

## 11. [MEDIUM] Deprecated API Usage

**Sinais de detecção:**
- Python: `datetime.utcnow()` (deprecated desde Python 3.12, usar `datetime.now(timezone.utc)`)
- Node.js: `new Buffer()` (usar `Buffer.from()`)
- Express 4.x: `app.del()` (usar `app.delete()`)
- Flask: `@app.before_first_request` (removed in Flask 2.3+)
- SQLAlchemy: `Model.query` (legacy pattern, preferir `db.session.execute`)

**Impacto:** Código pode quebrar em versões futuras; warnings em produção.

**Severidade:** MEDIUM

---

## 12. [LOW] Magic Numbers / Hardcoded Values

**Sinais de detecção:**
- Números literais em lógica de negócio: `if faturamento > 10000`
- Percentuais soltos: `desconto = faturamento * 0.1`
- Tamanhos limite sem constante nomeada: `if len(nome) > 200`
- Portas hardcoded: `port=5000`

**Impacto:** Difícil entender e modificar regras de negócio.

**Severidade:** LOW

---

## 13. [LOW] Poor Naming / Readability

**Sinais de detecção:**
- Variáveis de 1-2 caracteres: `u`, `e`, `p`, `cid`, `cc`
- Nomes genéricos: `data`, `result`, `temp`, `stuff`
- Funções sem indicar ação: `process()`, `handle()`, `doStuff()`
- Mistura de idiomas (português e inglês) inconsistente

**Impacto:** Código difícil de entender e manter.

**Severidade:** LOW

---

## 14. [LOW] Print Statements Instead of Logging

**Sinais de detecção:**
- `print()` para debug/monitoring em vez de `logging` module
- `console.log()` para informações operacionais sem estrutura
- Ausência de log levels (INFO, WARNING, ERROR)
- Print com dados sensíveis (emails, IDs)

**Impacto:** Sem controle de verbosidade, impossível filtrar logs em produção.

**Severidade:** LOW

---

## 15. [LOW] Unused Imports

**Sinais de detecção:**
- Módulos importados mas nunca utilizados no arquivo
- `import os, sys, json, datetime` onde apenas 1 é usado
- Imports que existem "por garantia"

**Impacto:** Poluição do namespace, confunde quem lê o código.

**Severidade:** LOW
