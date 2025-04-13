import requests
from telegram.ext import CommandHandler

CLOUDFLARE_API_TOKEN = "YOUR_CLOUDFLARE_API_TOKEN"
CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/"

def add_waf_rule(update, context):
    try:
        args = context.args
        if len(args) < 3:
            update.message.reply_text("用法：/add_waf_rule <action> <field> <value>")
            return

        action = args[0]
        field = args[1]
        value = args[2]

        url = f"{CLOUDFLARE_API_URL}zones/YOUR_ZONE_ID/firewall/rules"
        headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
        data = {
            "action": action,
            "filter": {
                "expression": f"{field} eq \"{value}\""
            },
            "description": "Added via Telegram Bot"
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            update.message.reply_text("WAF 规则已成功添加！")
        else:
            update.message.reply_text(f"WAF 规则添加失败：{response.json().get('errors')}")
    except Exception as e:
        update.message.reply_text(f"错误：{str(e)}")

add_waf_handler = CommandHandler('add_waf_rule', add_waf_rule)