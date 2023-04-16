import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):

    print("Connected to server (i.e., broker) with result code " + str(rc))
    # replace user with your USC username in all subscriptions
    # Add the custom callbacks by indicating the topic and the name of the callback handle
    client.subscribe("sangwonc/distance")
    client.message_callback_add("sangwonc/distance", on_message_from_distance)

    client.subscribe("sangwonc/temperature")
    client.message_callback_add("sangwonc/temperature", on_message_from_temperature)

    client.subscribe("sangwonc/humidity")
    client.message_callback_add("sangwonc/humidity", on_message_from_humidity)


def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

# Custom message callback.
def on_message_from_distance(client, userdata, message):
    print("Custom callback  - distance: " + message.payload.decode())

def on_message_from_temperature(client, userdata, message):
    print("Custom callback  - temperature " + message.payload.decode())

def on_message_from_humidity(client, userdata, message):
    print("Custom callback  - humidity " + message.payload.decode())


if __name__ == '__main__':
    # create a client object
    client = mqtt.Client()
    # attach a default callback which we defined above for incoming mqtt messages
    client.on_message = on_message
    # attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect

    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)

    client.loop_forever()
