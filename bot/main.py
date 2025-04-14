from flask import Flask, request, jsonify
from telegram.ext import ApplicationBuilder, CommandHandler

from bot.handlers.zones import list_zones
from bot.handlers.cache import purge_cache
from config.settings import TELEGRAM_BOT_TOKEN

# Flask app for webhook handling
flask_app = Flask(__name__)

# Create Telegram Bot application
def create_app():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("list_zones", list_zones))
    application.add_handler(CommandHandler("purge_cache", purge_cache))

    return application

telegram_app = create_app()

# Root endpoint for service status
@flask_app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Service is live 🎉", "description": "Telegram Bot is running!"}), 200

# Webhook route for Telegram
@flask_app.route(f"/webhook/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        telegram_app.update_queue.put(request.get_json())
        return "OK", 200

# WSGI Entry Point
def wsgi(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"Service is live."]
