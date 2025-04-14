from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.cloudflare import CloudflareManager
from config.settings import CLOUDFLARE_API_KEY, CLOUDFLARE_EMAIL

cf_manager = CloudflareManager(api_key=CLOUDFLARE_API_KEY, email=CLOUDFLARE_EMAIL)

async def list_zones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        zones = cf_manager.list_zones()
        response = "\n".join([f"{zone['name']} (ID: {zone['id']})" for zone in zones])
        await update.message.reply_text(f"Cloudflare Zones:\n{response}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")