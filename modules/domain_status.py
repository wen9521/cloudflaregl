import requests
from telegram.ext import CommandHandler

def check_domain_status(update, context):
    try:
        args = context.args
        if len(args) < 1:
            update.message.reply_text("Usage: /check_domain_status <domain>")
            return

        domain = args[0]
        url = f"{CLOUDFLARE_API_URL}zones?name={domain}"
        headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            result = response.json().get("result", [])
            if result:
                status = result[0].get("status", "unknown")
                update.message.reply_text(f"Domain {domain} is {status}.")
            else:
                update.message.reply_text(f"No information found for domain {domain}.")
        else:
            update.message.reply_text(f"Failed to check domain status: {response.json().get('errors')}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

check_domain_status_handler = CommandHandler('check_domain_status', check_domain_status)