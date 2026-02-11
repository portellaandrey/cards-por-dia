import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
import requests
from collections import Counter
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_KEY")
TOKEN = os.getenv("TOKEN")
BOARD_ID = os.getenv("BOARD_ID")

@app.route("/")
def home():
    return "API Trello online 🚀"

@app.route("/cards-por-dia")
def cards_por_dia():
    url = f"https://api.trello.com/1/boards/{BOARD_ID}/cards?filter=open"
    params = {
        "key": API_KEY,
        "token": TOKEN
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        cards = response.json()

        datas = []
        for card in cards:
            card_id = card["id"]
            timestamp = int(card_id[:8], 16)
            data = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
            datas.append(data)

        contagem = dict(sorted(Counter(datas).items()))

        return jsonify(contagem)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)