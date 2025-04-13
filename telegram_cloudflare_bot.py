import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# 从环境变量中获取 API Token 和 Zone ID
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")
AUTHORIZED_USERS = os.getenv("AUTHORIZED_USERS", "").split(",")  # 通过环境变量设置授权用户的 Telegram ID

# 检查用户权限
def restricted(func):
    def wrapper(update: Update, context: CallbackContext):
        user_id = str(update.effective_user.id)
        if user_id not in AUTHORIZED_USERS:
            update.message.reply_text("You are not authorized to use this bot.")
            return
        return func(update, context)
    return wrapper

# 清理 Cloudflare 缓存
@restricted
def clear_cache(update: Update, context: CallbackContext) -> None:
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/purge_cache"
    data = {"purge_everything": True}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        update.message.reply_text("Cache cleared successfully!")
    else:
        update.message.reply_text(f"Failed to clear cache: {response.text}")

# 添加 Cloudflare DNS 记录
@restricted
def add_dns(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 3:
        update.message.reply_text("Usage: /add_dns <type> <name> <content>")
        return

    record_type = context.args[0]
    record_name = context.args[1]
    record_content = context.args[2]

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
    data = {
        "type": record_type,
        "name": record_name,
        "content": record_content,
        "ttl": 1
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        update.message.reply_text("DNS record added successfully!")
    else:
        update.message.reply_text(f"Failed to add DNS record: {response.text}")

# 查询 Cloudflare DNS 记录
@restricted
def get_dns(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 1:
        update.message.reply_text("Usage: /get_dns <name>")
        return

    record_name = context.args[0]

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
    }
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records?name={record_name}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        records = response.json().get("result", [])
        if records:
            message = "\n".join(
                [f"{r['type']} {r['name']} -> {r['content']}" for r in records]
            )
            update.message.reply_text(message)
        else:
            update.message.reply_text("No DNS records found.")
    else:
        update.message.reply_text(f"Failed to fetch DNS records: {response.text}")

# 启动命令
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I'm your Cloudflare manager bot.")

# 主函数
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)

    # 添加命令处理程序
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("clear_cache", clear_cache))
    updater.dispatcher.add_handler(CommandHandler("add_dns", add_dns))
    updater.dispatcher.add_handler(CommandHandler("get_dns", get_dns))

    # 启动 Bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()