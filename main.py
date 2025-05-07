from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("EAAYH4fpuod0BOzu5KFaagApjhEGSTiPYlDbJ0mlitRKXnZBkvKF3RU9PrUctONk2E16ZAB2Hzczvd9YJOJCNppzleLzonZC3PrCjiWE782nQGn2AsHHRZAA6DldoaZBtJ3AxUbwpawXg0kWH0K730Q9j8lifTVZBq1B5tpbq9rxzKhvWEbYfUestYkC7HxuhnMYyOOwV2LlvKnrenr")
PAGE_ACCESS_TOKEN = os.environ.get("roeis_webhook_2025")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token", 403

    if request.method == "POST":
        data = request.get_json()
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]
                if "message" in messaging_event:
                    send_message(sender_id, arvut_response())
        return "OK", 200

def arvut_response():
    return (
        "Hi! A few quick questions to help us screen for the right room:\n\n"
        "1. How many people will the room be for?\n"
        "2. Do you have children? (Note: Children are not allowed, even for visits)\n\n"
        "📌 Prices: Single tenant = R4400. Couple = R4700 + R200 utilities each.\n"
        "🚫 No overnight guests.\n\n"
        "⏰ Viewings: Mon–Fri, 8am–4pm (excl. public holidays)\n"
        "📍 Location: 9 Melon Street, Maitland\n"
        "📅 To book a viewing, please send us:\n"
        "- Full name\n- Cell number\n- Preferred day/time\n\n"
        "💬 Or contact Anthony directly: +27 83 525 3170\n"
        "🏠 See listings: https://www.facebook.com/marketplace/profile/100000658290757/?ref=permalink&tab=listings&mibextid=6ojiHh"
    )

def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post(url, params=params, headers=headers, json=data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
