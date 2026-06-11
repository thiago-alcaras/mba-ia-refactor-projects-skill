================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   JavaScript + Express 4.18.2
Files:   3 analyzed | ~170 lines of code

## Summary
CRITICAL: 3 | HIGH: 3 | MEDIUM: 2 | LOW: 3

## Findings

### [CRITICAL] Hardcoded Credentials
File: src/utils.js:1-7
Description: Credenciais de produção hardcoded no código: `dbPass: "senha_super_secreta_prod_123"`, `paymentGatewayKey: "pk_live_1234567890abcdef"`, `smtpUser`. Todas em plaintext no repositório.
Impact: Credenciais expostas permitem acesso ao banco, gateway de pagamento e servidor de email.
Recommendation: Mover todas as credenciais para variáveis de ambiente (`process.env`).

### [CRITICAL] God Class (AppManager)
File: src/AppManager.js:1-130
Description: Classe única contém TODA a lógica da aplicação — inicialização do banco, definição de rotas, lógica de checkout, processamento de pagamento, relatórios financeiros, deleção de usuários. Viola completamente SRP e separação MVC.
Impact: Impossível testar, manter ou evoluir. Qualquer mudança afeta todas as funcionalidades.
Recommendation: Separar em models (UserModel, CourseModel, EnrollmentModel), controllers (CheckoutController, CourseController), e routes.

### [CRITICAL] Sensitive Data Logging
File: src/AppManager.js:46
Description: `console.log(\`Processando cartão ${cc} na chave ${config.paymentGatewayKey}\`)` — número do cartão de crédito e chave do gateway logados em plaintext.
Impact: Violação de PCI-DSS. Dados de cartão expostos nos logs do servidor.
Recommendation: Nunca logar dados de cartão. Remover completamente esta linha.

### [HIGH] Insecure Password Hashing (badCrypto)
File: src/utils.js:18-23
Description: Função `badCrypto` usa um loop de 10.000 iterações de Base64 truncado como "hash". Não é um algoritmo de hash criptográfico — é facilmente reversível e não usa salt.
Impact: Senhas de todos os usuários podem ser recuperadas trivialmente.
Recommendation: Substituir por `bcrypt.hash()` com salt rounds adequado (10+).

### [HIGH] Callback Hell / Deep Nesting
File: src/AppManager.js:29-72
Description: Rota de checkout tem 6 níveis de callbacks aninhados (db.get → db.get → db.run → db.run → db.run → callback). Fluxo extremamente difícil de seguir.
Impact: Impossível manter, debugar ou testar. Race conditions silenciosas.
Recommendation: Converter para async/await com Promises wrapper sobre sqlite3.

### [HIGH] Orphan Data on Delete
File: src/AppManager.js:117-121
Description: `DELETE FROM users` não remove enrollments nem payments associados. A resposta até admite: "as matrículas e pagamentos ficaram sujos no banco".
Impact: Inconsistência de dados, foreign keys quebradas, relatórios incorretos.
Recommendation: Implementar cascade delete ou soft delete (marcar como inativo).

### [MEDIUM] N+1 Queries in Financial Report
File: src/AppManager.js:76-113
Description: Para cada curso, busca enrollments; para cada enrollment, busca user e payment individualmente. Com 100 cursos e 1000 matrículas = ~3000 queries.
Impact: Endpoint de relatório fica lento com volume de dados, podendo causar timeout.
Recommendation: Usar JOINs para buscar dados em 1-2 queries.

### [MEDIUM] Global Mutable State
File: src/utils.js:9-10
Description: `let globalCache = {}` e `let totalRevenue = 0` são estado global mutável exportado. Cache sem invalidação ou limites.
Impact: Memory leak progressivo, dados inconsistentes entre requests.
Recommendation: Remover global cache. Usar solução adequada (Redis) se necessário.

### [LOW] Single-Character Variable Names
File: src/AppManager.js:30-35
Description: Variáveis `u`, `e`, `p`, `cid`, `cc` sem significado claro. Requer leitura do body para entender o que cada uma representa.
Impact: Código ilegível, difícil de manter e revisar.
Recommendation: Usar nomes descritivos: `username`, `email`, `password`, `courseId`, `cardNumber`.

### [LOW] No Error Handling Structure
File: src/AppManager.js (todo o arquivo)
Description: Errors tratados inline com `return res.status(500).send("Erro DB")`. Sem middleware centralizado de error handling, sem logging estruturado.
Impact: Respostas de erro inconsistentes, erros silenciados, difícil diagnosticar problemas.
Recommendation: Implementar middleware de error handling centralizado com logging.

### [LOW] Missing Input Validation
File: src/AppManager.js:33
Description: Checkout valida apenas presença de campos (`if (!u || !e || !cid || !cc)`), sem validar formato de email, formato de cartão, ou tipo de dados.
Impact: Dados inválidos persistidos no banco, comportamento inesperado.
Recommendation: Adicionar validação de formato para email, card number, e IDs numéricos.

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
src/
├── app.js                     (composition root)
├── config/
│   └── settings.js            (env vars)
├── models/
│   ├── database.js            (connection + helpers)
│   ├── userModel.js           (bcrypt hashing)
│   ├── courseModel.js
│   ├── enrollmentModel.js
│   ├── paymentModel.js
│   └── auditModel.js
├── controllers/
│   ├── checkoutController.js  (checkout flow)
│   ├── courseController.js    (financial report)
│   └── userController.js     (user management)
├── routes/
│   └── index.js               (route definitions)
└── middlewares/
    ├── errorHandler.js        (centralized errors)
    └── logger.js              (structured logging)
```

Validation:
  ✓ Application boots without errors
  ✓ GET /health → 200
  ✓ POST /api/checkout → 200 (with valid card)
  ✓ GET /api/admin/financial-report → 200
  ✓ DELETE /api/users/:id → 200 (with cascade)
  ✓ All original endpoints respond correctly
  ✓ Zero CRITICAL anti-patterns remaining
  ✓ Credentials moved to environment variables
  ✓ bcrypt replaces badCrypto
  ✓ Credit card data no longer logged
  ✓ God Class eliminated (separated into 5 models + 3 controllers)
================================
