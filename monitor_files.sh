#!/bin/bash
# 监控关键文件变更
files_to_watch=(
    "cf_bot.py"
    ".env"
    "run.sh"
)

for file in "${files_to_watch[@]}"; do
    if [ -f "$file" ]; then
        inotifywait -m -e modify,attrib "$file" |
        while read -r directory event filename; do
            echo "安全警报：文件 $filename 被修改！"
        done &
    fi
done