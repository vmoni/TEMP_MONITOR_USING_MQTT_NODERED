import ssl
import time
import paho.mqtt.client as mqtt
import json

# AWS IoT Endpoint
AWS_ENDPOINT = "a1u5rzhci0e8b2-ats.iot.eu-north-1.amazonaws.com"
PORT = 8883
TOPIC = "IOT_DATA"
CLIENT_ID = "RaspberryPi"

# Certificate paths
CA_PATH = "/home/vivek/dht11/rootCA.pem"
CERT_PATH = "/home/vivek/dht11/certificate.pem.crt"
KEY_PATH = "/home/vivek/dht11/private.pem.key"

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("? Connected to AWS IoT Core!")
    else:
        print("? Connection failed with code:", rc)

def on_message(client, userdata, msg):
    print(f"?? {msg.topic}: {msg.payload.decode()}")

# MQTT Client
client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message

# TLS Configuration
client.tls_set(
    ca_certs=CA_PATH,
    certfile=CERT_PATH,
    keyfile=KEY_PATH,
    tls_version=ssl.PROTOCOL_TLSv1_2
)
client.tls_insecure_set(False)

# Connect and loop
client.connect(AWS_ENDPOINT, PORT, keepalive=60)
client.loop_start()

# Publish sample JSON data
while True:
    data = {"year": 2025, "month": 10, "date": 24}
    client.publish(TOPIC, json.dumps(data), qos=1)
    print("?? Published:", data)
    time.sleep(5)

