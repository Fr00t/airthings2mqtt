###About
This program will transfer data from Airthings sensors such as the [Wave Mini](https://www.airthings.com/en/wave-mini) 
or [Wave Plus](https://www.airthings.com/en/wave-plus) via their Dashboard to a MQTT-broker of your choice.

###Prerequisites:
This program will only get your sensor data from the cloud, it will not connect directly to the sensors. This means you need an Airthings account, and a way of syncing the data to the cloud. The simplest method being their [Airthings Hub](https://www.airthings.com/en/hub) or the [View Plus](https://www.airthings.com/en/view-plus). Having the app on your phone and connected to the sensor will also sync to the cloud, albeit with a delay.

You also need to have a dashboard set up on [https://dashboard.airthings.com](https://dashboard.airthings.com) 
with a tile that looks like this:
![Dashboard tile](https://i.imgur.com/glDnnK3.png)

Note that the selected location and room (workplace/living room in the screenshot) will make up part of the MQTT-topic.

###Installation:
This is a Python program and has been developed on Python 3.8.3. 

1. Download or clone the script. 
2. Install necessary packages from requirements.txt using `pip install -r requirements.txt`
3. Run setup.py to set up and test connections to Airthings and broker: `python setup.py` The information is stored locally in the directory in a file named `settings.json`.
4. Run `airthings2mqtt.py` on a schedule using Cron or equivalent.


###Credits:
This script would not be possible without the foundation of this program: https://github.com/Danielhiversen/home_assistant_airthings_cloud

Daniel had already set up the connections to the API and the data structures. I've simply moved the output to be MQTT.