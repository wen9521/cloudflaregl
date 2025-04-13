import requests
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

# 会话状态
SELECT_FORMAT, INPUT_LINK = range(2)

# 第一步：询问用户目标格式
def start_conversion(update, context):
    keyboard = [["Clash", "Quantumult"], ["Surge"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("请选择订阅转换的目标格式：", reply_markup=reply_markup)
    return SELECT_FORMAT

# 第二步：询问用户订阅链接
def select_format(update, context):
    context.user_data['format'] = update.message.text
    update.message.reply_text("请发送订阅链接：", reply_markup=ReplyKeyboardRemove())
    return INPUT_LINK

# 第三步：执行订阅转换
def convert_subscription(update, context):
    subscription_link = update.message.text
    target_format = context.user_data.get('format')

    try:
        # 模拟转换逻辑
        converted_link = simulate_conversion(subscription_link, target_format)
        update.message.reply_text(f"您的转换后的订阅链接为：\n{converted_link}")
    except Exception as e:
        update.message.reply_text(f"转换过程中发生错误：{e}")
    return ConversationHandler.END

# 模拟转换逻辑
def simulate_conversion(link, target_format):
    # 根据目标格式模拟转换
    if target_format == "Clash":
        return f"{link}?format=clash"
    elif target_format == "Quantumult":
        return f"{link}?format=quantumult"
    elif target_format == "Surge":
        return f"{link}?format=surge"
    else:
        raise ValueError("不支持的格式！")

# 取消会话
def cancel(update, context):
    update.message.reply_text("已取消订阅转换操作。", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# 定义会话处理程序
convert_subscription_handler = ConversationHandler(
    entry_points=[CommandHandler('convert_subscription', start_conversion)],
    states={
        SELECT_FORMAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_format)],
        INPUT_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, convert_subscription)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)