try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Garage door opener',
    'author': 'Michael Neuendorf',
    'url': 'www.neuendorf-online.de',
    'download_url': 'www.neuendorf-online.de',
    'author_email': 'michael@neuendorf-online.de',
    'version': '0.1',
    'install_requires': ['nose', 'RPi.GPIO', 'blinker'],
    'packages': ['garage'],
    'scripts': [],
    'name': 'garage'
}

setup(**config)
