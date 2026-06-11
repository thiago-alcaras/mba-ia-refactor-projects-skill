# Referência: Playbook de Refatoração

Padrões concretos de transformação para cada anti-pattern, com exemplos antes/depois.

---

## 1. SQL Injection → Parameterized Queries

### Antes (Python/sqlite3)
```python
cursor.execute("SELECT * FROM users WHERE id = " + str(id))
cursor.execute("SELECT * FROM users WHERE email = '" + email + "' AND senha = '" + senha + "'")
cursor.execute(
    "INSERT INTO produtos (nome, preco) VALUES ('" + nome + "', " + str(preco) + ")"
)
```

### Depois (Python/sqlite3)
```python
cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
cursor.execute("SELECT * FROM users WHERE email = ? AND senha = ?", (email, senha))
cursor.execute(
    "INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco)
)
```

### Depois (Node.js/sqlite3)
```javascript
// Antes: db.get(`SELECT * FROM users WHERE id = ${id}`)
db.get("SELECT * FROM users WHERE id = ?", [id], callback);
```

---

## 2. Hardcoded Credentials → Environment Variables

### Antes (Python)
```python
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
app.config["DEBUG"] = True
```

### Depois (Python)
```python
# config/settings.py
import os

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-in-production")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///app.db")
    PORT = int(os.getenv("PORT", "5000"))
```

### Antes (Node.js)
```javascript
const config = {
    dbPass: "senha_super_secreta_prod_123",
    paymentGatewayKey: "pk_live_1234567890abcdef",
};
```

### Depois (Node.js)
```javascript
// config/settings.js
const config = {
    dbPass: process.env.DB_PASSWORD || "dev-password",
    paymentGatewayKey: process.env.PAYMENT_KEY || "pk_test_placeholder",
    port: parseInt(process.env.PORT || "3000"),
};
module.exports = config;
```

---

## 3. God Class → Separação por Domínio

### Antes
```python
# models.py — 300+ linhas com tudo junto
def get_todos_produtos(): ...
def criar_produto(): ...
def get_todos_usuarios(): ...
def criar_usuario(): ...
def criar_pedido(): ...
def relatorio_vendas(): ...
```

### Depois
```python
# models/product_model.py
class ProductModel:
    def __init__(self, db):
        self.db = db
    def get_all(self): ...
    def get_by_id(self, id): ...
    def create(self, data): ...

# models/user_model.py
class UserModel:
    def __init__(self, db):
        self.db = db
    def get_all(self): ...
    def authenticate(self, email, password): ...

# models/order_model.py
class OrderModel:
    def __init__(self, db):
        self.db = db
    def create(self, user_id, items): ...
    def get_by_user(self, user_id): ...
```

---

## 4. Insecure Password → Secure Hashing

### Antes (Python)
```python
# Plaintext
cursor.execute("INSERT INTO users (senha) VALUES ('" + senha + "')")

# MD5 insecure
import hashlib
self.password = hashlib.md5(pwd.encode()).hexdigest()
```

### Depois (Python)
```python
from werkzeug.security import generate_password_hash, check_password_hash

def set_password(self, password):
    self.password = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password, password)
```

### Antes (Node.js)
```javascript
function badCrypto(pwd) {
    let hash = "";
    for(let i = 0; i < 10000; i++) {
        hash += Buffer.from(pwd).toString('base64').substring(0, 2);
    }
    return hash.substring(0, 10);
}
```

### Depois (Node.js)
```javascript
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 10;

async function hashPassword(password) {
    return bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(password, hash) {
    return bcrypt.compare(password, hash);
}
```

---

## 5. Sensitive Data Exposure → Data Sanitization

### Antes
```python
def to_dict(self):
    return {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'password': self.password,  # EXPÕE SENHA!
    }

# Health endpoint expõe secrets
return {"secret_key": "minha-chave-super-secreta-123", "debug": True}
```

### Depois
```python
def to_dict(self):
    return {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        # password NUNCA incluído na serialização
    }

# Health endpoint seguro
return {"status": "ok", "database": "connected"}
```

---

## 6. N+1 Queries → JOIN ou Eager Loading

### Antes (Python/sqlite3)
```python
cursor.execute("SELECT * FROM pedidos")
for pedido in pedidos:
    cursor2.execute("SELECT * FROM itens WHERE pedido_id = " + str(pedido["id"]))
    for item in itens:
        cursor3.execute("SELECT nome FROM produtos WHERE id = " + str(item["produto_id"]))
```

### Depois (Python/sqlite3)
```python
cursor.execute("""
    SELECT p.*, i.quantidade, i.preco_unitario, pr.nome as produto_nome
    FROM pedidos p
    LEFT JOIN itens_pedido i ON i.pedido_id = p.id
    LEFT JOIN produtos pr ON pr.id = i.produto_id
    WHERE p.usuario_id = ?
""", (usuario_id,))
```

### Depois (SQLAlchemy)
```python
# Usar eager loading
tasks = Task.query.options(
    db.joinedload(Task.user),
    db.joinedload(Task.category)
).all()
```

---

## 7. Business Logic in Routes → Controller Layer

### Antes
```python
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    # 50 linhas de lógica de negócio aqui
    # validação, cálculos, queries, notificações...
    return jsonify(result), 201
```

### Depois
```python
# routes/order_routes.py
@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    result, status = order_controller.create(data)
    return jsonify(result), status

# controllers/order_controller.py
class OrderController:
    def __init__(self, order_model):
        self.order_model = order_model

    def create(self, data):
        # Validação
        if not data.get("user_id"):
            return {"error": "user_id required"}, 400
        # Lógica de negócio
        order = self.order_model.create(data["user_id"], data["items"])
        return {"data": order}, 201
```

---

## 8. Arbitrary SQL Endpoint → Remoção

### Antes
```python
@app.route("/admin/query", methods=["POST"])
def executar_query():
    query = request.get_json().get("sql", "")
    cursor.execute(query)  # EXECUTA QUALQUER SQL!
```

### Depois
```python
# REMOVER COMPLETAMENTE este endpoint.
# Se necessário para debug em desenvolvimento:
# - Proteger com autenticação forte
# - Limitar a SELECT apenas
# - Desabilitar em produção via variável de ambiente
# - Melhor: não implementar, usar ferramentas de DB admin separadas
```

---

## 9. Code Duplication → Extração de Método

### Antes
```python
# Repetido 4 vezes em task_routes.py:
if t.due_date:
    if t.due_date < datetime.utcnow():
        if t.status != 'done' and t.status != 'cancelled':
            task_data['overdue'] = True
        else:
            task_data['overdue'] = False
    else:
        task_data['overdue'] = False
else:
    task_data['overdue'] = False
```

### Depois
```python
# No model Task:
def is_overdue(self):
    if not self.due_date:
        return False
    return self.due_date < datetime.utcnow() and self.status not in ('done', 'cancelled')

# No route/controller:
task_data['overdue'] = task.is_overdue()
```

---

## 10. Print Statements → Structured Logging

### Antes
```python
print("ERRO CRITICO ao criar pedido: " + str(e))
print("Produto criado com ID: " + str(id))
print("!!! BANCO DE DADOS RESETADO !!!")
```

### Depois
```python
import logging
logger = logging.getLogger(__name__)

logger.error("Failed to create order", exc_info=True)
logger.info("Product created", extra={"product_id": id})
logger.warning("Database reset executed")
```
