messages = {
    "en": {
        "not_authorized": "You are not authorized to perform this action.",
        "node_added": "Node added successfully!",
        "node_removed": "Node removed successfully!",
        "node_latency": "Node latency: {} ms",
        "invalid_command": "Invalid command. Please try again.",
        "no_nodes_found": "No nodes found."
    },
    "zh": {
        "not_authorized": "您无权执行此操作。",
        "node_added": "节点添加成功！",
        "node_removed": "节点移除成功！",
        "node_latency": "节点延迟：{} 毫秒",
        "invalid_command": "无效的命令，请重试。",
        "no_nodes_found": "未找到任何节点。"
    }
}

def get_message(key, lang="en"):
    return messages.get(lang, {}).get(key, key)