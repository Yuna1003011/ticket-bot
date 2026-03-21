 import requests
import time
import os
import threading

URL = "https://relief-ticket.jp/events/artist/40/127"
WEBHOOK = "https://discord.com/api/webhooks/1484872948920877217/4RKMq62nrlDXWCxEs_u29Zd3Est_C9runcsdhwlYq_jdTx0uQvu1IfF9g1GhUlwz5qFO"

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
    try:
        requests.post(WEBHOOK, json={"content": msg})
    except:
        pass

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
    except:
        return "error"

last_status = load_last_status()

# 👇 テスト送信（これが来れば成功）
send("✅テスト送信")
send("🚀最強監視スタート")

def worker():
    global last_status
    while True:
        current_status = check()

        if current_status == "available" and last_status != "available":
            send("@everyone 🔥SixTONESリセール出た！！！今すぐ！！！")

        if current_status != "error":
            save_status(current_status)
            last_status = current_status

        time.sleep(5)

# 👇 2並列で最速監視
for _ in range(2):
    threading.Thread(target=worker).start()
