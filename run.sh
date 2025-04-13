#!/bin/bash
# 安全启动脚本

export PYTHONPATH=$HOME/.local/lib/python3.8/site-packages
export SAFE_WORK_DIR=$HOME/cf-bot/sandbox

while true; do
    echo "$(date) - 启动应用程序..."
    python3 ~/cf-bot/cf_bot.py >> ~/cf-bot/logs/runtime.log 2>&1
    echo "$(date) - 应用程序退出，等待重启..."
    sleep 15
    # 自动清理临时文件
    find $SAFE_WORK_DIR -type f -mmin +60 -exec rm -f {} \;
done
