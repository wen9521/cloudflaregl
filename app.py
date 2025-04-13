from flask import Flask, request
from telegram.ext import Application, CommandHandler
from modules.cache_management import clear_cache_handler
from modules.waf_rules import add_waf_handler
from modules.domain_status import check_domain_status_handler
from modules.load_balancer import create_load_balancer_handler
from modules.performance_optimization import toggle_brotli_handler

app = Flask(__name__)

# Initialize the Telegram Bot Application
bot_application = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

# Add Command Handlers
bot_application.add_handler(clear_cache_handler)
bot_application.add_handler(add_waf_handler)
bot_application.add_handler(check_domain_status_handler)
bot_application.add_handler(create_load_balancer_handler)
bot_application.add_handler(toggle_brotli_handler)

@app.route('/')
def index():
    return "Telegram Cloudflare Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    # Process the incoming update
    update = request.get_json()
    bot_application.update_queue.put(update)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)