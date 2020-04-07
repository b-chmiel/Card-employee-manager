import paho.mqtt.client as mqtt

import backend.terminalBack

client_name = "Broker"
host_name = "localhost"
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