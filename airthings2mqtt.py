#Parts of code sourced from https://github.com/Danielhiversen/home_assistant_airthings_cloud 
#which was shared using the Apache licence.

import json
import logging
import time
import requests
import paho.mqtt.client as mqtt
import sys


def get_access_token(username, password):
    """Uses stored credentials to fetch a new access token.

    Returns:
        [str,int]: [Access Token, seconds to expiration]
    """
    headers = {
        "content-type": "application/json;charset=UTF-8",
        "accept": "application/json, text/plain, */*",
    }    
    urlauth = "https://accounts-api.airthings.com/v1/token"
    urluri = "https://accounts-api.airthings.com/v1/authorize?client_id=dashboard&redirect_uri=https%3A%2F%2Fdashboard.airthings.com"

    object = {
        "username": username,
        "password": password,
        "grant_type": "password",
        "client_id": "accounts",
    }
    resp = requests.post(urlauth, json = object, headers = headers)
    dict = resp.json()
    access_token = dict['access_token']
    headers['authorization'] = access_token
    expiry = time.time() + dict['expires_in']

    json_data = {"scope": ["dashboard"]}

    resp = requests.post(urluri, headers = headers, json = json_data)
    dict = resp.json()
    code = str(dict["redirect_uri"].split("=")[1])

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": access_token
    }
    data = (
        '{"grant_type":"authorization_code","client_id":"dashboard",'
        '"client_secret":"e333140d-4a85-4e3e-8cf2-bd0a6c710aaa","code":"'
        + code
        + '","redirect_uri":"https://dashboard.airthings.com"}'
    )
    resp = requests.post(urlauth, headers=headers, data=data)
    dict = resp.json()

    headers['authorization'] = dict['access_token']

    return dict['access_token'], expiry


def get_sensor_data(access_token):
    urldash = "https://web-api.airthin.gs/v1/dashboards"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": access_token
    }

    resp = requests.get(urldash, headers=headers)
    return resp.json()


def parse_sensor_data(sensor_data):
    publish_list = [] #[LOC, ROOM, TYPE, VAL, UNIT]
    for device in sensor_data.get("currentDashboard", {}).get("tiles", []):
        if device.get("type") != 'device':
            continue
        location = device.get("content", {}).get("locationName")
        room = device.get("content", {}).get("roomName")
        battery = device.get("content", {}).get("batteryPercentage")
        latest_sample = device.get("content", {}).get("latestSample")
        publish_list.append(["airthings2MQTT/"+location.replace(" ", "_")+"/"+room.replace(" ", "_")+"/Battery_Percentage", battery, "%"])
        publish_list.append(["airthings2MQTT/"+location.replace(" ", "_")+"/"+room.replace(" ", "_")+"/Latest_sample", latest_sample, "ISO8601 Datetime"])
        
        sensors = device.get("content", {}).get("currentSensorValues", [])
        if not sensors:
            #print("Couldn't find any tiles with current values. Please "
            #    "check that dashboard is set up on https://dashboard.airthings.com")
            continue

        for sensor in sensors:
            publish_list.append(["airthings2MQTT/"+location.replace(" ", "_")+"/"+room.replace(" ", "_")+"/"+sensor["type"], sensor['value'], sensor['providedUnit']])
            
    return publish_list

try:
    with open('settings.json') as json_file:
        settings = json.load(json_file)
except FileNotFoundError:
    print("Couldn't find settings in folder. Please run setup.py to get started")
    sys.exit()


if settings['expiry'] - time.time() < 60:
    access_token, expiry = get_access_token(settings['airthings_username'], settings['airthings_password'])
    settings['access_token'] = access_token
    settings['expiry'] = expiry
    with open('settings.json', 'w') as fp:
        json.dump(settings, fp, indent=4, sort_keys=True)

sensor_data = get_sensor_data(settings['access_token'])
publish_list = parse_sensor_data(sensor_data)

client = mqtt.Client("Airthings2MQTT")
if "mqtt_password" in settings:
    client.username_pw_set(username=settings['mqtt_username'], password=settings['mqtt_password']) 

client.loop_start()

client.connect(settings['mqtt_adress'], port=settings['mqtt_port'])

#Allow time for connecting to MQTT. client.connect doesn't always await connection correctly
time.sleep(3)

for t in publish_list:
    client.publish(t[0], t[1])
