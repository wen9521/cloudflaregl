from flask import Flask, request
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup
from modules.subscription_converter import convert_subscription_handler
from modules.cache_management import clear_cache_handler
from modules.waf_rules import add_waf_handler
from modules.domain_status import check_domain_status_handler
from modules.load_balancer import create_load_balancer_handler
from modules.performance_optimization import toggle_brotli_handler

app = Flask(__name__)

# 初始化 Telegram Bot 应用
bot_application = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

# 命令：开始（带自定义键盘）
def start(update, context):
    keyboard = [
        ["订阅转换", "清除缓存"],
        ["添加 WAF 规则", "检查域名状态"],
        ["创建负载均衡", "切换 Brotli 压缩"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("欢迎使用 Cloudflare 管理机器人！请选择一个功能：", reply_markup=reply_markup)

start_handler = CommandHandler('start', start)
bot_application.add_handler(start_handler)

# 处理菜单选项
def handle_menu(update, context):
    text = update.message.text
    if text == "订阅转换":
        update.message.reply_text("请使用 /convert_subscription 命令来进行订阅转换。")
    elif text == "清除缓存":
        update.message.reply_text("请使用 /clear_cache <zone_id> 命令来清除缓存。")
    elif text == "添加 WAF 规则":
        update.message.reply_text("请使用 /add_waf_rule <action> <field> <value> 命令来添加 WAF 规则。")
    elif text == "检查域名状态":
        update.message.reply_text("请使用 /check_domain_status <domain> 命令来检查域名状态。")
    elif text == "创建负载均衡":
        update.message.reply_text("请使用 /create_load_balancer <name> <origin> <default_pool> 命令来创建负载均衡。")
    elif text == "切换 Brotli 压缩":
        update.message.reply_text("请使用 /toggle_brotli <zone_id> <on|off> 命令来切换 Brotli 压缩。")
    else:
        update.message.reply_text("无效选项，请使用菜单中的功能按钮。")

menu_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)
bot_application.add_handler(menu_handler)

# 添加其他命令处理程序
bot_application.add_handler(convert_subscription_handler)
bot_application.add_handler(clear_cache_handler)
bot_application.add_handler(add_waf_handler)
bot_application.add_handler(check_domain_status_handler)
bot_application.add_handler(create_load_balancer_handler)
bot_application.add_handler(toggle_brotli_handler)

@app.route('/')
def index():
    return "Cloudflare 管理机器人正在运行！"

@app.route('/webhook', methods=['POST'])
def webhook():
    # 处理传入的更新
    update = request.get_json()
    bot_application.update_queue.put(update)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)