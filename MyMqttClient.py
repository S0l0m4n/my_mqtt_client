#!/usr/bin/python3

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import uuid

# Generate a random client id. I'm worried AWS IoT Core will kick this instance
# of the client off the server if someone else also uses this script at the same
# time.
MY_CLIENT_ID = "MyMqttClient-{0}".format(uuid.uuid4().hex[:8])

ROOTCA = "rootca.txt"
CLICRT = "clicrt.txt"
CLIKEY = "clikey.txt"

HOST = "ag8zxd6iafu8d-ats.iot.eu-west-1.amazonaws.com"
PORT = 8883

class MyMqttClient(AWSIoTMQTTClient):
    def __init__(self):
        super().__init__(MY_CLIENT_ID)

        self.messages = []

        self.configureEndpoint(HOST, PORT)
        self.configureCredentials(ROOTCA, CLIKEY, CLICRT)
        self.configureMQTTOperationTimeout(5)  # 5 sec

        self.connect()
        print("{0} is connected to {1}".format(MY_CLIENT_ID, HOST))

    def subscribe(self, topic):
        if (super().subscribe(topic, 1, self.subscribeCallback)):
            print('MyMqttClient is subscribed to "{}"'.format(topic))
            self.topic = topic
        else:
            print("ERROR with MQTT client subscribing")

    def subscribeCallback(self, client, userdata, message):
        self.messages.append(message.payload.decode())

    def getMessages(self):
        return self.messages

    def getNumMessages(self):
        return len(self.messages)

    def getLastMessage(self):
        return self.messages[-1]


if __name__ == "__main__":
    x = MyMqttClient()
    x.subscribe("telemetry/modem")
    n = x.getNumMessages()
    while True:
        if n != x.getNumMessages():
            n = x.getNumMessages()
            print("#msgs = {}".format(n))
            print(x.getMessages())
        time.sleep(2)
