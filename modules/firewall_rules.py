import requests
from telegram.ext import CommandHandler

def add_firewall_rule(update, context):
    try:
        args = context.args
        if len(args) < 3:
            update.message.reply_text("Usage: /add_firewall_rule <action> <field> <value>")
            return

        action, field, value = args[0], args[1], args[2]
        zone_id = "YOUR_CLOUDFLARE_ZONE_ID"

        url = f"{CLOUDFLARE_API_URL}zones/{zone_id}/firewall/rules"
        headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
        data = {
            "action": action,
            "filter": {
                "expression": f"{field} eq {value}"
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            update.message.reply_text(f"Firewall rule added: {action} {field} {value}")
        else:
            update.message.reply_text(f"Failed to add firewall rule: {response.json().get('errors')}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

handler = CommandHandler('add_firewall_rule', add_firewall_rule)