import requests
from telegram import Update
from telegram.ext import CallbackContext

CLOUDFLARE_API_TOKEN = "your-cloudflare-api-token"
CLOUDFLARE_ACCOUNT_ID = "your-cloudflare-account-id"
KV_NAMESPACE_ID = "your-kv-namespace-id"

# Modify or add a KV variable
def set_kv(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 2:
        update.message.reply_text("Usage: /set_kv <key> <value>")
        return

    key = context.args[0]
    value = " ".join(context.args[1:])  # Handle multi-word values

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "text/plain"
    }
    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/storage/kv/namespaces/{KV_NAMESPACE_ID}/values/{key}"
    response = requests.put(url, headers=headers, data=value)

    if response.status_code == 200:
        update.message.reply_text(f"KV variable '{key}' set successfully!")
    else:
        update.message.reply_text(f"Failed to set KV variable: {response.text}")

# Retrieve a KV variable
def get_kv(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 1:
        update.message.reply_text("Usage: /get_kv <key>")
        return

    key = context.args[0]

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
    }
    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/storage/kv/namespaces/{KV_NAMESPACE_ID}/values/{key}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        update.message.reply_text(f"KV variable '{key}': {response.text}")
    else:
        update.message.reply_text(f"Failed to retrieve KV variable: {response.text}")