import os

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    ADMIN_ID = int(os.getenv("ADMIN_ID"))
    DATABASE_URL = os.getenv("DATABASE_URL", "nodes.db")