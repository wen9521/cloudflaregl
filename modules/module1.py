from telegram.ext import CommandHandler

# 定义模块 1 功能的处理函数
def module1_command(update, context):
    update.message.reply_text("这是模块 1 的功能！")

# 创建模块 1 的命令处理器
handler = CommandHandler("module1", module1_command)