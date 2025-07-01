import network
import time
import machine
from umqtt.robust import MQTTClient
import dht

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Provide Your WiFi Credentials
SSID = ""
PASS = ""

#Provide your MQTT Credentials
mqtt_token = "" 

#Mention you device ID
device_ID = ""

#Example ( Publishing Variables ) 
pubvariables = {"temperature": 0, "humidity": 0}


try:
    client = MQTTClient(device_ID, "industrial.api.ubidots.com", 1883, user=mqtt_token, password=mqtt_token)
    print("MQTT client initialized successfully.")
    client.connect()
except Exception as e:
    print("Error initializing MQTT client:", e)


def connect_WiFi(SSID, PASS):
    if not wlan.isconnected():
        print("Trying to connect")
        wlan.connect(SSID, PASS)
        while not wlan.isconnected():
            pass
        print('Connected to WiFi')
        print('IP Address:', wlan.ifconfig()[0])


def mqtt_publish():
    if wlan.isconnected():
        for key in pubvariables:
            try:
                msg = b'{"%s":{"value":%s}}' % (key, pubvariables[key])
                client.publish("/v1.6/devices/pico", msg)
                print("Published message:", msg)
            except Exception as e:
                print("Error publishing message:", e)
    else:
        print("Trying to connect.....")
        connect_WiFi(SSID, PASS)


# Read DHT
def read_dht11(pin_number):
    dht_pin = machine.Pin(pin_number, machine.Pin.IN, machine.Pin.PULL_UP)
    dht_sensor = dht.DHT11(dht_pin)
    try:
        dht_sensor.measure()  # Perform a measurement
        pubvariables["temperature"] = dht_sensor.temperature()
        pubvariables["humidity"] = dht_sensor.humidity()
        print("Temperature: ", pubvariables["temperature"])
        print("Humidity: ", pubvariables["humidity"])
    except Exception as e:
        print("Error reading data:", e)


while True:
    read_dht11(16)
    mqtt_publish()
    time.sleep(1)
