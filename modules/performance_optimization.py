import requests
from telegram.ext import CommandHandler

CLOUDFLARE_API_TOKEN = "YOUR_CLOUDFLARE_API_TOKEN"
CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/"

def toggle_brotli(update, context):
    try:
        args = context.args
        if len(args) < 2:
            update.message.reply_text("用法：/toggle_brotli <zone_id> <on|off>")
            return

        zone_id = args[0]
        status = args[1].lower()

        if status not in ["on", "off"]:
            update.message.reply_text("无效参数，请使用 'on' 或 'off'")
            return

        url = f"{CLOUDFLARE_API_URL}zones/{zone_id}/settings/brotli"
        headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
        data = {"value": status}

        response = requests.patch(url, headers=headers, json=data)

        if response.status_code == 200:
            update.message.reply_text(f"Brotli 压缩已成功切换为：{status}")
        else:
            update.message.reply_text(f"切换 Brotli 压缩失败：{response.json().get('errors')}")
    except Exception as e:
        update.message.reply_text(f"错误：{str(e)}")

toggle_brotli_handler = CommandHandler('toggle_brotli', toggle_brotli)