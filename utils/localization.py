messages = {
    "en": {
        "welcome": "Welcome to the VPN Bot!",
        "help": "Available commands:\n/start - Start the bot\n/help - Show this help\n/add_node - Add a VPN node\n/list_nodes - List VPN nodes\n/remove_node - Remove a VPN node",
        "not_authorized": "You are not authorized to perform this action.",
        "node_added": "Node added successfully!",
        "node_removed": "Node removed successfully!",
        "invalid_command": "Invalid command. Please try again.",
        "no_nodes_found": "No nodes found."
    }
}

def get_message(key, lang="en"):
    return messages.get(lang, {}).get(key, key)