#!/usr/bin/python3

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time

MY_CLIENT_ID = "MyMqttClient"

ROOTCA = "rootca.txt"
CLICRT = "clicrt.txt"
CLIKEY = "clikey.txt"

HOST = "ag8zxd6iafu8d-ats.iot.eu-west-1.amazonaws.com"
PORT = 8883
TOPIC = "telemetry"

class MyMqttClient(AWSIoTMQTTClient):
    def __init__(self, hubClientId):
        super().__init__(MY_CLIENT_ID)

        self.messages = []
        self.topic = TOPIC + "/" + hubClientId

        self.configureEndpoint(HOST, PORT)
        self.configureCredentials(ROOTCA, CLIKEY, CLICRT)
        self.configureMQTTOperationTimeout(5)  # 5 sec

        self.connect()

        if self.subscribe(self.topic, 1, self.subscribeCallback):
            print('MyMqttClient is subscribed to "{}"'.format(self.topic))
        else:
            print("ERROR with MQTT client subscribing")

    def subscribeCallback(self, client, userdata, message):
        self.messages.append(message.payload)

    def getMessages(self):
        return self.messages

    def getNumMessages(self):
        return len(self.messages)


if __name__ == '__main__':
    x = MyMqttClient("python")
    n = x.getNumMessages()
    while True:
        if n != x.getNumMessages():
            n = x.getNumMessages()
            print("#msgs = {}".format(n))
            print(x.getMessages())
        time.sleep(2)
