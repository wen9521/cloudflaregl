import os
import fcntl
import logging
import asyncio  # Ensure asyncio is imported
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters
)
from CloudFlare import CloudFlare

# --- 初始化阶段 ---
# 加载环境变量
load_dotenv()

# 确保日志目录存在
os.makedirs('logs', exist_ok=True)

# 进程锁保障单实例
lock_file = open('bot.lock', 'w')
try:
    fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    print("⚠️ 已有实例在运行！")
    exit(1)

# 配置参数
CF_API_KEY = os.getenv('CF_API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
ALLOWED_COMMANDS = ['ls -l', 'df -h', 'uptime', 'date']
SAFE_WORK_DIR = '/tmp/cf-bot'
CMD_TIMEOUT = 5

# 初始化 Cloudflare
cf = CloudFlare(token=CF_API_KEY)

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/runtime.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- 自定义键盘 ---
main_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton("📡 DNS管理"), KeyboardButton("🔒 SSL")],
    [KeyboardButton("🛡️ 防火墙"), KeyboardButton("🧹 缓存")],
    [KeyboardButton("💻 终端"), KeyboardButton("🚪 退出")]
], resize_keyboard=True)

# 会话状态
MENU, SHELL_CMD, DNS_MGMT = range(3)

def auth_required(func):
    """增强型权限验证装饰器"""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != ADMIN_ID:
            log_security(f"未授权访问尝试: {update.effective_user}")
            await update.message.reply_text("⛔ 权限拒绝！")
            return ConversationHandler.END
        return await func(update, context)
    return wrapper

# --- 日志系统 ---
def log_security(event: str):
    """安全事件记录"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('logs/audit.log', 'a') as f:
        f.write(f"[SECURITY] {timestamp} - {event}\n")

def log_operation(action: str):
    """操作审计记录"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('logs/audit.log', 'a') as f:
        f.write(f"[OPERATE] {timestamp} - {action}\n")

# --- 核心功能 ---
@auth_required
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """启动命令"""
    await update.message.reply_markdown_v2(
        "🔐 *Cloudflare 管理平台* 🔐\n"
        f"*服务器*: `{os.uname().nodename}`\n"
        f"*用户*: {update.effective_user.full_name}",
        reply_markup=main_keyboard
    )
    return MENU

# DNS管理模块
@auth_required
async def dns_management(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        zones = cf.zones.get(params={'per_page': 20})
        zone_btns = [[KeyboardButton(z['name'])] for z in zones]
        zone_btns.append([KeyboardButton("🔙 返回")])
        
        await update.message.reply_text(
            "🌐 选择域名：",
            reply_markup=ReplyKeyboardMarkup(zone_btns, resize_keyboard=True)
        )
        return DNS_MGMT
    except Exception as e:
        await handle_error(update, e, "获取域名失败")

# Shell终端模块
@auth_required
async def secure_shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """安全终端入口"""
    cmd_list = '\n'.join(ALLOWED_COMMANDS)
    await update.message.reply_text(
        f"⚠️ 安全终端模式（{CMD_TIMEOUT}秒超时）\n"
        f"允许命令：\n{cmd_list}",
        reply_markup=ReplyKeyboardRemove()
    )
    return SHELL_CMD

@auth_required
async def execute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """执行Shell命令"""
    cmd = update.message.text.strip()
    log_operation(f"执行命令: {cmd}")
    
    if cmd not in ALLOWED_COMMANDS:
        log_security(f"非法命令尝试: {cmd}")
        await update.message.reply_text("❌ 命令未授权！")
        return MENU

    try:
        os.makedirs(SAFE_WORK_DIR, exist_ok=True)
        result = subprocess.run(
            cmd.split(),
            cwd=SAFE_WORK_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=CMD_TIMEOUT,
            check=True
        )
        output = (result.stdout.decode() or result.stderr.decode())[:1500]
        await update.message.reply_text(f"🖥️ 执行结果：\n```\n{output}\n```",
                                        parse_mode='MarkdownV2')
    except subprocess.TimeoutExpired:
        await update.message.reply_text("⏳ 命令执行超时！")
    except Exception as e:
        await handle_error(update, e, "命令执行失败")
    
    return await start(update, context)

# --- 辅助函数 ---
async def handle_error(update: Update, error: Exception, context: str):
    """统一错误处理"""
    err_msg = f"🚨 {context}：`{str(error)}`"
    logger.error(err_msg)
    await update.message.reply_text(err_msg, parse_mode='MarkdownV2')
    log_security(f"系统错误 - {context}")

def cleanup():
    """退出清理"""
    lock_file.close()
    os.remove('bot.lock')

# --- 主程序 ---
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                MessageHandler(filters.Regex('^📡 DNS管理$'), dns_management),
                MessageHandler(filters.Regex('^💻 终端$'), secure_shell),
                MessageHandler(filters.Regex('^🚪 退出$'), lambda u, c: ConversationHandler.END)
            ],
            SHELL_CMD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, execute_command)
            ],
            DNS_MGMT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: MENU)
            ]
        },
        fallbacks=[CommandHandler('cancel', start)]
    )

    application.add_handler(conv_handler)
    logger.info("✅ 机器人启动成功")
    await application.run_polling()

if __name__ == '__main__':
    os.makedirs(SAFE_WORK_DIR, mode=0o700, exist_ok=True)
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.ensure_future(main())
        else:
            loop.run_until_complete(main())
    finally:
        cleanup()