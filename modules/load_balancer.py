import requests
from telegram.ext import CommandHandler

CLOUDFLARE_API_TOKEN = "YOUR_CLOUDFLARE_API_TOKEN"
CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/"

def create_load_balancer(update, context):
    try:
        args = context.args
        if len(args) < 3:
            update.message.reply_text("Usage: /create_load_balancer <name> <origin> <default_pool>")
            return

        name, origin, default_pool = args[0], args[1], args[2]
        zone_id = "YOUR_CLOUDFLARE_ZONE_ID"

        url = f"{CLOUDFLARE_API_URL}zones/{zone_id}/load_balancers"
        headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
        data = {
            "name": name,
            "origin": origin,
            "default_pool": default_pool
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            update.message.reply_text(f"Load balancer {name} created successfully!")
        else:
            update.message.reply_text(f"Failed to create load balancer: {response.json().get('errors')}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

create_load_balancer_handler = CommandHandler('create_load_balancer', create_load_balancer)