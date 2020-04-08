import paho.mqtt.client as mqtt

import backend.terminalBack as terminalBack

client_name = "Broker"
host_name = "localhost"
client = mqtt.Client(client_name)
client.connect(host_name)

terminalID = 0


def main():
    client.subscribe("system/terminal/ID")
    client.on_message=on_message_id
    client.loop_forever()
    client.subscribe("system/terminal/card")
    client.on_message=on_message_card
    client.loop_forever()

    client.loop_stop()
    client.disconnect()

def on_message_id(client, userdata, message):
    txt_message = str(message.payload.decode("utf-8"))
    global terminalID 
    terminalID = int(txt_message)
    if not terminalBack.is_terminal_existing(terminalID):
        client.publish("system/terminal/ID", "False")
    else:
        client.publish("system/terminal/ID", "")
    client.loop_stop() 


def on_message_card(client, userdata, message):
    cardID = str(message.payload.decode("utf-8"))
    if len(cardID) != 1:
        client.publish("system/terminal/card", "Incorrect card ID!")
    
    client.publish("system/terminal/card", str(terminalBack.run(terminalID, cardID)))


if __name__ == "__main__":
    main()