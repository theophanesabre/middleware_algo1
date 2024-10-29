from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

CAPITAL_API_KEY = os.getenv("CAPITAL_API_KEY")
CAPITAL_BASE_URL = "https://api-capital.backend-capital.com/api/v1"

headers = {
    "X-CAP-API-KEY": CAPITAL_API_KEY,
    "Content-Type": "application/json"
}

def send_order_to_capital(symbol, side, quantity, price):
    url = f"{CAPITAL_BASE_URL}/orders"
    payload = {
        "market": symbol,
        "side": side,
        "quantity": quantity,
        "price": price
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    symbol = data.get("symbol")
    side = data.get("side")
    quantity = data.get("quantity")  # La quantité reçue du webhook
    price = data.get("price")

    if not symbol or not side or not quantity:
        return jsonify({"error": "Invalid data"}), 400

    response = send_order_to_capital(symbol, side, quantity, price)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
