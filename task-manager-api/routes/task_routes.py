from flask import Blueprint, request, jsonify
from controllers.task_controller import TaskController

task_bp = Blueprint('tasks', __name__)
task_controller = TaskController()


@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    result, status = task_controller.get_all()
    return jsonify(result), status


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    result, status = task_controller.get_by_id(task_id)
    return jsonify(result), status


@task_bp.route('/tasks', methods=['POST'])
def create_task():
    result, status = task_controller.create(request.get_json())
    return jsonify(result), status


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    result, status = task_controller.update(task_id, request.get_json())
    return jsonify(result), status


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    result, status = task_controller.delete(task_id)
    return jsonify(result), status


@task_bp.route('/tasks/search', methods=['GET'])
def search_tasks():
    query = request.args.get('q', '')
    status_filter = request.args.get('status', '')
    priority = request.args.get('priority', '')
    user_id = request.args.get('user_id', '')
    result, status = task_controller.search(query, status_filter, priority, user_id)
    return jsonify(result), status


@task_bp.route('/tasks/stats', methods=['GET'])
def task_stats():
    result, status = task_controller.get_stats()
    return jsonify(result), status
