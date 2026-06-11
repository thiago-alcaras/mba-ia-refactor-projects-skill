import logging
import re
from database import db
from models.user import User

logger = logging.getLogger(__name__)


class UserController:
    def get_all(self):
        users = User.query.all()
        result = []
        for u in users:
            user_data = u.to_dict()
            user_data['task_count'] = len(u.tasks)
            result.append(user_data)
        return result, 200

    def get_by_id(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'error': 'Usuário não encontrado'}, 404

        data = user.to_dict()
        data['tasks'] = [t.to_dict() for t in user.tasks]
        return data, 200

    def create(self, data):
        if not data:
            return {'error': 'Dados inválidos'}, 400

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')

        if not name:
            return {'error': 'Nome é obrigatório'}, 400
        if not email:
            return {'error': 'Email é obrigatório'}, 400
        if not password:
            return {'error': 'Senha é obrigatória'}, 400

        if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', email):
            return {'error': 'Email inválido'}, 400

        if len(password) < 4:
            return {'error': 'Senha deve ter no mínimo 4 caracteres'}, 400

        existing = User.query.filter_by(email=email).first()
        if existing:
            return {'error': 'Email já cadastrado'}, 409

        if role not in ['user', 'admin', 'manager']:
            return {'error': 'Role inválido'}, 400

        user = User()
        user.name = name
        user.email = email
        user.set_password(password)
        user.role = role

        try:
            db.session.add(user)
            db.session.commit()
            logger.info("User created: %d - %s", user.id, user.name)
            return user.to_dict(), 201
        except Exception:
            db.session.rollback()
            logger.error("Error creating user", exc_info=True)
            return {'error': 'Erro ao criar usuário'}, 500

    def update(self, user_id, data):
        user = User.query.get(user_id)
        if not user:
            return {'error': 'Usuário não encontrado'}, 404

        if not data:
            return {'error': 'Dados inválidos'}, 400

        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', data['email']):
                return {'error': 'Email inválido'}, 400
            user.email = data['email']
        if 'role' in data:
            if data['role'] not in ['user', 'admin', 'manager']:
                return {'error': 'Role inválido'}, 400
            user.role = data['role']
        if 'active' in data:
            user.active = data['active']
        if 'password' in data:
            if len(data['password']) < 4:
                return {'error': 'Senha deve ter no mínimo 4 caracteres'}, 400
            user.set_password(data['password'])

        try:
            db.session.commit()
            logger.info("User updated: %d", user.id)
            return user.to_dict(), 200
        except Exception:
            db.session.rollback()
            return {'error': 'Erro ao atualizar usuário'}, 500
