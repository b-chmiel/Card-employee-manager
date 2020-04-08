import paho.mqtt.client as mqtt
import json
import time

import backend.terminalBack as terminalBack

client_name = "Broker"
host_name = "localhost"
client = mqtt.Client(client_name)


def main():
    time_left = 10
    print("Connecting to mosquitto...")
    while time_left > 0:
        try:    
            client.connect(host_name)
            break
        except:
            print("Waiting for mosquitto: ", time_left, "s")
            time_left -= 1
            time.sleep(1)

    if time_left == 0:
        print("Cannot connect to mosquitto")
        exit()

    print("Connected")
    print("Waiting for terminal to connect...")
    client.on_message=on_message
    client.subscribe("terminal/ID/post")
    client.subscribe("terminal/card/post")
    
    client.loop_forever()


def on_message(client, userdata, message):
    txt_message = str(message.payload.decode("utf-8", "ignore"))

    if message.topic == "terminal/ID/post":
        if not terminalBack.is_terminal_existing(int(txt_message)):
            client.publish("terminal/ID/get", "False")
        else:
            client.publish("terminal/ID/get", "True")
        print("Connected terminal: ", int(txt_message))    
    elif message.topic == "terminal/card/post":
        result = json.loads(txt_message)
        terminalID = result['terminalID']
        cardID = result['cardID']
        if len(cardID) != 1:
            print(result)
            client.publish("terminal/card/get", "Incorrect card ID!") 
        else:
            print(result)
            client.publish("terminal/card/get", str(terminalBack.run(terminalID, cardID)))  


if __name__ == "__main__":
    main()