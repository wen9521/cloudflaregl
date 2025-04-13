AUTHORIZED_USERS = [123456789, 987654321]  # 替换成你的 Telegram 用户 ID

def restricted(func):
    def wrapper(update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        if user_id not in AUTHORIZED_USERS:
            update.message.reply_text("You are not authorized to use this bot.")
            return
        return func(update, context)
    return wrapper

@restricted
def set_kv(update: Update, context: CallbackContext):
    # Your existing function here
    pass