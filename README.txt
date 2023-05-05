Sangwon Cha (Done individually)

Instructions on how to compile/execute program(s):
sensors.py should be run on RPi, with sensors connected to it. ThingsBoard generates
an access token for each device that is added to the users' account, and the String of the
access token must passed as a parameter when instantiating a ThingsBoard MQTT client. 

List of any external libraries that were used:
import time
import grovepi
from tb_device_mqtt import TBDeviceMqttClient
(import statements were copied and pasted)
