from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.cloudflare import CloudflareManager
from config.settings import CLOUDFLARE_API_KEY, CLOUDFLARE_EMAIL

cf_manager = CloudflareManager(api_key=CLOUDFLARE_API_KEY, email=CLOUDFLARE_EMAIL)

async def purge_cache(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        zone_id = context.args[0]
        cf_manager.purge_cache(zone_id)
        await update.message.reply_text(f"Cache purged for Zone ID: {zone_id}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")