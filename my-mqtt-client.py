#!/usr/bin/python3

import pdb
#pdb.set_trace()

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from MyMqttClient import MyMqttClient
import time

parser = ArgumentParser(
    formatter_class=RawDescriptionHelpFormatter,
    description=
    """
    Subscribe to a topic on AWS IoT Core

    Example: ./%(prog)s telemetry/unit1

    Note: You must supply the following files in this directory:
      clicrt.txt    client certificate
      clikey.txt    client private key
      rootca.txt    Amazon CA root certificate
    """)

parser.add_argument('topic', action='store', metavar='<topic>', type=str,
    help='topic to subscribe to')

args = parser.parse_args()

x = MyMqttClient()
x.subscribe(args.topic)

n = x.getNumMessages()

while True:
    if n != x.getNumMessages():
        n = x.getNumMessages()
        print("#msgs = {}".format(n))
        print(x.getMessages())
    time.sleep(1)
