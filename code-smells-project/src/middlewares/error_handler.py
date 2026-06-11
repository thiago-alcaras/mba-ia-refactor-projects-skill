from flask import jsonify
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        return jsonify({"erro": str(error), "sucesso": False}), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"erro": "Recurso não encontrado", "sucesso": False}), 404

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logger.error("Unexpected error", exc_info=True)
        return jsonify({"erro": "Erro interno do servidor", "sucesso": False}), 500
