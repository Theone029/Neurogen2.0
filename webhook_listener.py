from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received webhook:", data)
    # Here you’d process the payment and deliver leads
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(port=5001)
