from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler
import os
import modules.module1  # 导入模块 1
import modules.module2  # 导入模块 2

app = Flask(__name__)

# 获取 Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("环境变量 BOT_TOKEN 未设置！")

# 初始化 Telegram Bot Application
bot_application = Application.builder().token(BOT_TOKEN).build()

# 定义 /start 命令的处理函数
def start(update, context):
    update.message.reply_text("欢迎使用模块化 Telegram Bot！")

# 注册命令处理器
bot_application.add_handler(CommandHandler("start", start))
bot_application.add_handler(modules.module1.handler)  # 注册模块 1 的处理器
bot_application.add_handler(modules.module2.handler)  # 注册模块 2 的处理器

# Webhook 路由
@app.route('/webhook', methods=['POST'])
def webhook():
    """接收 Telegram Webhook 请求并处理"""
    update = Update.de_json(request.get_json(), bot_application.bot)
    bot_application.update_queue.put(update)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))