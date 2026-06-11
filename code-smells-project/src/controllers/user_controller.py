import logging

logger = logging.getLogger(__name__)


class UserController:
    def __init__(self, user_model):
        self.user_model = user_model

    def list_users(self):
        usuarios = self.user_model.get_all()
        return {"dados": usuarios, "sucesso": True}, 200

    def get_user(self, user_id):
        usuario = self.user_model.get_by_id(user_id)
        if usuario:
            return {"dados": usuario, "sucesso": True}, 200
        return {"erro": "Usuário não encontrado"}, 404

    def create_user(self, dados):
        if not dados:
            return {"erro": "Dados inválidos"}, 400

        nome = dados.get("nome", "")
        email = dados.get("email", "")
        senha = dados.get("senha", "")

        if not nome or not email or not senha:
            return {"erro": "Nome, email e senha são obrigatórios"}, 400

        user_id = self.user_model.create(nome, email, senha)
        logger.info("User created", extra={"user_id": user_id, "email": email})
        return {"dados": {"id": user_id}, "sucesso": True}, 201

    def login(self, dados):
        if not dados:
            return {"erro": "Dados inválidos"}, 400

        email = dados.get("email", "")
        senha = dados.get("senha", "")

        if not email or not senha:
            return {"erro": "Email e senha são obrigatórios"}, 400

        usuario = self.user_model.authenticate(email, senha)
        if usuario:
            logger.info("Login successful", extra={"email": email})
            return {"dados": usuario, "sucesso": True, "mensagem": "Login OK"}, 200
        else:
            return {"erro": "Email ou senha inválidos", "sucesso": False}, 401
