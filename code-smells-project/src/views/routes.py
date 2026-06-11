from flask import Blueprint, jsonify, request


def create_routes(product_controller, order_controller, user_controller):
    bp = Blueprint("api", __name__)

    # Health check
    @bp.route("/health")
    def health_check():
        return jsonify({"status": "ok", "service": "code-smells-project"}), 200

    @bp.route("/")
    def index():
        return jsonify({
            "mensagem": "Bem-vindo à API da Loja",
            "versao": "2.0.0",
            "endpoints": {
                "produtos": "/produtos",
                "usuarios": "/usuarios",
                "pedidos": "/pedidos",
                "login": "/login",
                "relatorios": "/relatorios/vendas",
                "health": "/health",
            }
        })

    # Products
    @bp.route("/produtos", methods=["GET"])
    def listar_produtos():
        body, status = product_controller.list_products()
        return jsonify(body), status

    @bp.route("/produtos/busca", methods=["GET"])
    def buscar_produtos():
        termo = request.args.get("q", "")
        categoria = request.args.get("categoria")
        preco_min = request.args.get("preco_min", type=float)
        preco_max = request.args.get("preco_max", type=float)
        body, status = product_controller.search_products(termo, categoria, preco_min, preco_max)
        return jsonify(body), status

    @bp.route("/produtos/<int:product_id>", methods=["GET"])
    def buscar_produto(product_id):
        body, status = product_controller.get_product(product_id)
        return jsonify(body), status

    @bp.route("/produtos", methods=["POST"])
    def criar_produto():
        body, status = product_controller.create_product(request.get_json())
        return jsonify(body), status

    @bp.route("/produtos/<int:product_id>", methods=["PUT"])
    def atualizar_produto(product_id):
        body, status = product_controller.update_product(product_id, request.get_json())
        return jsonify(body), status

    @bp.route("/produtos/<int:product_id>", methods=["DELETE"])
    def deletar_produto(product_id):
        body, status = product_controller.delete_product(product_id)
        return jsonify(body), status

    # Users
    @bp.route("/usuarios", methods=["GET"])
    def listar_usuarios():
        body, status = user_controller.list_users()
        return jsonify(body), status

    @bp.route("/usuarios/<int:user_id>", methods=["GET"])
    def buscar_usuario(user_id):
        body, status = user_controller.get_user(user_id)
        return jsonify(body), status

    @bp.route("/usuarios", methods=["POST"])
    def criar_usuario():
        body, status = user_controller.create_user(request.get_json())
        return jsonify(body), status

    @bp.route("/login", methods=["POST"])
    def login():
        body, status = user_controller.login(request.get_json())
        return jsonify(body), status

    # Orders
    @bp.route("/pedidos", methods=["POST"])
    def criar_pedido():
        body, status = order_controller.create_order(request.get_json())
        return jsonify(body), status

    @bp.route("/pedidos", methods=["GET"])
    def listar_todos_pedidos():
        body, status = order_controller.list_all_orders()
        return jsonify(body), status

    @bp.route("/pedidos/usuario/<int:usuario_id>", methods=["GET"])
    def listar_pedidos_usuario(usuario_id):
        body, status = order_controller.list_user_orders(usuario_id)
        return jsonify(body), status

    @bp.route("/pedidos/<int:pedido_id>/status", methods=["PUT"])
    def atualizar_status_pedido(pedido_id):
        body, status = order_controller.update_order_status(pedido_id, request.get_json())
        return jsonify(body), status

    @bp.route("/relatorios/vendas", methods=["GET"])
    def relatorio_vendas():
        body, status = order_controller.get_sales_report()
        return jsonify(body), status

    return bp
