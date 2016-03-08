#!/usr/bin/env python

from garage.door.model import Door
from functools import wraps
from flask import Flask, request, Response
import logging
from optparse import OptionParser
import sys
import json
import importlib
import re
import base64

logger = logging.getLogger('garage')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

filehandler = logging.FileHandler('garage.log')
filehandler.setLevel(logging.DEBUG)
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)

config_filename = 'config.json'
door_list = []
allowed_users = []

app = Flask(__name__)

# Authentication
def check_auth(username, password):
    """Check the username and password"""
    return (username, password) in allowed_users

def authenticate():
    return Response('Could not verfiy your access level', 401,
    {'WWW-Authenticate': 'Basic realm="Login required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'accept,content-type,authorization'
    return response

@app.route('/doors')
@requires_auth
def getDoors():
    json = '{"doors": ['

    i = 1
    for door in door_list:
        if i <> 1:
            json += ','
        json += '{"id": "%d", "name": "%s"}' % (i, door.name)
        i += 1

    json += ']}'

    resp = Response(json)
    resp.headers['Content-Type'] = 'application/json'

    return resp

@app.route('/door/<int:door_id>', methods=['GET'])
@requires_auth
def getDoor(door_id):
    json = '{"name": "%s","state": "%s","intent": "%s"}' % (
        door_list[door_id - 1].name, door_list[door_id - 1].state.__class__.__name__,
        door_list[door_id - 1].intent.__class__.__name__)

    resp = Response(json)
    resp.headers['Content-Type'] = 'application/json'

    return resp

@app.route('/door/<int:door_id>', methods=['POST'])
@requires_auth
def postDoor(door_id):
    post_data = request.get_json()

    if 'trigger' in post_data and post_data['trigger'] == True:
        door_list[door_id - 1].start_door_signal()
    elif 'intent' in post_data and post_data['intent'] == 'open':
        door_list[door_id - 1].set_intent('Open')
    elif 'intent' in post_data and post_data['intent'] == 'close':
        door_list[door_id - 1].set_intent('Close')
    elif 'intent' in post_data and post_data['intent'] == 'idle':
        door_list[door_id - 1].set_intent('Idle')
    else:
        return Response("Invalid post command!", 404)

    return Response("")

@app.route('/door/<int:door_id>', methods=['OPTIONS'])
def getDoorOptions(door_id):
    resp = Response()

    return resp

@app.route('/login', methods=['GET'])
@requires_auth
def getLogin():
    resp = Response('{"login": "ok"}')
    resp.headers['Content-Type'] = 'application/json'

    return resp

@app.route('/login', methods=['OPTIONS'])
def getLoginOptions():
    resp = Response()

    return resp

def init():
    # Process config file
    with open(config_filename) as json_data_file:
        config_data = json.load(json_data_file)

    for door_config in config_data["door-list"]:
        if door_config["driver"]["class"] == "MockDriver":
            # Instantiate mock driver
            mockdriver_module = importlib.import_module("tests.mock_driver")
            driver = getattr(mockdriver_module, "MockDriver")()
        elif door_config["driver"]["class"] == "RPiDriver":
            # Instantiate RPi driver
            rpidriver_module = importlib.import_module("garage.door.rpi_driver")
            driver = getattr(rpidriver_module, "RPiDriver")(
                door_config["driver"]["gpioRelay"],
                door_config["driver"]["gpioUpperLimitSwitch"],
                door_config["driver"]["gpioLowerLimitSwitch"])

        new_door = Door(door_config["name"], driver, door_config["transitTime"],
            door_config["triggerTime"], door_config["accelerateTime"])
        door_list.append(new_door)

    for user in config_data["allowed-users"]:
        allowed_users.append((user["username"], user["password"]))


if __name__ == "__main__":
    # Parse the command line options
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="config_filename", help="config filename; defaults to config.json")
    (options, args) = parser.parse_args()

    if options.config_filename:
        config_filename = options.config_filename

    # args contains the remaining options. Assign args to sys.argv to hand them
    # over to the web app
    sys.argv = args

    init()

    app.run(host="0.0.0.0", port=8080)

    for door in door_list:
        door.cleanup()
