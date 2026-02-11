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
    url = f"https://api.trello.com/1/boards/{BOARD_ID}/cards"
    params = {
        "key": API_KEY,
        "token": TOKEN
    }

    response = requests.get(url, params=params)
    cards = response.json()

    datas = []

    for card in cards:
        card_id = card["id"]
        timestamp = int(card_id[:8], 16)
        data = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        datas.append(data)

    contagem = Counter(datas)

    return jsonify(contagem)

  # CERTO
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) # Dê um TAB ou 4 espaços aqui
    app.run(host='0.0.0.0', port=port)       # E aqui também
