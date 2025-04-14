from flask import Flask, request, jsonify
from telegram.ext import ApplicationBuilder, CommandHandler
import asyncio
import os

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
@flask_app.route(f"/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        # Ensure async handling of Telegram updates
        update_data = request.get_json()
        if update_data:
            await telegram_app.update_queue.put(update_data)
        return "OK", 200
    return jsonify({"error": "Invalid request method"}), 405

# Configure webhook during initialization
async def configure_webhook():
    webhook_url = f"https://<YOUR_SERVICE_URL>/webhook"
    await telegram_app.bot.set_webhook(webhook_url)

# WSGI Entry Point
def wsgi(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"Service is live."]

if __name__ == "__main__":
    # Run Flask app with Hypercorn for async support
    import hypercorn.asyncio
    from hypercorn.config import Config

    async def main():
        # Configure Telegram webhook
        await configure_webhook()

        # Start Flask app
        config = Config()
        config.bind = ["0.0.0.0:10000"]
        await hypercorn.asyncio.serve(flask_app, config)

    asyncio.run(main())
