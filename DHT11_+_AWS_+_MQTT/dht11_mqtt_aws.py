import ssl
import time
import json
import paho.mqtt.client as mqtt
import adafruit_dht
import board
from datetime import datetime

# --- AWS IoT Configuration ---
AWS_ENDPOINT = "a1u5rzhci0e8b2-ats.iot.eu-north-1.amazonaws.com"
PORT = 8883
TOPIC = "iot_temp"
CLIENT_ID = "RaspberryPi"

CA_PATH = "/home/vivek/dht11/rootCA.pem"
CERT_PATH = "/home/vivek/dht11/certificate.pem.crt"
KEY_PATH = "/home/vivek/dht11/private.pem.key"

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("? Connected to AWS IoT Core!")
    else:
        print("? Connection failed with code:", rc)

def on_message(client, userdata, msg):
    print(f"?? {msg.topic}: {msg.payload.decode()}")

# --- MQTT Client Setup ---
client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(
    ca_certs=CA_PATH,
    certfile=CERT_PATH,
    keyfile=KEY_PATH,
    tls_version=ssl.PROTOCOL_TLSv1_2
)
client.tls_insecure_set(False)

client.connect(AWS_ENDPOINT, PORT, keepalive=60)
client.loop_start()

# --- DHT11 Setup ---
# use_pulseio=False avoids libgpiod dependency
dht_device = adafruit_dht.DHT11(board.D15, use_pulseio=False)

# --- Main Loop: Read sensor and publish ---
while True:
    try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity

        # Safely convert to Fahrenheit if temperature is valid
        if temperature_c is not None:
            temperature_f = temperature_c * 9 / 5 + 32
        else:
            temperature_f = None

        # Prepare JSON data with timestamp
        data = {
            "timestamp": datetime.now().isoformat(),
            "temperature_c": temperature_c,
            "temperature_f": temperature_f,
            "humidity": humidity
        }

        # Publish to AWS IoT, retain=False (pulse off)
        client.publish(TOPIC, json.dumps(data), qos=1, retain=False)
        print("?? Published:", data)

    except RuntimeError as err:
        # DHT11 read errors are normal
        print("?? DHT11 read error:", err)

    time.sleep(5)  # Adjust delay as needed
