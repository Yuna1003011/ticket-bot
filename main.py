import requests
import time
import random
import os

URL = "https://relief-ticket.jp/events/artist/40/127"
WEBHOOK = "https://discord.com/api/webhooks/1484872948920877217/4RKMq62nrlDXWCxEs_u29Zd3Est_C9runcsdhwlYq_jdTx0uQvu1IfF9g1GhUlwz5qFO"

MIN_INTERVAL = 5
MAX_INTERVAL = 12

STATE_FILE = "status.txt"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def load_last_status():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return "none"

def save_status(status):
    with open(STATE_FILE, "w") as f:
        f.write(status)

def send(msg):
    requests.post(WEBHOOK, json={"content": msg})

def check():
    try:
        res = requests.get(URL, headers=headers)
        html = res.text

        if any(word in html for word in ["申込み", "購入", "残席", "受付中"]):
            return "available"
        elif any(word in html for word in ["該当なし", "受付終了"]):
            return "none"
        else:
            return "unknown"

    except Exception as e:
        send(f"⚠️エラー: {e}")
        return "error"

last_status = load_last_status()

send("🚀監視スタート（軽量版）")

while True:
    current_status = check()

    if current_status == "available" and last_status != "available":
        send("🔥SixTONESリセール出た！！！")

    if current_status != "error":
        save_status(current_status)
        last_status = current_status

    time.sleep(random.randint(MIN_INTERVAL, MAX_INTERVAL))
