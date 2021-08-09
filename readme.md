Prerequisites:
This program will only get your sensor data from the cloud, it will not connect directly to the sensors. 
This means you need an Airthings account, and a way of syncing the data to the cloud. The simplest 
method being their Airthings Hub. Having the app on your phone will also sync to the cloud, albeit with a delay

You also need to have a dashboard set up on dashboard.airthings.com with a tile that looks like this:
https://i.imgur.com/glDnnK3.png
Note that the selected location and room (workplace/living room in the screenshot) will make up the MQTT-topic


Installation:
This is a Python program and has been developed on Python 3.8.3. The requirements.txt contains packages known to work
with this program

Download or clone the script. On first run make sure you run it with the "--setup" flag to enter credentials for 
your account and MQTT-broker. This information is stored locally in the directory in a file named "settings.json".

During the setup-run the program will check connection and returned the discovered sensors and their corresponding
MQTT-topics for setting up in your software of choice.

After first setup the program can be automated to run on a schedule using cron or Windows Task Scheduler depending
on your OS. 


Credits:
This script would not be possible without the foundation of this program: https://github.com/Danielhiversen/home_assistant_airthings_cloud

Daniel had already set up the connections to the API and the data structures. I've simply moved the output to be MQTT.