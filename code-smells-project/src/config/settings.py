import os


class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-in-production")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    DATABASE_PATH = os.getenv("DATABASE_PATH", "loja.db")
    PORT = int(os.getenv("PORT", "5000"))
    HOST = os.getenv("HOST", "0.0.0.0")

    # Business constants
    VALID_CATEGORIES = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]
    VALID_ORDER_STATUSES = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]
    DISCOUNT_TIERS = [
        (10000, 0.10),
        (5000, 0.05),
        (1000, 0.02),
    ]
