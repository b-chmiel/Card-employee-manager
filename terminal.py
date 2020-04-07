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

    client.unsubscribe("system/terminal/ID")
    client.subscribe("system/terminal/cardID")
    
    '''
    while cardID != 'exit':
        cardID = input("Please provide card character or exit keyword >> ")
        client.publish("system/terminal/cardID", str(cardID))
    '''
'''
    print("To exit write \"exit\"")
    while terminalBack.run(args.terminalID):
        pass
    
'''

def on_message(client, userdata, message):
    txt_message = str(message.payload.decode("utf-8"))
    if message.topic == "system/terminal/ID":
        if txt_message == "False":
            print("In order to use this terminal please first register it!")
            exit()    
    client.disconnect()      


if __name__ == "__main__":
    main()   