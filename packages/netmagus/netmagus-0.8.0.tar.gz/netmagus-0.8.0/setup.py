# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['netmagus']

package_data = \
{'': ['*']}

install_requires = \
['autobahn-sync>=0.3,<0.4', 'autobahn>=19.10,<20.0']

setup_kwargs = {
    'name': 'netmagus',
    'version': '0.8.0',
    'description': 'Python module for JSON data exchange via files or RPC with the Intelligent Visibility NetMagus system.',
    'long_description': 'NetMāgus Python Package\n=======================\n\n| |Updates| |Python3| |BuildStatus|\n\n\nThis Python package is to be used with the `NetMāgus <http://www.intelligentvisibility.com/netmagus>`_ product from `Intelligent Visbility, Inc <http://www.intelligentvisibility.com>`_.\n\nIt is used to create and exchange UI forms and Formula steps with the NetMāgus application.\n\nThe code has been tested and should work for both Python 2.7 and 3.5+.\n\nTo install, simply use ``pip install netmagus``\n\nRefer to the `NetMāgus <http://www.intelligentvisibility.com/netmagus>`_ documentation for usage details.\n\n.. |Updates| image:: https://pyup.io/repos/github/rbcollins123/netmagus_python/shield.svg?token=fffb8c76-e275-451f-8ce0-1ec463f6d650\n    :target: https://pyup.io/repos/github/rbcollins123/netmagus_python/\n     :alt: Updates\n\n.. |Python3| image:: https://pyup.io/repos/github/rbcollins123/netmagus_python/python-3-shield.svg?token=fffb8c76-e275-451f-8ce0-1ec463f6d650\n    :target: https://pyup.io/repos/github/rbcollins123/netmagus_python/\n     :alt: Python3\n\n.. |BuildStatus| image:: https://travis-ci.com/rbcollins123/netmagus_python.svg?token=dqosS7xWadx9zSztAYMC&branch=master\n    :target: https://travis-ci.com/rbcollins123/netmagus_python/\n     :alt: Build Status',
    'author': 'Richard Collins',
    'author_email': 'richardc@intelligentvisibility.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.intelligentvisibility.com/netmagus/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
