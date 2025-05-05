
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "2wfgaXsF3AhSEoIXqzjD7Q0S7zq_3y8yfnMGKk7p75FZsNZ7J"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403

    if request.method == "POST":
        data = request.json
        print("Incoming message:", data)
        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
