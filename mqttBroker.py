import paho.mqtt.client as mqtt

import backend.manageBack
import backend.terminalBack

client_name = "Client1"
host_name = "192.168.0.41"
client = mqtt.Client(client_name)
client.connect(host_name)


def receive():
    pass


def send():
    pass


def main():
    pass


if __name__ == "__main__":
    main()