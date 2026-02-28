print("SCRIPT STARTED 🚀")
import requests
import os
import time
import json

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

SEEN_FILE = "seen_markets.json"


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)


def get_cricket_markets():
    url = "https://gamma-api.polymarket.com/markets"
    params = {
        "active": "true",
        "closed": "false",
        "limit": 100
    }

    response = requests.get(url)
    data = response.json()

    cricket_markets = []

    for market in data:
        if "cricket" in market.get("question", "").lower():
            cricket_markets.append(market)

    return cricket_markets


def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f)


def main():
    seen = load_seen()
    markets = get_cricket_markets()

    for market in markets:
        market_id = market["id"]

        if market_id not in seen:
            message = f"🏏 NEW CRICKET MARKET:\n\n{market['question']}"
            send_telegram(message)

            seen.append(market_id)

    save_seen(seen)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(300)  # runs every 5 minutes
