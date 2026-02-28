import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

POLYMARKET_URL = "https://gamma-api.polymarket.com/markets"

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

    if response.status_code != 200:
        print("API Error:", response.status_code)
        return

    markets = response.json()

    # Filter only Cricket category
    cricket_markets = [
        m for m in markets
        if m.get("category", "").lower() == "sports"
        and m.get("subcategory", "").lower() == "cricket"
    ]

    if not cricket_markets:
        print("No cricket markets found")
        return

    cricket_markets.sort(key=lambda x: x.get("createdAt", ""), reverse=True)

    latest_market = cricket_markets[0]
    latest_id = str(latest_market["id"])

    last_id = get_last_market()

    if latest_id != last_id:
        question = latest_market.get("question", "New Cricket Game")
        slug = latest_market.get("slug", "")
        link = f"https://polymarket.com/event/{slug}"

        message = f"🏏 New Cricket Game Listed!\n\n{question}\n\n{link}"
        send_telegram(message)
        save_last_market(latest_id)
        print("New market sent!")
    else:
        print("No new market.")

if __name__ == "__main__":
    main()
