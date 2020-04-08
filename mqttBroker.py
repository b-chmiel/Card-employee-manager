import paho.mqtt.client as mqtt
import json

import backend.terminalBack as terminalBack

client_name = "Broker"
host_name = "localhost"
client = mqtt.Client(client_name)
client.connect(host_name)


def main():
    client.subscribe("terminal/ID/post")
    client.subscribe("terminal/card/post")
    client.on_message=on_message
    client.loop_forever()


def on_message(client, userdata, message):
    txt_message = str(message.payload.decode("utf-8", "ignore"))

    if message.topic == "terminal/ID/post":
        if not terminalBack.is_terminal_existing(int(txt_message)):
            client.publish("terminal/ID/get", "False")
        else:
            client.publish("terminal/ID/get", "True")
    if message.topic == "terminal/card/post":
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