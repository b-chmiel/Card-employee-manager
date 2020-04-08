import argparse
import sqlite3
import json
import paho.mqtt.client as mqtt

import backend.terminalBack as terminalBack

client_name = "Terminal"
host_name = "localhost"
client = mqtt.Client(client_name)
client.connect(host_name)

terminalID = 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("terminalID", help="TerminalID which will be emulated", type=int)
    args = parser.parse_args()

    global terminalID
    terminalID = args.terminalID

    client.publish("terminal/ID/post", str(terminalID))
    client.subscribe("terminal/ID/get")
    client.subscribe("terminal/card/get")
    client.on_message=on_message
    client.loop_forever()


def on_message(client, userdata, message):
    txt_message = str(message.payload.decode("utf-8", "ignore"))
    if message.topic == "terminal/ID/get":
        if txt_message == "False":
            print("In order to use this terminal please first register it!")
            exit()        
    if message.topic == "terminal/card/get":
        if len(txt_message) > 1:
            print(txt_message)

    cardID = input("Please provide card character or \'exit\' keyword >> ")
    if cardID != 'exit':
        to_send = {"terminalID": terminalID, "cardID": cardID}
        client.publish("terminal/card/post", json.dumps(to_send))
    else:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()   