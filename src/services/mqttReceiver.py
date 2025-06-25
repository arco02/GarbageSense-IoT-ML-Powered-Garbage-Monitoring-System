import paho.mqtt.client as mqtt
import joblib
import json

model=joblib.load("../../models/model.pkl")
le=joblib.load("../../models/encoder.pkl")

def on_message(client, userdata, message):
    try:
        raw=message.payload.decode()
        print("Received from MQTT :", raw)

        parts=raw.replace('%','').split(',')
        temp=float(parts[0])
        hum=float(parts[1])
        fill_level=float(parts[2])

        prediction=model.predict([[temp, hum]])[0]
        label=le.inverse_transform([prediction])[0]

        print("Temperate : "+str(temp)+"\nHumidity : "+str(hum)+"\nFill Level : "+str(fill_level)+"%\nLabel :"+label)

        result = {
            "temperature": temp,
            "humidity": hum,
            "fill_level": fill_level,
            "label": label
        }
        with open("../../data/external/latest_data.json", "w") as f:
            json.dump(result, f)
    except Exception as e :
        print(e)

client=mqtt.Client()
client.connect("broker.hivemq.com",1883);
client.subscribe(topic="smartbin/data")
client.on_message=on_message
print("🚀 Listening for MQTT messages...")
client.loop_forever()