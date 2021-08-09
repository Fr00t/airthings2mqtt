from tabulate import tabulate
from getpass import getpass
from airthings2mqtt import get_sensor_data, get_access_token, parse_sensor_data
import paho.mqtt.client as mqtt
import time
import json

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to MQTT-broker")
    elif rc == 1:
        print("connection refused, unacceptable protocol version")
    elif rc == 2:
        print("Connection refused, identifier rejected")
    elif rc == 3:
        print("Connection refused, server unavailable")
    elif rc == 4:
        print("Connection refused, bad user name or password")
    elif rc == 5:
    	print("Connection refused, not authorized")

mqtt_connection = False
airthings_connection = False
settings = {}
mqtt_connection
airthings_connection

print("Running setup of program")
print()
while airthings_connection is False:
    airthings_username = input("Please input username of Airthings account (e-mail): ")
    airthings_password = getpass("Please input password of Airthings account: ")
    access_token, expiry = get_access_token(airthings_username, airthings_password)
    if access_token:
        settings['access_token'] = access_token
        settings['expiry'] = expiry
        print("Successfully connected to Airthings cloud")
        
        sensor_data = get_sensor_data(access_token)
        publish_list = parse_sensor_data(sensor_data)
        print("The following topics will be published next time the program runs: ")
        print()
        print(tabulate(publish_list, ['Topic', 'Value', 'Unit'], tablefmt="plain"))
        print()

        airthings_connection = True
    else:
        print("Couldn't connect. Please retry..")

while mqtt_connection is False:
    mqtt_adress = input("Please input IP or adress of MQTT-broker: ")
    mqtt_port = input("Input MQTT-port, default=1883: ")
    if mqtt_port == '':
        mqtt_port = 1883
    mqtt_username = input("Input MQTT-username, leave blank if no authentication is required: ")
    if mqtt_username == '':
        #No mqtt-authentication needed
        pass
    else:
        mqtt_password = getpass("Input MQTT-password: ")

    client = mqtt.Client("airthings2mqtt_setup")
    if mqtt_username != '':
        client.username_pw_set(username=mqtt_username, password=mqtt_password)
    client.on_connect = on_connect
    client.loop_start()
    print("Please wait, testing connection...")

    try:
        client.connect(mqtt_adress, port=mqtt_port)
        time.sleep(5)
        client.loop_stop()
        mqtt_connection = True
    except:
        client.loop_stop()
        print("Couldn't connect to the broker, please check settings.")

    if mqtt_username != '':
        settings['mqtt_username'] = mqtt_username
        settings['mqtt_password'] = mqtt_password

print("Available QOS-levels of MQTT: ")
print("0 - At most once")
print("1 - At least once")
print("2 - Exactly once")

mqtt_qos = input("Input QOS-level, recommended 1: ")
if mqtt_qos == '':
    mqtt_qos = 1
settings['mqtt_adress'] = mqtt_adress
settings['mqtt_port'] = mqtt_port
settings['mqtt_qos'] = mqtt_qos
settings['airthings_username'] = airthings_username
settings['airthings_password'] = airthings_password

print()
print("Setup complete. The program can now be scheduled to run in the background.")
print()

with open('settings.json', 'w') as fp:
    json.dump(settings, fp, indent=4, sort_keys=True)
