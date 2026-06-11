# Referência: Guidelines de Arquitetura MVC

## Princípio Central
Separação de responsabilidades em camadas com responsabilidades claras e bem definidas.

## Camadas do Padrão MVC Alvo

### 1. Config (`config/`)
**Responsabilidade:** Centralizar TODAS as configurações e variáveis de ambiente.

- Credenciais lidas de variáveis de ambiente (`os.getenv` / `process.env`)
- Valores padrão seguros para desenvolvimento
- Nenhum valor sensível hardcoded
- Constantes de negócio nomeadas

**Exemplos de conteúdo:**
- SECRET_KEY, DATABASE_URI, PORT
- Chaves de API externas
- Configurações de CORS, debug mode
- Constantes de negócio (limites de desconto, taxas, etc.)

### 2. Models (`models/`)
**Responsabilidade:** Abstração de dados e acesso ao banco.

- Um arquivo por entidade/domínio (ex: `product_model.py`, `user_model.py`)
- Queries parametrizadas (NUNCA concatenação de strings)
- Métodos CRUD por entidade
- Validação de dados no nível do modelo (se usar ORM)
- Serialização (`to_dict()`) sem expor dados sensíveis

**Regras:**
- Models NÃO devem importar Flask/Express request/response
- Models NÃO devem fazer print/console.log
- Models NÃO devem conhecer rotas ou controllers
- Senhas devem ser hasheadas com bcrypt ou equivalente seguro

### 3. Controllers (`controllers/`)
**Responsabilidade:** Orquestrar o fluxo da aplicação e lógica de negócio.

- Um arquivo por domínio (ex: `product_controller.py`, `order_controller.py`)
- Receber dados já parseados (não acessar `request` diretamente quando possível)
- Chamar models para acessar dados
- Aplicar regras de negócio
- Retornar resultado formatado

**Regras:**
- Controllers NÃO devem executar SQL diretamente
- Controllers NÃO devem conhecer detalhes do HTTP (headers, status codes) — isso é da camada de rotas
- Controllers DEVEM ser testáveis sem servidor HTTP

### 4. Views / Routes (`views/` ou `routes/`)
**Responsabilidade:** Roteamento HTTP, parsing de request, formatação de response.

- Definir endpoints (GET, POST, PUT, DELETE)
- Extrair dados do request (body, params, query)
- Chamar controller apropriado
- Formatar resposta HTTP (status code, JSON)
- Validação superficial de input (presença de campos obrigatórios)

**Regras:**
- Routes NÃO devem conter lógica de negócio
- Routes NÃO devem acessar banco diretamente
- Routes DEVEM ser finas (poucas linhas por handler)

### 5. Middlewares (`middlewares/`)
**Responsabilidade:** Comportamentos transversais (cross-cutting concerns).

- Error handling centralizado
- Autenticação/Autorização
- Logging
- Rate limiting
- CORS

**Regras:**
- Middlewares são reutilizáveis entre rotas
- Error handler deve capturar exceções e retornar formato padronizado

### 6. Entry Point (`app.py` / `app.js`)
**Responsabilidade:** Composition root — montar e iniciar a aplicação.

- Criar instância da aplicação
- Carregar configurações
- Registrar middlewares
- Registrar rotas/blueprints
- Inicializar banco de dados
- Iniciar servidor

**Regras:**
- NÃO deve conter lógica de negócio
- NÃO deve definir rotas inline
- DEVE ser limpo e legível (< 50 linhas idealmente)

## Regras de Segurança Obrigatórias

1. **Credenciais**: Sempre via variáveis de ambiente
2. **SQL**: Sempre parameterized queries
3. **Senhas**: Sempre hash seguro (bcrypt/argon2), nunca MD5/SHA1/plaintext
4. **Dados sensíveis**: Nunca expor em responses ou logs
5. **Endpoints admin**: Sempre protegidos por autenticação
6. **Debug mode**: Desativado em produção

## Adaptação por Stack

### Python/Flask
```
src/
├── __init__.py
├── app.py              # create_app() factory
├── config/
│   ├── __init__.py
│   └── settings.py     # classe Settings com env vars
├── models/
│   ├── __init__.py
│   ├── product_model.py
│   └── user_model.py
├── controllers/
│   ├── __init__.py
│   ├── product_controller.py
│   └── order_controller.py
├── views/
│   ├── __init__.py
│   └── routes.py       # Blueprints com rotas
└── middlewares/
    ├── __init__.py
    └── error_handler.py
```

### Node.js/Express
```
src/
├── app.js              # Express setup + composition
├── config/
│   └── settings.js     # Config from env vars
├── models/
│   ├── userModel.js
│   └── courseModel.js
├── controllers/
│   ├── userController.js
│   └── courseController.js
├── routes/
│   └── index.js        # Router definitions
└── middlewares/
    └── errorHandler.js
```
