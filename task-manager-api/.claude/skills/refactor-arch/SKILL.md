# Skill: refactor-arch — Auditoria e Refatoração Arquitetural

## Descrição
Skill para análise, auditoria e refatoração arquitetural de projetos backend para o padrão MVC. Funciona com qualquer linguagem/framework (Python/Flask, Node.js/Express, etc.).

## Invocação
```
/refactor-arch
```

## Execução
A skill executa 3 fases sequenciais:

---

### FASE 1 — ANÁLISE DO PROJETO

1. Detectar a stack do projeto:
   - Ler arquivos de dependências (`requirements.txt`, `package.json`, `Gemfile`, `pom.xml`, etc.)
   - Identificar linguagem, framework, versão e dependências
   - Consultar referência: `01-project-analysis.md`

2. Mapear a arquitetura atual:
   - Contar e listar todos os arquivos de código-fonte
   - Identificar padrão atual (monolito, parcialmente organizado, MVC, etc.)
   - Identificar banco de dados (SQLite, PostgreSQL, MongoDB, etc.)
   - Identificar domínio da aplicação (e-commerce, LMS, task manager, etc.)

3. Imprimir resumo no formato:
```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      [linguagem]
Framework:     [framework versão]
Dependencies:  [lista de deps]
Domain:        [domínio da aplicação]
Architecture:  [descrição da arquitetura atual]
Source files:  [N] files analyzed
DB:            [tipo de banco + tabelas identificadas]
================================
```

---

### FASE 2 — AUDITORIA

1. Analisar cada arquivo contra o catálogo de anti-patterns:
   - Consultar referência: `02-anti-patterns-catalog.md`
   - Para cada anti-pattern, verificar sinais de detecção no código
   - Registrar arquivo, linhas exatas, severidade e recomendação

2. Verificar APIs deprecated:
   - Verificar se há uso de APIs/funções obsoletas para o framework detectado
   - Ex: `datetime.utcnow()` (deprecated no Python 3.12+), `express 4.x` deprecated APIs

3. Gerar relatório de auditoria:
   - Usar template de: `03-report-template.md`
   - Ordenar findings por severidade (CRITICAL → HIGH → MEDIUM → LOW)
   - Incluir contagem total por severidade

4. **OBRIGATÓRIO**: Apresentar o relatório completo ao usuário e **PERGUNTAR**:
   ```
   Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
   ```
   - **NÃO modificar nenhum arquivo** até receber confirmação explícita
   - Se o usuário responder "n", encerrar a execução

---

### FASE 3 — REFATORAÇÃO

1. Consultar guidelines de arquitetura:
   - Referência: `04-architecture-guidelines.md`
   - Aplicar padrão MVC adequado à stack detectada

2. Executar transformações:
   - Consultar referência: `05-refactoring-playbook.md`
   - Aplicar cada padrão de transformação relevante
   - Criar estrutura de diretórios MVC
   - Mover/reescrever código para as camadas corretas

3. Estrutura alvo (adaptar conforme stack):
   ```
   src/ (ou raiz)
   ├── config/          # Configurações e variáveis de ambiente
   ├── models/          # Abstração de dados e acesso ao banco
   ├── controllers/     # Lógica de negócio e orquestração
   ├── views/ ou routes/ # Roteamento e formatação de resposta
   ├── middlewares/     # Error handling, auth, logging
   └── app.py/app.js   # Entry point (composition root)
   ```

4. Validar resultado:
   - Verificar que a aplicação inicia sem erros
   - Verificar que todos os endpoints originais continuam funcionando
   - Verificar que nenhum anti-pattern CRITICAL permanece

5. Imprimir resultado:
```
================================
PHASE 3: REFACTORING COMPLETE
================================
New Project Structure:
[árvore de diretórios]

Validation:
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero CRITICAL anti-patterns remaining
================================
```

---

## Arquivos de Referência
- `01-project-analysis.md` — Heurísticas de detecção de stack e mapeamento
- `02-anti-patterns-catalog.md` — Catálogo de anti-patterns com severidades
- `03-report-template.md` — Template do relatório de auditoria
- `04-architecture-guidelines.md` — Regras do padrão MVC alvo
- `05-refactoring-playbook.md` — Transformações com exemplos antes/depois
