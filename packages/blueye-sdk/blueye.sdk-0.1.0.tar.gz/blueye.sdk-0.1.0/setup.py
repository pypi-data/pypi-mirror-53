# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['blueye', 'blueye.sdk']

package_data = \
{'': ['*']}

install_requires = \
['blueye.protocol>=1.1.2,<2.0.0']

extras_require = \
{'examples': ['xbox360controller>=1.1.2,<2.0.0', 'asciimatics>=1.11.0,<2.0.0']}

setup_kwargs = {
    'name': 'blueye.sdk',
    'version': '0.1.0',
    'description': 'SDK for controlling a Blueye Pioneer',
    'long_description': '# blueye.sdk\n[![Tests](https://github.com/BluEye-Robotics/blueye.sdk/workflows/Tests/badge.svg)](https://github.com/BluEye-Robotics/blueye.sdk/actions)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n_________________\n\n[Read Latest Documentation](https://blueye-robotics.github.io/blueye.sdk/) - [Browse GitHub Code Repository](https://github.com/BluEye-Robotics/blueye.sdk)\n_________________\n\n**Note: This is a pre-release -- Please report any issues you might encounter**\n_________________\nA Python package for remote control of the Blueye Pioneer underwater drone.\n\n\n![SDK demo](./docs/media/sdk-demo.gif)\n\n# About The Pioneer\nThe Blueye Pioneer is a underwater drone designed for inspections. It is produced and sold by the Norwegian company [`Blueye Robotics`](https://www.blueyerobotics.com/).\nHere is a [`youtube video`](https://www.youtube.com/watch?v=_-AEtr6xOP8) that gives a overview of the system and its specifications.\n\n\n![Pioneer at the Tautra Reef](./docs/media/pioneer-at-reef.gif)\n\n## This SDK and the Pioneer\nThe Pioneer is normally controlled via a mobile device through the Blueye App ([iOS](https://apps.apple.com/no/app/blueye/id1369714041)/[Android](https://play.google.com/store/apps/details?id=no.blueye.blueyeapp)). The mobile device\nis connected via WiFi to a surface unit, and the Pioneer is connected to the surface unit via a tether cable.\n\nThis python SDK exposes the functionality of the Blueye app through a Python object. The SDK enables remote control of the Pioneer as well as reading telemetry data and viewing video streams, it is not meant for executing code on the Pioneer.\nTo control the Pioneer you connect your laptop to the surface unit WiFi and run code that interfaces with the Pioneer through the Pioneer Python object.\n\n\nCheck out the [`Quick Start Guide`](./docs/quick_start.md) to get started with using the SDK.\n',
    'author': 'Sindre Hansen',
    'author_email': 'sindre.hansen@blueye.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.blueyerobotics.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
