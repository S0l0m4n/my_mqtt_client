#!/usr/bin/python3

import pdb
#pdb.set_trace()

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from MyMqttClient import MyMqttClient

HOST_DEV = "ag8zxd6iafu8d-ats.iot.eu-west-1.amazonaws.com"
HOST_PROD = "a1d18d1xa0vfcy-ats.iot.eu-west-1.amazonaws.com"
HOST_QA = "abz61otkz1ry8-ats.iot.eu-west-1.amazonaws.com"

parser = ArgumentParser(
    formatter_class=RawDescriptionHelpFormatter,
    description=
    """
    Publish to a topic on AWS IoT Core

    Example: ./%(prog)s --host=dev --topic dbg/00100018 pic:list

    NOTE: Supply these files in a matching "dev", "prod" or "qa" directory:
      clicrt.txt    client certificate
      clikey.txt    client private key
      rootca.txt    Amazon CA root certificate
    """)

parser.add_argument(
        '--host', choices=['dev','prod','qa'], help='host to connect to')
parser.add_argument('--topic', metavar='<topic>', help='topic to subscribe to')
parser.add_argument('payload', metavar='<payload>', help='data to publish')

args = parser.parse_args()

if args.host == "prod":
    host = HOST_PROD
elif args.host == "qa":
    host = HOST_QA
else:
    host = HOST_DEV

x = MyMqttClient(host, creds=args.host, verbose=False)

x.publish(args.topic, args.payload)
