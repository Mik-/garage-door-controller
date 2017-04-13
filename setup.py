try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Garage door opener',
    'author': 'Michael Neuendorf',
    'url': 'http://www.neuendorf-online.de',
    'download_url': 'www.neuendorf-online.de',
    'author_email': 'michael@neuendorf-online.de',
    'version': '0.1',
    'install_requires': ['RPi.GPIO', 'blinker', 'flask'],
    'packages': ['garage'],
    'py_modules': ['controller'],
    'data_files': [('/etc/init.d', ['scripts/garage-door-opener'])],
    'scripts': [],
    'name': 'garage'
}

setup(**config)
