import logging
from datetime import datetime
from database import db
from models.task import Task
from models.user import User
from models.category import Category

logger = logging.getLogger(__name__)


class TaskController:
    def get_all(self):
        tasks = Task.query.all()
        result = []
        for task in tasks:
            data = task.to_dict()
            data['user_name'] = task.user.name if task.user else None
            data['category_name'] = task.category.name if task.category else None
            result.append(data)
        return result, 200

    def get_by_id(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return {'error': 'Task não encontrada'}, 404
        return task.to_dict(), 200

    def create(self, data):
        if not data:
            return {'error': 'Dados inválidos'}, 400

        title = data.get('title')
        if not title:
            return {'error': 'Título é obrigatório'}, 400
        if len(title) < 3:
            return {'error': 'Título muito curto'}, 400
        if len(title) > 200:
            return {'error': 'Título muito longo'}, 400

        status = data.get('status', 'pending')
        priority = data.get('priority', 3)

        if status not in Task.VALID_STATUSES:
            return {'error': 'Status inválido'}, 400
        if priority < Task.MIN_PRIORITY or priority > Task.MAX_PRIORITY:
            return {'error': 'Prioridade deve ser entre 1 e 5'}, 400

        user_id = data.get('user_id')
        category_id = data.get('category_id')

        if user_id and not User.query.get(user_id):
            return {'error': 'Usuário não encontrado'}, 404
        if category_id and not Category.query.get(category_id):
            return {'error': 'Categoria não encontrada'}, 404

        task = Task()
        task.title = title
        task.description = data.get('description', '')
        task.status = status
        task.priority = priority
        task.user_id = user_id
        task.category_id = category_id

        due_date = data.get('due_date')
        if due_date:
            try:
                task.due_date = datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                return {'error': 'Formato de data inválido. Use YYYY-MM-DD'}, 400

        tags = data.get('tags')
        if tags:
            task.tags = ','.join(tags) if isinstance(tags, list) else tags

        try:
            db.session.add(task)
            db.session.commit()
            logger.info("Task created: %d - %s", task.id, task.title)
            return task.to_dict(), 201
        except Exception:
            db.session.rollback()
            logger.error("Error creating task", exc_info=True)
            return {'error': 'Erro ao criar task'}, 500

    def update(self, task_id, data):
        task = Task.query.get(task_id)
        if not task:
            return {'error': 'Task não encontrada'}, 404

        if not data:
            return {'error': 'Dados inválidos'}, 400

        if 'title' in data:
            if len(data['title']) < 3:
                return {'error': 'Título muito curto'}, 400
            if len(data['title']) > 200:
                return {'error': 'Título muito longo'}, 400
            task.title = data['title']

        if 'description' in data:
            task.description = data['description']

        if 'status' in data:
            if data['status'] not in Task.VALID_STATUSES:
                return {'error': 'Status inválido'}, 400
            task.status = data['status']

        if 'priority' in data:
            if data['priority'] < Task.MIN_PRIORITY or data['priority'] > Task.MAX_PRIORITY:
                return {'error': 'Prioridade deve ser entre 1 e 5'}, 400
            task.priority = data['priority']

        if 'user_id' in data:
            if data['user_id'] and not User.query.get(data['user_id']):
                return {'error': 'Usuário não encontrado'}, 404
            task.user_id = data['user_id']

        if 'category_id' in data:
            if data['category_id'] and not Category.query.get(data['category_id']):
                return {'error': 'Categoria não encontrada'}, 404
            task.category_id = data['category_id']

        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
                except ValueError:
                    return {'error': 'Formato de data inválido'}, 400
            else:
                task.due_date = None

        if 'tags' in data:
            tags = data['tags']
            task.tags = ','.join(tags) if isinstance(tags, list) else tags

        task.updated_at = datetime.utcnow()

        try:
            db.session.commit()
            logger.info("Task updated: %d", task.id)
            return task.to_dict(), 200
        except Exception:
            db.session.rollback()
            return {'error': 'Erro ao atualizar'}, 500

    def delete(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return {'error': 'Task não encontrada'}, 404

        try:
            db.session.delete(task)
            db.session.commit()
            logger.info("Task deleted: %d", task_id)
            return {'message': 'Task deletada com sucesso'}, 200
        except Exception:
            db.session.rollback()
            return {'error': 'Erro ao deletar'}, 500

    def search(self, query, status, priority, user_id):
        tasks = Task.query

        if query:
            tasks = tasks.filter(
                db.or_(
                    Task.title.like(f'%{query}%'),
                    Task.description.like(f'%{query}%')
                )
            )
        if status:
            tasks = tasks.filter(Task.status == status)
        if priority:
            tasks = tasks.filter(Task.priority == int(priority))
        if user_id:
            tasks = tasks.filter(Task.user_id == int(user_id))

        results = tasks.all()
        return [t.to_dict() for t in results], 200

    def get_stats(self):
        total = Task.query.count()
        pending = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        done = Task.query.filter_by(status='done').count()
        cancelled = Task.query.filter_by(status='cancelled').count()

        all_tasks = Task.query.all()
        overdue_count = sum(1 for t in all_tasks if t.is_overdue())

        return {
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'done': done,
            'cancelled': cancelled,
            'overdue': overdue_count,
            'completion_rate': round((done / total) * 100, 2) if total > 0 else 0,
        }, 200
