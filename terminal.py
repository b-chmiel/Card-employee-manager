import argparse
import sqlite3
import json
import time
import os
import socket
from datetime import datetime
import paho.mqtt.client as mqtt
from termcolor import colored
from dotenv import load_dotenv
from pathlib import Path

# Setting environmental variables
env_path = Path('./authentication') / '.env'
load_dotenv(dotenv_path=env_path)

#Setting authentication
username = os.getenv('CLIENT_USERNAME')
password = os.getenv('CLIENT_PASSWORD')
broker = socket.gethostname()
print(broker)
client = mqtt.Client()
port = 8883
client.tls_set("/etc/mosquitto/certs/ca.crt")
client.username_pw_set(username=username, password=password)

terminalID = 0


def getTime():
    return "[ " + datetime.now().strftime("%X") + " ]"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "terminalID", help="TerminalID which will be emulated", type=int)
    args = parser.parse_args()

    global terminalID
    terminalID = args.terminalID

    time_left = 20
    print("Connecting to mosquitto...")
    while time_left != 0:
        try:
            client.connect(broker, port)
            break
        except Exception as e:
            print("Waiting for mosquitto: ", time_left)
            time_left -= 1
            time.sleep(1)

    if time_left == 0:
        print(colored("Cannot connect to mosquitto", 'red'))
        print(colored("Run command \'sudo service mosquitto start\'", 'yellow'))
        print(colored("If mosquitto service is already running:", 'yellow'))
        print(colored("run \'sudo ./authentication/authCreate.sh\' and configure ssl properly", 'yellow'))
        exit()

    print(colored("Connected", 'green'), getTime())
    client.connected_flag = False
    client.on_message = on_message
    id_topic = "ID/get/" + str(terminalID)
    card_topic = "card/get/" + str(terminalID)
    client.subscribe(card_topic)
    client.subscribe(id_topic)

    time_left = 20
    client.loop_start()
    while (not client.connected_flag) and (time_left != 0):
        print("Waiting for mqttBroker.py...", time_left, "s")
        client.publish("ID/post", str(terminalID))

        time.sleep(1)
        time_left -= 1

    if time_left == 0:
        print(colored("Cannot connect to mqttBroker.py", 'red'))
        print(colored("Run \'python3 mqttBroker.py\'", 'yellow'))
        exit()

    client.loop_stop()
    while True and not client.bad_connection_flag:
        client.loop_forever()


def on_message(client, userdata, message):
    txt_message = str(message.payload.decode("utf-8", "ignore"))
    id_topic = "ID/get/" + str(terminalID)
    client.connected_flag = True
    client.bad_connection_flag = False
    if message.topic == id_topic:
        if txt_message == "False":
            print(
                colored("In order to use this terminal please first register it!", 'red'))
            client.bad_connection_flag = True
            return

    elif message.topic == ("card/get/" + str(terminalID)):
        if len(txt_message) > 1:
            print(getTime(), "   ", txt_message)

    cardID = input("Please provide card character or \'exit\' keyword >> ")
    if cardID != 'exit':
        to_send = {"terminalID": terminalID, "cardID": cardID}
        client.publish("card/post", json.dumps(to_send))
    else:
        client.bad_connection_flag = True


if __name__ == "__main__":
    main()
