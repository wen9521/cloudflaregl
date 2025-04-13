# Telegram Cloudflare Manager Bot

A modular Telegram Bot to manage Cloudflare resources, deployed using Render.

## Features
- **Modular Design**: Easily extendable with new commands.
- **Webhook Deployment**: Uses Telegram Webhook for efficient updates.
- **Cloudflare Management**: List DNS records and more.

## Setup Instructions

### Prerequisites
1. Telegram Bot Token: Create a bot using [BotFather](https://core.telegram.org/bots#botfather).
2. Cloudflare API Token: Generate a token from Cloudflare with the necessary permissions.
3. Render Account: Sign up at [Render](https://render.com/).

### Local Development
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask app locally:
   ```bash
   python app.py
   ```

### Deployment to Render
1. Push this repository to GitHub or any Git provider.
2. Create a new **Web Service** on Render.
3. Use `render.yaml` for automatic deployment configuration.
4. Set environment variables in Render:
   - `API_TOKEN`
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_ZONE_ID`
5. Deploy and set the Telegram Webhook:
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_API_TOKEN>/setWebhook?url=https://<YOUR_RENDER_URL>/webhook"
   ```

## Commands
- `/start`: Start the bot.
- `/help`: Display help message.
- `/list_dns`: List Cloudflare DNS records.

## License
MIT