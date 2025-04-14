from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers.zones import list_zones
from bot.handlers.cache import purge_cache
from config.settings import TELEGRAM_BOT_TOKEN

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("list_zones", list_zones))
    application.add_handler(CommandHandler("purge_cache", purge_cache))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()