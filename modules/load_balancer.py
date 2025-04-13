import requests
from telegram.ext import CommandHandler

CLOUDFLARE_API_TOKEN = "YOUR_CLOUDFLARE_API_TOKEN"
CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/"

def create_load_balancer(update, context):
    try:
        args = context.args
        if len(args) < 3:
            update.message.reply_text("用法：/create_load_balancer <name> <origin> <default_pool>")
            return

        name = args[0]
        origin = args[1]
        default_pool = args[2]

        url = f"{CLOUDFLARE_API_URL}zones/YOUR_ZONE_ID/load_balancers"
        headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
        data = {
            "name": name,
            "origins": [{"name": origin, "address": origin, "enabled": True}],
            "default_pool_ids": [default_pool]
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            update.message.reply_text("负载均衡已成功创建！")
        else:
            update.message.reply_text(f"创建负载均衡失败：{response.json().get('errors')}")
    except Exception as e:
        update.message.reply_text(f"错误：{str(e)}")

create_load_balancer_handler = CommandHandler('create_load_balancer', create_load_balancer)