import paho.mqtt.client as mqtt
import json
import time
import os
from datetime import datetime
from termcolor import colored
from dotenv import load_dotenv
from pathlib import Path

import backend.terminalBack as terminalBack

# Setting environmental variables
env_path = Path('./authentication') / '.env'
load_dotenv(dotenv_path=env_path)

#Setting authentication
username = os.getenv('SERVER_USERNAME')
password = os.getenv('SERVER_PASSWORD')
broker = "Incvisius"
client = mqtt.Client()
port = 8883
client.tls_set("/etc/mosquitto/certs/ca.crt")
client.username_pw_set(username=username, password=password)


def getTime():
    return "[ " + datetime.now().strftime("%X") + " ]"


def main():
    time_left = 10
    print("Connecting to mosquitto...")
    while time_left > 0:
        try:
            client.connect(broker, port)
            break
        except Exception as e:
            print("Waiting for mosquitto: ", time_left, "s")
            time_left -= 1
            time.sleep(1)

    if time_left == 0:
        print(colored("Cannot connect to mosquitto", 'red'))
        print(colored("Run command \'sudo service mosquitto start\'", 'yellow'))
        exit()

    print(colored("Connected", 'green'), getTime())
    print("Waiting for terminal to connect...")
    client.on_message = on_message
    client.subscribe("ID/post")
    client.subscribe("card/post")

    client.loop_forever()


def on_message(client, userdata, message):
    txt_message = str(message.payload.decode("utf-8", "ignore"))
    if message.topic == "ID/post":
        topic = "ID/get/" + str(txt_message)
        if not terminalBack.is_terminal_existing(int(txt_message)):
            client.publish(topic, "False")
            txt = f"Unregistered terminal {txt_message} detected"
            print(colored(txt, 'red'))
            txt = f"Register it using \'python3 manage.py add -t {txt_message}\'"
            print(colored(txt, 'red'))
        else:
            client.publish(topic, "True")
            txt = f"Connected terminal: {txt_message}"
            print(colored(txt, 'green'))
    elif message.topic == "card/post":
        result = json.loads(txt_message)
        terminalID = result['terminalID']
        cardID = result['cardID']
        message = ""
        if len(cardID) != 1:
            print("Received message: ", result, "   ", getTime())
            message = "Incorrect card ID!"
        else:
            print("Received message: ", result, "   ", getTime())
            message = str(terminalBack.run(terminalID, cardID))
        topic = "card/get/" + str(terminalID)
        client.publish(topic, message)


if __name__ == "__main__":
    main()
