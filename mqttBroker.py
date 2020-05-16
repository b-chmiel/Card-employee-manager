import paho.mqtt.client as mqtt
import json
import time

import backend.terminalBack as terminalBack


broker = "DESKTOP-KQ5BG8O"
broker = "Incvisius"
client = mqtt.Client()
port = 8883
client.tls_set("/etc/mosquitto/certs/ca.crt")
client.username_pw_set(username='server', password='password')


def main():
    time_left = 10
    print("Connecting to mosquitto...")
    while time_left > 0:
        try:
            client.connect(broker, port)
            break
        except Exception as e:
            print(e)
            print("Waiting for mosquitto: ", time_left, "s")
            time_left -= 1
            time.sleep(1)

    if time_left == 0:
        print("Cannot connect to mosquitto")
        exit()

    print("Connected")
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
        else:
            client.publish(topic, "True")
        print("Connected terminal: ", int(txt_message))
    elif message.topic == "card/post":
        result = json.loads(txt_message)
        terminalID = result['terminalID']
        cardID = result['cardID']
        message = ""
        if len(cardID) != 1:
            print("Received message: ", result)
            message = "Incorrect card ID!"
        else:
            print("Received message: ", result)
            message = str(terminalBack.run(terminalID, cardID))
        topic = "card/get/" + str(terminalID)
        client.publish(topic, message)


if __name__ == "__main__":
    main()
