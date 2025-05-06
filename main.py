from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = '2wfgaXsF3AhSEoIXqzjD7Q0S7zq_3y8yfnMGKk7p75FZsNZ7J'
PAGE_ACCESS_TOKEN = 'EAAXL20IaXaYBO57rWPeX330wbZAe0ZBozb7RaoaHmNMl2PxnOeRVeGaetgswfMYdi4j0EyeTwREgFddSkZAPwyZCIZCjxzIu5g6W3khmwPH5OvZAWs2ZA6E1CqL9NXMXzypamUUPyYDQoPCnSZAJ77ZCgOenzshzN2QvaA4EGmZBgzK5BQeMhSWx2sR7PmGZAxOMMncTfeGZBzNp9nZCZBWX9D'

@app.route("/", methods=["GET"])
def home():
    return "Tenant bot is running ✅"

def send_message(recipient_id, message_text):
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': message_text}
    }
    headers = {'Content-Type': 'application/json'}
    params = {'access_token': PAGE_ACCESS_TOKEN}
    requests.post('https://graph.facebook.com/v17.0/me/messages',
                  headers=headers, params=params, json=payload)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "Verification failed", 403

    if request.method == 'POST':
        data = request.get_json()
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                if "message" in event and "text" in event["message"]:
                    text = event["message"]["text"].lower()

                    if "child" in text or "kid" in text:
                        send_message(sender_id, "Unfortunately children aren’t allowed at the property — even for visits.")
                    elif "double" in text or "2" in text or "two" in text:
                        send_message(sender_id, "For two tenants, rent is R4700 + R200/person for utilities.")
                    elif "price" in text or "cost" in text:
                        send_message(sender_id, "The ad price is for one tenant. Let me know if it’s for more.")
                    elif "view" in text:
                        send_message(sender_id, "Viewings are Mon–Fri, 8AM–4PM at 9 Melon St, Maitland.")
                    else:
                        send_message(sender_id, "Hi! Is the room for 1 or 2 people? And do you have children?")
        return "ok", 200

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT", 10000)), host="0.0.0.0")
