import requests
from telegram.ext import CommandHandler

def delete_dns(update, context):
    try:
        args = context.args
        if len(args) < 1:
            update.message.reply_text("Usage: /delete_dns <record_id>")
            return

        record_id = args[0]
        zone_id = "YOUR_CLOUDFLARE_ZONE_ID"

        url = f"{CLOUDFLARE_API_URL}zones/{zone_id}/dns_records/{record_id}"
        headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}

        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            update.message.reply_text(f"DNS record deleted: {record_id}")
        else:
            update.message.reply_text(f"Failed to delete DNS record: {response.json().get('errors')}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

handler = CommandHandler('delete_dns', delete_dns)