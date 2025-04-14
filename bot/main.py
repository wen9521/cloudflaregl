from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers.zones import list_zones
from bot.handlers.cache import purge_cache
from config.settings import TELEGRAM_BOT_TOKEN

# Define a WSGI-compatible function
def create_app():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("list_zones", list_zones))
    application.add_handler(CommandHandler("purge_cache", purge_cache))
    
    return application

# WSGI application for Gunicorn
def wsgi(environ, start_response):
    app = create_app()
    app.run_polling()
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"Telegram Bot is running."]
