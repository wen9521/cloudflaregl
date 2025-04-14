from flask import Flask, request
from telegram import Update
from telegram.ext import Dispatcher
from bot import bot
from modules import start, cloudflare, help

app = Flask(__name__)

# Telegram Bot Dispatcher
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(start.handler)
dispatcher.add_handler(cloudflare.handler)
dispatcher.add_handler(help.handler)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)