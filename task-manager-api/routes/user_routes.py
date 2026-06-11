from flask import Blueprint, request, jsonify
from controllers.user_controller import UserController

user_bp = Blueprint('users', __name__)
user_controller = UserController()


@user_bp.route('/users', methods=['GET'])
def get_users():
    result, status = user_controller.get_all()
    return jsonify(result), status


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    result, status = user_controller.get_by_id(user_id)
    return jsonify(result), status


@user_bp.route('/users', methods=['POST'])
def create_user():
    result, status = user_controller.create(request.get_json())
    return jsonify(result), status


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    result, status = user_controller.update(user_id, request.get_json())
    return jsonify(result), status
