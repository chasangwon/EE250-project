import paho.mqtt.client as mqtt
import json
import time


def on_connect(client, userdata, flags, rc):

    print("Connected to server (i.e., broker) with result code " + str(rc))
    # replace user with your USC username in all subscriptions
    # Add the custom callbacks by indicating the topic and the name of the callback handle

    client.subscribe("sangwonc/sensor_info")
    client.message_callback_add("sangwonc/sensor_info", on_message_from_payload)

    # client.subscribe("sangwonc/distance")
    # client.message_callback_add("sangwonc/distance", on_message_from_distance)
    #
    # client.subscribe("sangwonc/temperature")
    # client.message_callback_add("sangwonc/temperature", on_message_from_temperature)
    #
    # client.subscribe("sangwonc/humidity")
    # client.message_callback_add("sangwonc/humidity", on_message_from_humidity)


def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

# Custom message callback.
def on_message_from_distance(client, userdata, message):
    print("Custom callback  - distance: " + message.payload.decode())

def on_message_from_temperature(client, userdata, message):
    print("Custom callback  - temperature " + message.payload.decode())

def on_message_from_humidity(client, userdata, message):
    print("Custom callback  - humidity " + message.payload.decode())

def on_message_from_payload(client, userdata, message):
    d = json.loads(message.payload.decode("utf-8"))
    with open("sensor_info.txt", "a+") as file:
        file.write("{0},{1},{2}".format(d["distance"], d["temp"], d["hum"]))

def process_info():
    with open('sensor_info.txt', 'r') as f:
        last_line = f.readlines()[-1]
        processed = last_line.split(',')

    distance = processed[0]
    temp = processed[1]
    hum = processed[2]

    print('Distance: {}, Temp: {}, Hum: {}'.format(distance, temp, hum))



if __name__ == '__main__':
    # create a client object
    client = mqtt.Client()
    # attach a default callback which we defined above for incoming mqtt messages
    client.on_message = on_message
    # attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect

    client.connect(host="172.20.10.2", port=1883, keepalive=60)

    client.loop_forever()

    while True:
        process_info()
        time.sleep(2)

