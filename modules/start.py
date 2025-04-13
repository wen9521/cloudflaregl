from telegram.ext import CommandHandler

def start(update, context):
    update.message.reply_text("Welcome to the Cloudflare Manager Bot!")

handler = CommandHandler('start', start)