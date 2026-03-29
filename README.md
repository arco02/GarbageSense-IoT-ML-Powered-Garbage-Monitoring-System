# GarbageSense: IoT & ML Powered Garbage Monitoring System

GarbageSense is an intelligent waste management solution that combines IoT hardware, Machine Learning, and a real-time monitoring backend. The system uses an ESP32 to monitor bin fill levels and environmental conditions, processes this data via an ML model to classify waste status, and provides a Flask-based API for data retrieval.

## 🚀 Features
* **Real-time Monitoring**: Uses ESP32 and ultrasonic sensors to track garbage fill levels.
* **Environmental Sensing**: Tracks temperature and humidity using a DHT22 sensor.
* **ML Classification**: Predicts waste status/labels based on environmental factors using a Scikit-Learn model.
* **MQTT Integration**: Utilizes a pub/sub architecture for seamless data transmission between hardware and the server.
* **REST API**: A Flask server provides endpoints to access the latest bin statistics.

## 🛠️ Hardware Requirements
* **Microcontroller**: ESP32.
* **Sensors**: 
    * Ultrasonic Sensor (HC-SR04) for distance/fill-level measurement.
    * DHT22 Temperature and Humidity sensor.
* **Connectivity**: WiFi (Standard 2.4GHz).

## 📂 Project Structure
* `sketch.ino`: Firmware for the ESP32 to collect sensor data and publish to MQTT.
* `src/services/flask_server.py`: Main backend script that runs the MQTT listener and the Flask API simultaneously.
* `src/services/mqttReceiver.py`: A standalone MQTT client for processing data and running ML predictions.
* `models/`: Contains the pre-trained `model.pkl` and `encoder.pkl` for waste classification.
* `requirements.txt`: Python dependencies including Flask, Scikit-Learn, and Paho-MQTT.

## 🔧 Setup & Installation

### Hardware Setup
1.  Connect the **DHT22** data pin to `GPIO 13`.
2.  Connect the **Ultrasonic Trigger** to `GPIO 0` and **Echo** to `GPIO 4`.
3.  Flash the `sketch.ino` to your ESP32 using the Arduino IDE or Wokwi.

### Backend Setup
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Server**:
    Navigate to the `src/services/` directory and run:
    ```bash
    python flask_server.py
    ```

## 📊 API Endpoints
* **GET `/`**: Check if the server is running.
* **GET `/latest`**: Returns the most recent sensor data and ML prediction in JSON format.

## 🤖 Machine Learning Logic
The system listens to the `smartbin/data` MQTT topic. When data is received:
1.  It parses temperature, humidity, and fill-level.
2.  It uses the `model.pkl` to predict a classification based on temperature and humidity.
3.  The numerical prediction is converted back to a human-readable label using `encoder.pkl`.
4.  Results are saved to `latest_data.json` for API consumption.
