import requests
from telegram.ext import CommandHandler

CLOUDFLARE_API_TOKEN = "YOUR_CLOUDFLARE_API_TOKEN"
CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/"

def list_dns(update, context):
    zone_id = "YOUR_CLOUDFLARE_ZONE_ID"  # Replace with your Cloudflare Zone ID
    url = f"{CLOUDFLARE_API_URL}zones/{zone_id}/dns_records"
    headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.ok:
        records = response.json()["result"]
        message = "\n".join([f"{record['name']} - {record['type']} - {record['content']}" for record in records])
    else:
        message = "Failed to fetch DNS records."
    
    update.message.reply_text(message)

handler = CommandHandler('list_dns', list_dns)