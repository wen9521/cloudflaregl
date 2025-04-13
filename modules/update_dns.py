import requests
from telegram.ext import CommandHandler

def update_dns(update, context):
    try:
        args = context.args
        if len(args) < 4:
            update.message.reply_text("Usage: /update_dns <record_id> <type> <name> <content>")
            return

        record_id, record_type, name, content = args[0], args[1], args[2], args[3]
        zone_id = "YOUR_CLOUDFLARE_ZONE_ID"

        url = f"{CLOUDFLARE_API_URL}zones/{zone_id}/dns_records/{record_id}"
        headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
        data = {
            "type": record_type.upper(),
            "name": name,
            "content": content,
            "ttl": 1,
            "proxied": False
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code == 200:
            update.message.reply_text(f"DNS record updated: {name} ({record_type}) -> {content}")
        else:
            update.message.reply_text(f"Failed to update DNS record: {response.json().get('errors')}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

handler = CommandHandler('update_dns', update_dns)