import logging
from werkzeug.security import generate_password_hash, check_password_hash

logger = logging.getLogger(__name__)


class UserModel:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT id, nome, email, tipo, criado_em FROM usuarios")
        return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, user_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT id, nome, email, tipo, criado_em FROM usuarios WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def create(self, nome, email, senha, tipo="cliente"):
        hashed = generate_password_hash(senha)
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            (nome, email, hashed, tipo)
        )
        self.db.commit()
        return cursor.lastrowid

    def authenticate(self, email, senha):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row and check_password_hash(row["senha"], senha):
            return {"id": row["id"], "nome": row["nome"], "email": row["email"], "tipo": row["tipo"]}
        return None
