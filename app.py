from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler
from modules import start, cloudflare, help

app = Flask(__name__)

# Initialize the Telegram Bot Application
bot_application = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

# Add Command Handlers
bot_application.add_handler(start.handler)
bot_application.add_handler(cloudflare.handler)
bot_application.add_handler(help.handler)

# Define a root route to handle `/`
@app.route('/')
def index():
    return "Telegram Cloudflare Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    # Process the incoming update
    update = Update.de_json(request.get_json(), bot_application.bot)
    bot_application.update_queue.put(update)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)