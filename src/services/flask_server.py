from flask import Flask, jsonify
import os
import json

app = Flask(__name__)

# Path to your latest_data.json (same one written by mqtt_receiver.py)
DATA_PATH = "../../data/external/latest_data.json"

@app.route("/")
def home():
    return "🗑️ SmartBin Flask API is running!"

@app.route("/latest")
def get_latest_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"error": "No data available yet."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
