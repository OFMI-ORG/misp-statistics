 #!/usr/bin/env python3


import requests
from pymisp import ExpandedPyMISP
from configparser import ConfigParser
import json

## Configuation reading

config=ConfigParser()
config.read("config.ini")

## Configuration in config.ini


webhook_url=config["webhook"]["webhook_url"]
misp_url=config["misp"]["url"]
misp_key=config["misp"]["key"]
misp_verify=config["misp"].getboolean("verifycert")
misp_last=config["misp"]["last"]
limit=config["misp"].getint("limit")


def send_webhook(text):
    requests.post(webhook_url, json={"text": text})

misp=ExpandedPyMISP(url=misp_url, key=misp_key, ssl=misp_verify)

test = [0] * limit
page=1
event_count=0
while limit == len(test):
    test=misp.search(limit=config["misp"]["limit"], page=page, last=misp_last)
    event_count+=len(test)

message=f"Statistics: {event_count} events since {misp_last}"
send_webhook(message)
