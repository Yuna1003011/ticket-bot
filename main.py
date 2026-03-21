from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import os
import random

URL = "https://relief-ticket.jp/events/artist/40/127"
WEBHOOK = "https://discord.com/api/webhooks/1484872948920877217/4RKMq62nrlDXWCxEs_u29Zd3Est_C9runcsdhwlYq_jdTx0uQvu1IfF9g1GhUlwz5qFO"

MIN_INTERVAL = 5
MAX_INTERVAL = 12

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0")

driver = webdriver.Chrome(options=options)

STATE_FILE = "status.txt"

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
        driver.get(URL)
        time.sleep(3)
        html = driver.page_source

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

send("🚀SixTONES監視スタート")

while True:
    current_status = check()

    if current_status == "available" and last_status != "available":
        send("🔥SixTONESリセール出た！！！今すぐ開け！！！")

    if current_status != "error":
        save_status(current_status)
        last_status = current_status

    time.sleep(random.randint(MIN_INTERVAL, MAX_INTERVAL))
