import requests
from telegram.ext import CommandHandler

CLOUDFLARE_API_TOKEN = "YOUR_CLOUDFLARE_API_TOKEN"
CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/"

def clear_cache(update, context):
    try:
        args = context.args
        if len(args) < 1:
            update.message.reply_text("用法：/clear_cache <zone_id>")
            return

        zone_id = args[0]
        url = f"{CLOUDFLARE_API_URL}zones/{zone_id}/purge_cache"
        headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
        data = {"purge_everything": True}

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            update.message.reply_text("缓存已成功清除！")
        else:
            update.message.reply_text(f"清除缓存失败：{response.json().get('errors')}")
    except Exception as e:
        update.message.reply_text(f"错误：{str(e)}")

clear_cache_handler = CommandHandler('clear_cache', clear_cache)