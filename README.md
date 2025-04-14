# Telegram VPN Bot

## 功能
- 节点管理（添加、查看、删除）
- 二维码生成
- 节点订阅解析
- 节点延迟测速
- 多语言支持

## 部署步骤

### 1. 配置环境变量
- `TELEGRAM_BOT_TOKEN`: Telegram Bot 的 Token。
- `WEBHOOK_URL`: Render 提供的 Webhook URL。
- `ADMIN_ID`: 管理员的 Telegram ID。

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 部署到 Render
- 在 Render 创建一个 Web Service。
- 设置环境变量。
- 部署代码。

### 4. 设置 Webhook
访问 `/set_webhook` 端点以设置 Webhook。