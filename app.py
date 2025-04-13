from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler
import modules.module1  # 导入自定义模块
import modules.module2  # 导入自定义模块

app = Flask(__name__)

# 初始化 Telegram Bot
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot_application = Application.builder().token(BOT_TOKEN).build()

# 定义 /start 命令的处理函数
def start(update, context):
    update.message.reply_text("欢迎使用模块化 Telegram Bot！")

# 注册命令处理器
bot_application.add_handler(CommandHandler("start", start))
bot_application.add_handler(modules.module1.handler)  # 自定义模块的 handler
bot_application.add_handler(modules.module2.handler)  # 自定义模块的 handler

# Webhook 路由
@app.route('/webhook', methods=['POST'])
def webhook():
    """接收 Telegram Webhook 请求并处理"""
    update = Update.de_json(request.get_json(), bot_application.bot)
    bot_application.update_queue.put(update)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)