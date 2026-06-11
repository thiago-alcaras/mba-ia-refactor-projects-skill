import logging
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class OrderModel:
    def __init__(self, db):
        self.db = db

    def create(self, usuario_id, itens):
        cursor = self.db.cursor()
        total = 0

        for item in itens:
            cursor.execute("SELECT * FROM produtos WHERE id = ?", (item["produto_id"],))
            produto = cursor.fetchone()
            if produto is None:
                return {"erro": f"Produto {item['produto_id']} não encontrado"}
            if produto["estoque"] < item["quantidade"]:
                return {"erro": f"Estoque insuficiente para {produto['nome']}"}
            total += produto["preco"] * item["quantidade"]

        cursor.execute(
            "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
            (usuario_id, total)
        )
        pedido_id = cursor.lastrowid

        for item in itens:
            cursor.execute("SELECT preco FROM produtos WHERE id = ?", (item["produto_id"],))
            produto = cursor.fetchone()
            cursor.execute(
                "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                (pedido_id, item["produto_id"], item["quantidade"], produto["preco"])
            )
            cursor.execute(
                "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                (item["quantidade"], item["produto_id"])
            )

        self.db.commit()
        logger.info("Order created", extra={"pedido_id": pedido_id, "total": total})
        return {"pedido_id": pedido_id, "total": total}

    def get_by_user(self, usuario_id):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT p.*, i.produto_id, i.quantidade, i.preco_unitario, pr.nome as produto_nome
            FROM pedidos p
            LEFT JOIN itens_pedido i ON i.pedido_id = p.id
            LEFT JOIN produtos pr ON pr.id = i.produto_id
            WHERE p.usuario_id = ?
            ORDER BY p.id
        """, (usuario_id,))
        return self._group_orders(cursor.fetchall())

    def get_all(self):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT p.*, i.produto_id, i.quantidade, i.preco_unitario, pr.nome as produto_nome
            FROM pedidos p
            LEFT JOIN itens_pedido i ON i.pedido_id = p.id
            LEFT JOIN produtos pr ON pr.id = i.produto_id
            ORDER BY p.id
        """)
        return self._group_orders(cursor.fetchall())

    def update_status(self, pedido_id, novo_status):
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE pedidos SET status = ? WHERE id = ?",
            (novo_status, pedido_id)
        )
        self.db.commit()
        return True

    def get_sales_report(self):
        cursor = self.db.cursor()

        cursor.execute("SELECT COUNT(*) as total FROM pedidos")
        total_pedidos = cursor.fetchone()["total"]

        cursor.execute("SELECT COALESCE(SUM(total), 0) as sum FROM pedidos")
        faturamento = cursor.fetchone()["sum"]

        cursor.execute("SELECT COUNT(*) as c FROM pedidos WHERE status = 'pendente'")
        pendentes = cursor.fetchone()["c"]

        cursor.execute("SELECT COUNT(*) as c FROM pedidos WHERE status = 'aprovado'")
        aprovados = cursor.fetchone()["c"]

        cursor.execute("SELECT COUNT(*) as c FROM pedidos WHERE status = 'cancelado'")
        cancelados = cursor.fetchone()["c"]

        desconto = 0
        for threshold, rate in Settings.DISCOUNT_TIERS:
            if faturamento > threshold:
                desconto = faturamento * rate
                break

        return {
            "total_pedidos": total_pedidos,
            "faturamento_bruto": round(faturamento, 2),
            "desconto_aplicavel": round(desconto, 2),
            "faturamento_liquido": round(faturamento - desconto, 2),
            "pedidos_pendentes": pendentes,
            "pedidos_aprovados": aprovados,
            "pedidos_cancelados": cancelados,
            "ticket_medio": round(faturamento / total_pedidos, 2) if total_pedidos > 0 else 0,
        }

    def _group_orders(self, rows):
        orders = {}
        for row in rows:
            row = dict(row)
            pedido_id = row["id"]
            if pedido_id not in orders:
                orders[pedido_id] = {
                    "id": row["id"],
                    "usuario_id": row["usuario_id"],
                    "status": row["status"],
                    "total": row["total"],
                    "criado_em": row["criado_em"],
                    "itens": [],
                }
            if row.get("produto_id"):
                orders[pedido_id]["itens"].append({
                    "produto_id": row["produto_id"],
                    "produto_nome": row.get("produto_nome", "Desconhecido"),
                    "quantidade": row["quantidade"],
                    "preco_unitario": row["preco_unitario"],
                })
        return list(orders.values())
