from telegram.ext import CommandHandler

# 定义模块 2 功能的处理函数
def module2_command(update, context):
    update.message.reply_text("这是模块 2 的功能！")

# 创建模块 2 的命令处理器
handler = CommandHandler("module2", module2_command)