# Garage door controller

This is the software part of my garage door controller.

There are lots of projects like this outside. What I was missing was the presence
of dedicated *open* and *close* buttons. When I'm leaving my house and don't see
the door, i wish to press the *open* button and when I arrive outside at my
garage, I want that the door is open (and not closed, because it's already open
when I pressed the button). The software should control the door engine in that
way, that the achieved position is reached, regardless in which state the doors
currently is.

**Examples:**

The door is open and I press the open button; the controller should do nothing.

The door is moving down and I press the open button; the controller should trigger
the engine to stop it, wait and trigger again to move to door up.

## Hardware

This application assumes, that the door engine is controlled via one button.
Furthermore, limit switches are necessary, to detect, if the door is in the
upper or lower position.

I use a Raspberry Pi with an relay to connect the door hardware. Other python
enabled computers are possible, too. Only the driver part should be created.

My external circuit looks like this:

![Schematic](docs/hardware_schematic.svg)

## Software

The software is split in multiple parts.

1. The controller with web service.
1. A single page app as frontend.

### The controller

This part is written in Python. Use `python controller.py` to start the software.

The configuration is done in `config.json`.

    {
      "door-list": [
        {
          "name": "Door 1",
          "driver": {
            "class": "RPiDriver",
            "gpioRelay": 18,
            "gpioUpperLimitSwitch": 17,
            "gpioLowerLimitSwitch": 27
          },
          "transitTime": 17,
          "triggerTime": 1.5,
          "accelerateTime": 4
        }
      ],
      "allowed-users": [
        {
          "username": "user",
          "password": "pass1"
        }
      ]
    }

The array `door-list` describes the connected doors. Multiple doors are possible.

**name** The name of the door, a.e. "left door" or "lamborghini"

**driver** The hardware driver. They are located in `/garage/door`
and must implement the Driver interface.

**driver.class** The class name of the driver. See `/garage/door/rpi_driver.py`

**driver.gpioRelay** The GPIO pin for the Raspbeery Pi driver to control the relay.

**driver.gpioUpperLimitSwitch** and **gpioLowerLimitSwitch** The GPIO pins for
the Raspbeery Pi driver to check the limit switches.

**transitTime** The time in seconds, the door needs to move from upper to lower
position or vice versa.

**triggerTime** The time in seconds, the relay will be triggerd.

**accelerateTime** The time in seconds, after which the door will be moved off of
the limit switches.

## Setup

    sudo apt-get install python-pip
    sudo pip install blinker
    sudo pip install web.py
    git clone https://github.com/Mik-/garage-door-controller.git garage
    cd garage

Edit your `config.json`.

    sudo python controller.py
