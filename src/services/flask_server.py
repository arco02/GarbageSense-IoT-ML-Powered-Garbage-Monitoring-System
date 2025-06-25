from flask import Flask, jsonify
import os
import json
import threading
import joblib
import paho.mqtt.client as mqtt
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
DATA_PATH = "data/external/latest_data.json" 


model = joblib.load("models/model.pkl")
le = joblib.load("models/encoder.pkl")


@app.route("/")
def home():
    return "🗑️ SmartBin Flask + MQTT is running!"


@app.route("/latest")
def get_latest_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"error": "No data available yet."}), 404


def on_message(client, userdata, message):
    try:
        raw = message.payload.decode()
        print("📩 Received from MQTT:", raw)

        parts = raw.replace('%', '').split(',')
        temp = float(parts[0])
        hum = float(parts[1])
        fill_level = float(parts[2])

        prediction = model.predict([[temp, hum]])[0]
        label = le.inverse_transform([prediction])[0]

        print(f"🌡️ Temp: {temp}, 💧 Hum: {hum}, 🗑️ Fill: {fill_level}%, 🧠 Label: {label}")

        result = {
            "temperature": temp,
            "humidity": hum,
            "fill_level": fill_level,
            "label": label
        }
        with open(DATA_PATH, "w") as f:
            json.dump(result, f)
    except Exception as e:
        print("❌ Error:", e)


def mqtt_thread():
    client = mqtt.Client()
    client.connect("broker.hivemq.com", 1883)
    client.subscribe("smartbin/data")
    client.on_message = on_message
    print("🚀 Listening for MQTT messages...")
    client.loop_forever()


if __name__ == "__main__":
    
    thread = threading.Thread(target=mqtt_thread)
    thread.daemon = True
    thread.start()

    app.run(host="0.0.0.0", port=8000)
