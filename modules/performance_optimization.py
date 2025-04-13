import requests
from telegram.ext import CommandHandler

CLOUDFLARE_API_TOKEN = "YOUR_CLOUDFLARE_API_TOKEN"
CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/"

def toggle_brotli(update, context):
    try:
        args = context.args
        if len(args) < 2:
            update.message.reply_text("Usage: /toggle_brotli <zone_id> <on|off>")
            return

        zone_id, state = args[0], args[1]
        url = f"{CLOUDFLARE_API_URL}zones/{zone_id}/settings/brotli"
        headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
        data = {"value": "on" if state.lower() == "on" else "off"}

        response = requests.patch(url, headers=headers, json=data)

        if response.status_code == 200:
            update.message.reply_text(f"Brotli compression toggled {state}.")
        else:
            update.message.reply_text(f"Failed to toggle Brotli: {response.json().get('errors')}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

toggle_brotli_handler = CommandHandler('toggle_brotli', toggle_brotli)