# Telegram VPN Bot

A Telegram Bot for managing VPN nodes, generating QR codes, and more.

## Features
- Add, list, and remove VPN nodes.
- Generate QR codes for VPN configuration.
- Multilingual support (currently English).
- Lightweight and compatible with Render deployment.

## Setup
1. **Environment Variables**:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram Bot token.
   - `WEBHOOK_URL`: Your Render service's public URL.
   - `ADMIN_ID`: Your Telegram user ID.

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the bot locally**:
   ```bash
   python3 app.py
   ```

4. **Deploy to Render**:
   - Add environment variables in Render's dashboard.
   - Set the `Procfile` for production deployment.

5. **Set Webhook**:
   Access `/set_webhook` endpoint to set the webhook.

## Commands
- `/start` - Start the bot.
- `/help` - Show help message.
- `/add_node` - Add a VPN node.
- `/list_nodes` - List all VPN nodes.
- `/remove_node` - Remove a VPN node.