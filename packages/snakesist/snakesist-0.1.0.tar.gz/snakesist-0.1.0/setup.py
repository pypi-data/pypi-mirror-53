# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['snakesist']

package_data = \
{'': ['*']}

install_requires = \
['delb>=0.1,<0.2', 'lxml>=4.3,<5.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'snakesist',
    'version': '0.1.0',
    'description': 'A Python database interface for eXist-db',
    'long_description': "snakesist\n=========\n\n.. image:: https://badge.fury.io/py/snakesist.svg\n    :target: https://badge.fury.io/py/snakesist\n\n.. image:: https://readthedocs.org/projects/snakesist/badge/?version=latest\n    :target: https://snakesist.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://travis-ci.org/03b8/snakesist.svg?branch=master\n    :target: https://travis-ci.org/03b8/snakesist\n\n\n``snakesist`` is a Python database interface for `eXist-db <https://exist-db.org>`_.\nIt supports creating, retrieving, updating and deleting and uses\n`delb <https://delb.readthedocs.io>`_ for representing the yielded resources.\n\n.. code-block:: shell\n\n    pip install snakesist\n\n\nUsage example\n-------------\n\n.. code-block:: python\n\n    from snakesist import ExistClient\n\n    db = ExistClient(\n        host='my.existdbinstance.org',  # defaults to 'localhost'\n        port='80',  # defaults to 8080\n        user='foo_bar',  # defaults to 'admin'\n        passwordw='f0ob4r'  # defaults to ''\n    )\n\n    db.root_collection = '/db/foo/bar'\n    # the client will only query from this point downwards\n\n    names = db.retrieve_resources('//*:persName')\n    # note the namespace wildcard in the XPath expression\n\n    # append 'Python' to all names which are 'Monty' and delete the rest\n    for name in names:\n        if name.node.full_text == 'Monty':\n            name.node.append_child(' Python')\n            name.update_push()\n        else:\n            name.delete()\n\n\nYour eXist instance\n-------------------\n\n``snakesist`` leverages the\n`eXist RESTful API <https://www.exist-db.org/exist/apps/doc/devguide_rest.xml>`_\nfor database queries. This means that allowing database queries using the\n``_query`` parameter of the RESTful API is a requirement in the used eXist-db\nbackend. eXist allows this by default, so if you haven't configured your\ninstance otherwise, don't worry about it.\n\n``snakesist`` is tested with eXist 4.7.1 and is not compatible yet with eXist 5.0.0.\n",
    'author': 'Theodor Costea',
    'author_email': 'theo.costea@gmail.com',
    'url': 'https://github.com/03b8/snakesist',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
