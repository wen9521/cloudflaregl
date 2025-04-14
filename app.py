from flask import Flask, request
import telebot
import os
from utils.qr_code import generate_qr_code
from utils.subscriptions import parse_subscription
from utils.speedtest import test_node_speed
from utils.localization import get_message
from database import Database

app = Flask(__name__)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(TOKEN)
db = Database()

@app.route('/')
def home():
    return "Telegram VPN Bot is running!", 200

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    try:
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "OK", 200
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return "Internal Server Error", 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    try:
        bot.remove_webhook()
        bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
        return "Webhook set successfully!", 200
    except Exception as e:
        return f"Failed to set webhook: {e}", 500

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, get_message("welcome"))

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, get_message("help"))

@bot.message_handler(commands=['add_node'])
def add_node(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, get_message("not_authorized"))
        return
    try:
        node_info = message.text.split(maxsplit=1)[1]
        db.add_node(node_info)
        bot.reply_to(message, get_message("node_added"))
    except IndexError:
        bot.reply_to(message, get_message("invalid_command"))

@bot.message_handler(commands=['list_nodes'])
def list_nodes(message):
    nodes = db.get_nodes()
    if not nodes:
        bot.reply_to(message, get_message("no_nodes_found"))
    else:
        reply = "\n".join([f"{i+1}. {node}" for i, node in enumerate(nodes)])
        bot.reply_to(message, reply)

@bot.message_handler(commands=['remove_node'])
def remove_node(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, get_message("not_authorized"))
        return
    try:
        index = int(message.text.split(maxsplit=1)[1]) - 1
        db.remove_node(index)
        bot.reply_to(message, get_message("node_removed"))
    except (IndexError, ValueError):
        bot.reply_to(message, get_message("invalid_command"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)