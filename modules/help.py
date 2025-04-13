from telegram.ext import CommandHandler

def help_command(update, context):
    update.message.reply_text("Available commands:\n"
                              "/start - Start the bot\n"
                              "/help - Show this help message\n"
                              "/list_dns - List DNS records")

handler = CommandHandler('help', help_command)