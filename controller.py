#!/usr/bin/env python

import sys
import json
import logging
import importlib
from optparse import OptionParser
import web
from garage.door.model import Door

web.config.debug = False

LOGGER = logging.getLogger('garage')
LOGGER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

FILEHANDLER = logging.FileHandler('garage.log')
FILEHANDLER.setLevel(logging.DEBUG)
FILEHANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(FILEHANDLER)

CONFIG_FILENAME = 'config.json'
DOOR_LIST = []
ALLOWED_USERS = []

URLS = (
    '/doors', 'ListDoors',
    '/door/(.*)', 'DoorState',
    '/log', 'ShowLog',
    '/session', 'SessionManager',
    '/', 'Index'
)

APP = web.application(URLS, globals())

SESSION_STORE = web.session.DiskStore('sessions')
SESSION = web.session.Session(APP, SESSION_STORE, initializer={'login': 0})

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

        if SESSION.login == 1:
            response = '{"doors": ['

            i = 1
            for door in DOOR_LIST:
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
        if SESSION.login == 1:
            id = int(door_id)
            response = '{"name": "%s","state": "%s","intent": "%s"}' % (
                DOOR_LIST[id - 1].name, DOOR_LIST[id - 1].state.__class__.__name__,
                DOOR_LIST[id - 1].intent.__class__.__name__)
        else:
            response = '{"error": "not logged in"}'

        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')

        return response

    def POST(self, door_id):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')

        if SESSION.login == 1:
            id = int(door_id)

            post_data = json.loads(web.data())

            if 'trigger' in post_data and post_data['trigger'] == True:
                DOOR_LIST[id - 1].start_door_signal()
            elif 'intent' in post_data and post_data['intent'] == 'open':
                DOOR_LIST[id - 1].set_intent('Open')
            elif 'intent' in post_data and post_data['intent'] == 'close':
                DOOR_LIST[id - 1].set_intent('Close')
            elif 'intent' in post_data and post_data['intent'] == 'idle':
                DOOR_LIST[id - 1].set_intent('Idle')
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

        if SESSION.login == 1:
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
        if SESSION.login == 0:
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
            SESSION.login = 0
        else:
            if 'username' in post_data:
                username = post_data['username']
            if 'password' in post_data:
                password = post_data['password']

            if (username, password) in ALLOWED_USERS:
                SESSION.login = 1
            else:
                SESSION.login = 0

        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return

class Index:
    def GET(self):
        raise web.seeother('/static/index.html')

def init():
    # Process config file
    with open(CONFIG_FILENAME) as json_data_file:
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
        elif door_config["driver"]["class"] == "PiGpioDriver":
            # Instantiate PiGpio driver
            rpidriver_module = importlib.import_module("garage.door.pigpio_driver")
            driver = getattr(rpidriver_module, "PiGpioDriver")(
                door_config["driver"]["host"],
                door_config["driver"]["gpioRelay"],
                door_config["driver"]["gpioUpperLimitSwitch"],
                door_config["driver"]["gpioLowerLimitSwitch"])

        new_door = Door(door_config["name"], driver, door_config["transitTime"],
                        door_config["triggerTime"], door_config["accelerateTime"])
        DOOR_LIST.append(new_door)

    for user in config_data["allowed-users"]:
        ALLOWED_USERS.append((user["username"], user["password"]))


if __name__ == "__main__":
    # Parse the command line options
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="config_filename", 
                      help="config filename; defaults to config.json")
    (options, args) = parser.parse_args()

    if options.config_filename:
        CONFIG_FILENAME = options.config_filename

    # args contains the remaining options. Assign args to sys.argv to hand them
    # over to the web app
    sys.argv = args

    init()

    APP.run()


    for door in DOOR_LIST:
        door.cleanup()
