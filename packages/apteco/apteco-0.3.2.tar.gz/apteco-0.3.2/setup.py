# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['apteco']

package_data = \
{'': ['*'], 'apteco': ['data/*']}

install_requires = \
['apteco-api>=0.1.7,<0.2.0', 'pysimplegui>=4.0,<5.0']

setup_kwargs = {
    'name': 'apteco',
    'version': '0.3.2',
    'description': 'A Python package for interacting with Apteco Marketing Suite resources via the Apteco API.',
    'long_description': 'Getting Started\n===============\n\nRequirements\n------------\n\n* Python 3.6+\n* Access to an installation of the Apteco API\n\nThe Apteco API (which also goes under the name **Orbit API**)\nis part of the Apteco Orbit™ installation.\nIf you have access to Apteco Orbit™, you also have access to the Apteco API!\nIf you\'re not sure about this, contact whoever administers your Apteco software,\nor get in touch with Apteco support (support@apteco.com).\n\nInstallation\n------------\n\nYou can install the package the usual way from PyPI using ``pip``:\n\n.. code-block:: python\n\n   pip install apteco\n\nLogging in\n----------\n\nYour login credentials are the same username and password\nyou would use to log in to Apteco Orbit™:\n\n.. code-block:: python\n\n   from apteco.session import login, Session\n\n   credentials = login("https://my-site.com/OrbitAPI", "my_data_view", "jdoe")\n   holidays = Session(credentials, "holidays")\n\nYou will be asked to enter your password in the terminal, which won\'t be echoed.\nIf Python is unable to ask for your password in this way,\nit will provide a pop-up box instead.\nThis might appear in the background,\nso check your taskbar for a new window if nothing seems to be happening.\n\nIf you don\'t want to enter your password every time,\nthere is also a ``login_with_password()`` function which takes your password\nas a fourth argument:\n\n.. code-block:: python\n\n   from apteco.session import login_with_password\n\n   # password is in plain sight in the code!\n   credentials = login_with_password(\n       "https://my-site.com/OrbitAPI", "my_data_view", "jdoe", "password"\n   )\n   holidays = Session(credentials, "holidays")\n\n',
    'author': 'Apteco Ltd',
    'author_email': 'support@apteco.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
