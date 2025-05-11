from flask import Flask, request
import stripe
from config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
from database import set_user_active

stripe.api_key = STRIPE_SECRET_KEY

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        return f"Webhook error: {str(e)}", 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        telegram_id = int(session["metadata"]["telegram_id"])
        set_user_active(telegram_id, 1)

    return "OK", 200
