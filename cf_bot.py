import os
import re
import subprocess
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler
)
from CloudFlare import CloudFlare

# 加载环境变量
load_dotenv()

# 配置参数
CF_API_KEY = os.getenv('CF_API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
ALLOWED_COMMANDS = ['ls -l', 'df -h', 'uptime', 'date']
SAFE_WORK_DIR = '/tmp'
CMD_TIMEOUT = 5

# 初始化 Cloudflare
cf = CloudFlare(token=CF_API_KEY)

# 会话状态
MENU, SHELL_CMD, DNS_MGMT = range(3)

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 自定义键盘
main_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton("📡 DNS管理"), KeyboardButton("🔒 SSL设置")],
    [KeyboardButton("🛡️ 防火墙"), KeyboardButton("🧹 缓存清理")],
    [KeyboardButton("💻 终端"), KeyboardButton("🚪 退出")]
], resize_keyboard=True)

def auth_required(func):
    """增强型权限验证装饰器"""
    def wrapper(update: Update, context: CallbackContext):
        if update.effective_user.id != ADMIN_ID:
            update.message.reply_text("⛔ 未授权访问！事件已记录。")
            log_security_event(f"未授权访问尝试 from {update.effective_user.id}")
            return ConversationHandler.END
        return func(update, context)
    return wrapper

def log_security_event(event: str):
    """安全事件日志记录"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("audit.log", "a") as f:
        f.write(f"[SECURITY] {timestamp} - {event}\n")

def log_operation(action: str):
    """操作审计日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("audit.log", "a") as f:
        f.write(f"[OPERATION] {timestamp} - {action}\n")

# 命令处理函数
@auth_required
def start(update: Update, context: CallbackContext):
    update.message.reply_markdown_v2(
        "🔐 *Cloudflare 综合管理平台* 🔐\n"
        "**版本**: 2\.0 \(安全加固版\)\n"
        "**最后更新**: 2023\-08\-20",
        reply_markup=main_keyboard
    )
    return MENU

# DNS 管理功能
@auth_required
def dns_management(update: Update, context: CallbackContext):
    try:
        zones = cf.zones.get(params={'per_page': 50})
        buttons = [[KeyboardButton(zone['name'])] for zone in zones]
        buttons.append([KeyboardButton("↩️ 返回主菜单")])
        update.message.reply_text(
            "🌐 选择要管理的域名：",
            reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        )
        return DNS_MGMT
    except Exception as e:
        handle_error(update, e, "获取域名列表失败")

def handle_dns_actions(update: Update, context: CallbackContext):
    selected_zone = update.message.text
    if selected_zone == "↩️ 返回主菜单":
        return start(update, context)
    
    try:
        zone_id = cf.zones.get(params={'name': selected_zone})[0]['id']
        records = cf.zones.dns_records.get(zone_id)
        
        # 显示记录管理选项
        context.user_data['current_zone'] = zone_id
        update.message.reply_text(
            f"📡 正在管理 {selected_zone}\n"
            "可用操作：\n"
            "/add_record [类型] [名称] [内容]\n"
            "/del_record [记录ID]\n"
            "/list_records\n"
            "↩️ 返回域名列表",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("↩️ 返回域名列表")]], resize_keyboard=True)
        )
        return ConversationHandler.END
    except Exception as e:
        handle_error(update, e, "域名解析失败")

# Shell 功能（安全增强版）
@auth_required
def secure_shell(update: Update, context: CallbackContext):
    allowed_commands = '\n'.join(ALLOWED_COMMANDS)
    update.message.reply_text(
        f"⚠️ 安全终端模式（5秒超时）\n允许命令：\n{allowed_commands}",
        reply_markup=ReplyKeyboardRemove()
    )
    return SHELL_CMD

def validate_command(cmd: str) -> bool:
    """增强型命令验证"""
    allowed_patterns = [
        r'^ls -l$',
        r'^df -h$',
        r'^uptime$',
        r'^date$'
    ]
    return any(re.fullmatch(pattern, cmd) for pattern in allowed_patterns)

@auth_required
def execute_command(update: Update, context: CallbackContext):
    cmd = update.message.text.strip()
    
    if not validate_command(cmd):
        log_security_event(f"非法命令尝试: {cmd}")
        update.message.reply_text("❌ 命令未授权！")
        return MENU

    try:
        log_operation(f"执行命令: {cmd}")
        result = subprocess.run(
            cmd.split(),
            cwd=SAFE_WORK_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=CMD_TIMEOUT,
            check=True
        )
        output = (result.stdout.decode() or result.stderr.decode())[:1500]
        update.message.reply_text(f"🖥️ 执行结果：\n```\n{output}\n```", parse_mode=ParseMode.MARKDOWN_V2)
    except Exception as e:
        handle_error(update, e, "命令执行失败")
    
    return start(update, context)

def handle_error(update: Update, error: Exception, context_msg: str):
    """统一错误处理"""
    logger.error(f"{context_msg}: {str(error)}")
    error_msg = f"🚨 {context_msg}：\n`{str(error)}`"
    update.message.reply_text(error_msg, parse_mode=ParseMode.MARKDOWN_V2)
    log_security_event(f"系统错误: {context_msg} - {str(error)}")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                MessageHandler(Filters.regex('^📡 DNS管理$'), dns_management),
                MessageHandler(Filters.regex('^💻 终端$'), secure_shell),
                # 其他功能处理...
            ],
            DNS_MGMT: [
                MessageHandler(Filters.text & ~Filters.command, handle_dns_actions)
            ],
            SHELL_CMD: [
                MessageHandler(Filters.text & ~Filters.command, execute_command)
            ]
        },
        fallbacks=[CommandHandler('cancel', start)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    logger.info("Bot 已启动，进入监听状态...")
    updater.idle()

if __name__ == '__main__':
    main()
