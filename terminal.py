import argparse
import sqlite3
import paho.mqtt.client as mqtt

import backend.terminalBack as terminalBack

client_name = "Terminal"
host_name = "localhost"
client = mqtt.Client(client_name)
client.connect(host_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("terminalID", help="TerminalID which will be emulated", type=int)
    args = parser.parse_args()

    client.publish("system/terminal/ID", str(args.terminalID))
    client.subscribe("system/terminal/ID")
    client.on_message=on_message
    client.loop_forever()

    client.connect(host_name)

    client.unsubscribe("system/terminal/ID")
    client.subscribe("system/terminal/card")
    client.on_message=on_message_card

    
    cardID = ""
    while cardID != 'exit':
        cardID = input("Please provide card character or exit keyword >> ")
        client.publish("system/terminal/card", str(cardID))
        client.loop()

    client.loop_stop()
    client.disconnect()

def on_message(client, userdata, message):
    print(1)
    txt_message = str(message.payload.decode("utf-8"))
    if txt_message == "False":
        print("In order to use this terminal please first register it!")
        exit()    
    client.disconnect()      


def on_message_card(client, userdata, message):
    print(2)
    txt_message = str(message.payload.decode("utf-8"))
    if len(txt_message) > 0:
        print(txt_message)  
    client.loop_stop()  


if __name__ == "__main__":
    main()   