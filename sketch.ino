#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

#define DHTPIN 13
#define DHTTYPE DHT22
#define TRIG_PIN 0
#define ECHO_PIN 4

const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqtt_server = "broker.hivemq.com";
const char* topic = "smartbin/data";

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);

void setup_wifi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

float getDistance() {
  digitalWrite(TRIG_PIN, LOW); delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10); digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH);
  return duration * 0.034 / 2;
}

void loop() {
  if (!client.connected()) client.connect("ESP32SmartBin");

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  float distance = getDistance(); // cm
  float fill_level= ((25.0-distance)/25.0)*100.0;
  if(fill_level<0) fill_level=0;
  if(fill_level>100) fill_level=100;

  String payload = String(temperature,1) + "," + String(humidity,1) + "," + String(fill_level,2)+"%";
  client.publish(topic, payload.c_str());

  Serial.println(payload);
  delay(5000);
}
