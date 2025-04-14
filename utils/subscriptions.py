import requests
import base64

def parse_subscription(url):
    response = requests.get(url)
    if response.status_code == 200:
        decoded = base64.b64decode(response.text).decode("utf-8")
        return decoded.splitlines()
    else:
        return []