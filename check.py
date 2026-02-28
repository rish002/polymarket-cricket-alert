import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

POLYMARKET_URL = "https://api.polymarket.com/markets?category=Sports&subcategory=Cricket"

STATE_FILE = "last_market.txt"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

def get_last_market():
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, "r") as f:
        return f.read().strip()

def save_last_market(market_id):
    with open(STATE_FILE, "w") as f:
        f.write(str(market_id))

def main():
    response = requests.get(POLYMARKET_URL)
    markets = response.json()

    if not markets:
        return

    markets.sort(key=lambda x: x.get("createdAt", ""), reverse=True)

    latest_market = markets[0]
    latest_id = str(latest_market["id"])

    last_id = get_last_market()

    if latest_id != last_id:
        question = latest_market.get("question", "New Cricket Game")
        link = f"https://polymarket.com/event/{latest_market.get('slug','')}"
        message = f"New Cricket Game Listed!\n\n{question}\n\n{link}"
        send_telegram(message)
        save_last_market(latest_id)

if __name__ == "__main__":
    main()
