import time
import grovepi
import paho.mqtt.client as mqtt
import json
from tb_gateway_mqtt import TBDeviceMqttClient

# import Adafruit_GPIO.SPI as SPI

client = None
telemetry = {'Distance': 0, 'Temp': 0, 'Hum': 0}

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

def connect_MQTT():
    global client
    client = TBDeviceMqttClient('demo.thingsboard.io', 1883, 'Y3FuVTzm2QzLnA2il9Xo')
    # client.on_connect = on_connect
    client.connect()
    time.sleep(1)

#def publish_data():
    # mqtt_client.publish("sangwonc/temperature", f"{temp}")
    # print(f"Publishing temperature: {temp} C")
    # time.sleep(1)
    # mqtt_client.publish("sangwonc/humidity", f"{hum}")
    # print(f"Publishing humidity: {hum}%")
    # time.sleep(1)

def main():
    global telemetry
    # Specify port numbers for each sensor/display
    temphum_port = 2  # port D2
    ultra_port = 4  # port D4
    # Establish ports as either inputs or outputs
    grovepi.pinMode(ultra_port, "INPUT")

    # # Initialize variables used in while loop
    # humi_old = 0
    # temp_old = 0

    grovepi.set_bus("RPI_1")
    time.sleep(1)

    connect_MQTT()

    while not client.stopped:

        # Read new sensor value from potentiometer, ultrasonic ranger
        distance_new = grovepi.ultrasonicRead(ultra_port)
        [humi_new, temp_new] = grovepi.dht(temphum_port, 0)
        print('Distance: {}, Humi: {}, Temp: {}'.format(distance_new, humi_new, temp_new))
        telemetry['Distance'] = distance_new
        telemetry['Temp'] = temp_new
        telemetry['Hum'] = humi_new
        client.send_telemetry(telemetry)

        time.sleep(1)

if __name__ == '__main__':
    main()