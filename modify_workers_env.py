import requests
from telegram import Update
from telegram.ext import CallbackContext

CLOUDFLARE_API_TOKEN = "your-cloudflare-api-token"
CLOUDFLARE_ACCOUNT_ID = "your-cloudflare-account-id"
WORKER_NAME = "your-worker-name"

# Modify an environment variable
def set_env(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 2:
        update.message.reply_text("Usage: /set_env <key> <value>")
        return

    key = context.args[0]
    value = context.args[1]

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/workers/scripts/{WORKER_NAME}/settings"
    data = {
        "env_vars": {
            key: {"text": value}
        }
    }
    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        update.message.reply_text(f"Environment variable '{key}' set successfully!")
    else:
        update.message.reply_text(f"Failed to set environment variable: {response.text}")