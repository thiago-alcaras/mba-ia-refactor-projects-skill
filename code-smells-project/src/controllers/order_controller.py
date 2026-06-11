import logging
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class OrderController:
    def __init__(self, order_model):
        self.order_model = order_model

    def create_order(self, dados):
        if not dados:
            return {"erro": "Dados inválidos"}, 400

        usuario_id = dados.get("usuario_id")
        itens = dados.get("itens", [])

        if not usuario_id:
            return {"erro": "Usuario ID é obrigatório"}, 400
        if not itens or len(itens) == 0:
            return {"erro": "Pedido deve ter pelo menos 1 item"}, 400

        resultado = self.order_model.create(usuario_id, itens)
        if "erro" in resultado:
            return {"erro": resultado["erro"], "sucesso": False}, 400

        return {"dados": resultado, "sucesso": True, "mensagem": "Pedido criado com sucesso"}, 201

    def list_user_orders(self, usuario_id):
        pedidos = self.order_model.get_by_user(usuario_id)
        return {"dados": pedidos, "sucesso": True}, 200

    def list_all_orders(self):
        pedidos = self.order_model.get_all()
        return {"dados": pedidos, "sucesso": True}, 200

    def update_order_status(self, pedido_id, dados):
        novo_status = dados.get("status", "") if dados else ""
        if novo_status not in Settings.VALID_ORDER_STATUSES:
            return {"erro": "Status inválido"}, 400

        self.order_model.update_status(pedido_id, novo_status)
        logger.info("Order status updated", extra={"pedido_id": pedido_id, "status": novo_status})
        return {"sucesso": True, "mensagem": "Status atualizado"}, 200

    def get_sales_report(self):
        relatorio = self.order_model.get_sales_report()
        return {"dados": relatorio, "sucesso": True}, 200
