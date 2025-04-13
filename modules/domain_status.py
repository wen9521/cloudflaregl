import requests
from telegram.ext import CommandHandler

def check_domain_status(update, context):
    try:
        args = context.args
        if len(args) < 1:
            update.message.reply_text("用法：/check_domain_status <domain>")
            return

        domain = args[0]
        url = f"https://api.cloudflare.com/client/v4/zones?name={domain}"
        headers = {"Authorization": f"Bearer YOUR_CLOUDFLARE_API_TOKEN"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()["result"]
            if result:
                update.message.reply_text(f"域名 {domain} 状态：正常")
            else:
                update.message.reply_text(f"域名 {domain} 未找到或无效。")
        else:
            update.message.reply_text(f"检查域名状态失败：{response.json().get('errors')}")
    except Exception as e:
        update.message.reply_text(f"错误：{str(e)}")

check_domain_status_handler = CommandHandler('check_domain_status', check_domain_status)