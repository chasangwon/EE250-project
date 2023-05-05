import time
import grovepi
import paho.mqtt.client as mqtt
import json
from tb_device_mqtt import TBDeviceMqttClient

# import Adafruit_GPIO.SPI as SPI

client = None
telemetry = {'Distance': 0, 'Temp': 0, 'Hum': 0}

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))



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
    light_port = 0  # port A0
    led_port = 4 # port D4
    buzzer_port = 3 # port D3
    led_on = 0 # LED off for now

    # Establish ports as either inputs or outputs
    grovepi.pinMode(led_port, "OUTPUT")
    grovepi.pinMode(light_port, "INPUT")
    grovepi.pinMode(buzzer_port, "OUTPUT")

    # Initialize variables and store data
    light = grovepi.analogRead(light_port)
    [humi, temp] = grovepi.dht(temphum_port, 0)
    grovepi.digitalWrite(led_port, led_on)

    grovepi.set_bus("RPI_1")
    time.sleep(1)

    def connect_MQTT():
        global client
        client = TBDeviceMqttClient('demo.thingsboard.io', 1883, 'Y3FuVTzm2QzLnA2il9Xo')
        # client.on_connect = on_connect
        client.set_server_side_rpc_request_handler(on_server_rpc_request)
        client.connect()
        time.sleep(1)

    # # controls LED (room light) from dashboard
    # def on_server_rpc_request(client, request_id, request_body):
    #     global led_on
    #     if request_body['method'] == 'getLED':
    #         client.send_rpc_reply(request_id, (True if (led_on == 1) else False))
    #     elif request_body['method'] == 'setLED':
    #         led_on = 1 if request_body['params'] else 0
    #         grovepi.digitalWrite(led_port, led_on)

    connect_MQTT()

    while not client.stopped:

        # Read new sensor value from potentiometer, ultrasonic ranger
        light = grovepi.analogRead(light_port)
        [humi, temp] = grovepi.dht(temphum_port, 0)
        print('Light: {}, Humi: {}, Temp: {}'.format(light, humi, temp))
        telemetry['Light'] = light
        telemetry['Temp'] = temp
        telemetry['Hum'] = humi
        client.send_telemetry(telemetry)

        if light > 200 or temp > 70 or humi < 20:
            grovepi.digitalWrite(buzzer_port,1)

        time.sleep(1)

        grovepi.digitalWrite(buzzer_port,0) # turn off at every loop

if __name__ == '__main__':
    main()