#!/usr/bin/env python

from garage.door.model import Door
import web
import logging
from optparse import OptionParser
import sys
import json
import importlib
import re
import base64

web.config.debug = False

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

urls = (
    '/doors', 'ListDoors',
    '/door/(.*)', 'DoorState',
    '/log', 'ShowLog',
    '/session', 'SessionManager',
    '/', 'Index'
)

app = web.application(urls, globals())

sessionStore = web.session.DiskStore('sessions')
session = web.session.Session(app, sessionStore, initializer={'login': 0})


class ListDoors:
    def OPTIONS(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Access-Control-Allow-Headers', 'X-Authorization, Content-Type')
        web.header('Access-Control-Allow-Methods', 'OPTIONS, GET')
        web.header('Access-Control-Max-Age', '1728000')
        return

    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')

        if session.login == 1:
            response = '{"doors": ['

            i = 1
            for door in door_list:
                if i <> 1:
                    response += ','
                response += '{"id": "%d", "name": "%s"}' % (i, door.name)
                i += 1

            response += ']}'

            return response
        else:
            return '{"error": "Not logged in!"}';

class DoorState:
    def OPTIONS(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Access-Control-Allow-Headers', 'X-Authorization, Content-Type')
        web.header('Access-Control-Allow-Methods', 'POST, OPTIONS, GET')
        web.header('Access-Control-Max-Age', '1728000')
        return

    def GET(self, door_id):
        if session.login == 1:
            id = int(door_id)
            response = '{"name": "%s","state": "%s","intent": "%s"}' % (
                door_list[id - 1].name, door_list[id - 1].state.__class__.__name__,
                door_list[id - 1].intent.__class__.__name__)
        else:
            response = '{"error": "not logged in"}'

        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')

        return response

    def POST(self, door_id):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')

        if session.login == 1:
            id = int(door_id)

            post_data = json.loads(web.data())

            if 'trigger' in post_data and post_data['trigger'] == True:
                door_list[id - 1].start_door_signal()
            elif 'intent' in post_data and post_data['intent'] == 'open':
                door_list[id - 1].set_intent('Open')
            elif 'intent' in post_data and post_data['intent'] == 'close':
                door_list[id - 1].set_intent('Close')
            elif 'intent' in post_data and post_data['intent'] == 'idle':
                door_list[id - 1].set_intent('Idle')
            else:
                return web.notfound("Invalid post command!")
        else:
            return '{"error": "not logged in"}'

class ShowLog:
    def OPTIONS(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Access-Control-Allow-Headers', 'X-Authorization, Content-Type')
        web.header('Access-Control-Allow-Methods', 'OPTIONS, GET')
        web.header('Access-Control-Max-Age', '1728000')
        return

    def GET(self):

        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')

        if session.login == 1:
            try:
                f = open('garage.log', 'r');
                return f.read()
            except IOError:
                return 'can not open garage.log'
        else:
            return 'Not logged in!'

class SessionManager:
    def OPTIONS(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Access-Control-Allow-Headers', 'X-Authorization, Content-Type')
        web.header('Access-Control-Allow-Methods', 'POST, OPTIONS, GET')
        web.header('Access-Control-Max-Age', '1728000')
        return

    def GET(self):
        if session.login == 0:
            response = '{"loggedIn": false }'
        else:
            response = '{"loggedIn": true }'

        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return response

    def POST(self):
        username = '-'
        password = '-'

        post_data = json.loads(web.data())

        if 'logout' in post_data and post_data['logout'] == True:
            session.login = 0
        else:
            if 'username' in post_data:
                username = post_data['username']
            if 'password' in post_data:
                password = post_data['password']

            if (username, password) in allowed_users:
                session.login = 1
            else:
                session.login = 0

        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return

class Index:
    def GET(self):
        raise web.seeother('/static/index.html')

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

    app.run()


    for door in door_list:
        door.cleanup()
