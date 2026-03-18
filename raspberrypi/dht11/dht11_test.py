import time
import adafruit_dht
import board

# Initialize DHT11 on GPIO15 (physical pin 10) without PulseIn
dht_device = adafruit_dht.DHT11(board.D15, use_pulseio=False)

while True:
    try:
        temperature_c = dht_device.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dht_device.humidity

        print("Temp: {:.1f} C / {:.1f} F    Humidity: {}%".format(
            temperature_c, temperature_f, humidity))

    except RuntimeError as err:
        # Reading errors are normal; just print and continue
        print("Sensor read error:", err.args[0])

    time.sleep(2.0)
