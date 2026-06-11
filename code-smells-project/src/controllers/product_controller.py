import logging
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class ProductController:
    def __init__(self, product_model):
        self.product_model = product_model

    def list_products(self):
        produtos = self.product_model.get_all()
        return {"dados": produtos, "sucesso": True}, 200

    def get_product(self, product_id):
        produto = self.product_model.get_by_id(product_id)
        if produto:
            return {"dados": produto, "sucesso": True}, 200
        return {"erro": "Produto não encontrado", "sucesso": False}, 404

    def create_product(self, dados):
        if not dados:
            return {"erro": "Dados inválidos"}, 400
        if "nome" not in dados:
            return {"erro": "Nome é obrigatório"}, 400
        if "preco" not in dados:
            return {"erro": "Preço é obrigatório"}, 400
        if "estoque" not in dados:
            return {"erro": "Estoque é obrigatório"}, 400

        nome = dados["nome"]
        descricao = dados.get("descricao", "")
        preco = dados["preco"]
        estoque = dados["estoque"]
        categoria = dados.get("categoria", "geral")

        if preco < 0:
            return {"erro": "Preço não pode ser negativo"}, 400
        if estoque < 0:
            return {"erro": "Estoque não pode ser negativo"}, 400
        if len(nome) < 2:
            return {"erro": "Nome muito curto"}, 400
        if len(nome) > 200:
            return {"erro": "Nome muito longo"}, 400
        if categoria not in Settings.VALID_CATEGORIES:
            return {"erro": f"Categoria inválida. Válidas: {Settings.VALID_CATEGORIES}"}, 400

        product_id = self.product_model.create(nome, descricao, preco, estoque, categoria)
        logger.info("Product created", extra={"product_id": product_id})
        return {"dados": {"id": product_id}, "sucesso": True, "mensagem": "Produto criado"}, 201

    def update_product(self, product_id, dados):
        produto_existente = self.product_model.get_by_id(product_id)
        if not produto_existente:
            return {"erro": "Produto não encontrado"}, 404

        if not dados:
            return {"erro": "Dados inválidos"}, 400
        if "nome" not in dados:
            return {"erro": "Nome é obrigatório"}, 400
        if "preco" not in dados:
            return {"erro": "Preço é obrigatório"}, 400
        if "estoque" not in dados:
            return {"erro": "Estoque é obrigatório"}, 400

        nome = dados["nome"]
        descricao = dados.get("descricao", "")
        preco = dados["preco"]
        estoque = dados["estoque"]
        categoria = dados.get("categoria", "geral")

        if preco < 0:
            return {"erro": "Preço não pode ser negativo"}, 400
        if estoque < 0:
            return {"erro": "Estoque não pode ser negativo"}, 400

        self.product_model.update(product_id, nome, descricao, preco, estoque, categoria)
        return {"sucesso": True, "mensagem": "Produto atualizado"}, 200

    def delete_product(self, product_id):
        produto = self.product_model.get_by_id(product_id)
        if not produto:
            return {"erro": "Produto não encontrado"}, 404
        self.product_model.delete(product_id)
        logger.info("Product deleted", extra={"product_id": product_id})
        return {"sucesso": True, "mensagem": "Produto deletado"}, 200

    def search_products(self, termo, categoria, preco_min, preco_max):
        resultados = self.product_model.search(termo, categoria, preco_min, preco_max)
        return {"dados": resultados, "total": len(resultados), "sucesso": True}, 200
