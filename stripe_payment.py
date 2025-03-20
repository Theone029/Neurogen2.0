import json
import stripe

with open('config.json', 'r') as f:
    config = json.load(f)

stripe.api_key = config.get('stripe_api_key')

def create_payment_session(amount, currency="usd"):
    # Dummy function: Replace with stripe.checkout.Session.create in production.
    session = {"id": "dummy_session_id", "amount": amount, "currency": currency}
    return session

if __name__ == '__main__':
    session = create_payment_session(1000)
    print("Payment session created:", session)
