import requests
from telegram.ext import CommandHandler

CLOUDFLARE_API_TOKEN = "YOUR_CLOUDFLARE_API_TOKEN"
CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/"

def create_dns(update, context):
    try:
        # Parse arguments: record type, name, content
        args = context.args
        if len(args) < 3:
            update.message.reply_text("Usage: /create_dns <type> <name> <content>")
            return

        record_type, name, content = args[0], args[1], args[2]
        zone_id = "YOUR_CLOUDFLARE_ZONE_ID"  # Replace with your Zone ID

        # API call to create DNS record
        url = f"{CLOUDFLARE_API_URL}zones/{zone_id}/dns_records"
        headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
        data = {
            "type": record_type.upper(),
            "name": name,
            "content": content,
            "ttl": 1,
            "proxied": False
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            update.message.reply_text(f"DNS record created: {name} ({record_type}) -> {content}")
        else:
            update.message.reply_text(f"Failed to create DNS record: {response.json().get('errors')}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

handler = CommandHandler('create_dns', create_dns)