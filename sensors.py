import time
import grovepi
import paho.mqtt.client as mqtt
import json
# import Adafruit_GPIO.SPI as SPI
# import Adafruit_MCP3008

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print(
        "Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

def connect_MQTT():
    client = mqtt.Client()

    client.on_connect = on_connect

    client.connect(host="172.20.10.2", port=1883, keepalive=60)

    client.loop_start()
    time.sleep(1)

    return client


def publish_data(mqtt_client, data):
    distance = data[0]
    temp = data[1]
    hum = data[2]

    # replace user with your USC username in all subscriptions
    mqtt_client.publish("sangwonc/sensor_info", '{"distance": {0}, "temp": {1}, "hum": {2}}'.format(distance, temp, hum))
    print(f"Publishing distance: {distance} cm")
    time.sleep(1)

    # # publish date and time in their own topics
    # mqtt_client.publish("sangwonc/temperature", f"{temp}")
    # print(f"Publishing temperature: {temp} C")
    # time.sleep(1)
    #
    # mqtt_client.publish("sangwonc/humidity", f"{hum}")
    # print(f"Publishing humidity: {hum}%")
    # time.sleep(1)

def main():
    # Specify port numbers for each sensor/display
    temphum_port = 2  # port D2
    ultra_port = 4  # port D4
    # Establish ports as either inputs or outputs
    grovepi.pinMode(ultra_port, "INPUT")


    # # Initialize variables used in while loop
    # humi_old = 0
    # temp_old = 0

    data = []

    grovepi.set_bus("RPI_1")
    time.sleep(1)

    clientmqtt = connect_MQTT()

    while True:

        # Read new sensor value from potentiometer, ultrasonic ranger
        distance_new = grovepi.ultrasonicRead(ultra_port)
        [humi_new, temp_new] = grovepi.dht(temphum_port, 0)

        print('Distance: {}, Humi: {}, Temp: {}'.format(distance_new, humi_new, temp_new))
        data.extend([distance_new, temp_new, humi_new])

        publish_data(clientmqtt, data)

        # New sensor values are now old
        # [humi_old, temp_old] = [humi_new, temp_new]
        # distance_old = distance_new
        data = []
        time.sleep(1)

if __name__ == '__main__':
    main()