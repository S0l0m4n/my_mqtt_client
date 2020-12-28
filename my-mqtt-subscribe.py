#!/usr/bin/python3

import pdb
#pdb.set_trace()

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from MyMqttClient import MyMqttClient
import time

HOST_DEV = "ag8zxd6iafu8d-ats.iot.eu-west-1.amazonaws.com"
HOST_PROD = "a1d18d1xa0vfcy-ats.iot.eu-west-1.amazonaws.com"

parser = ArgumentParser(
    formatter_class=RawDescriptionHelpFormatter,
    description=
    """
    Subscribe to a topic on AWS IoT Core

    Example: ./%(prog)s --host=dev --creds=dev command/unit1

    NOTE: You must supply the following files in the "cred" directory:
      clicrt.txt    client certificate
      clikey.txt    client private key
      rootca.txt    Amazon CA root certificate
    """)

parser.add_argument('--host', choices=['dev','prod'], help='host to connect to')
parser.add_argument('--creds', metavar='<creds>', help='dir containing creds')
parser.add_argument('topic', metavar='<topic>', help='topic to subscribe to')

args = parser.parse_args()

if args.host == "prod":
    host = HOST_PROD
else:
    host = HOST_DEV

x = MyMqttClient(host, creds=args.creds)
x.subscribe(args.topic)
n = x.getNumMessages()

while True:
    if n != x.getNumMessages():
        n = x.getNumMessages()
        curr_time = time.strftime("%H:%M:%S", time.localtime())
        print("#msgs = {}".format(n))
        print("[{0}] {1}".format(curr_time, x.getLastMessage()))
    time.sleep(1)
