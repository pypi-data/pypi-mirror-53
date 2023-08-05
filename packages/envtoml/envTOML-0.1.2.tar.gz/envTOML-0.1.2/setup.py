# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['envtoml']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'envtoml',
    'version': '0.1.2',
    'description': 'A simple way of using environment variables in TOML configs (via interpolation)',
    'long_description': 'envTOML\n=======\n\n.. image:: https://img.shields.io/pypi/v/envtoml.svg\n    :target: https://pypi.python.org/pypi/envtoml\n    :alt: PyPI Status\n\n.. image:: https://img.shields.io/travis/mrshu/envtoml.svg\n    :target: https://travis-ci.org/mrshu/envtoml\n    :alt: Build Status\n\n.. image:: https://coveralls.io/repos/github/mrshu/envtoml/badge.svg?branch=master\n    :target: https://coveralls.io/github/mrshu/envtoml?branch=master\n    :alt: Code coverage Status\n\n.. image:: https://img.shields.io/pypi/l/envtoml.svg\n   :target: ./LICENSE\n   :alt: License Status\n\n``envTOML`` is an answer to a fairly simple problem: including values from\nenvironment variables in TOML configuration files. In this way, it is very\nsimilar to both `envyaml <https://github.com/thesimj/envyaml>`_ and\n`varyaml <https://github.com/abe-winter/varyaml>`_ which provide very\nsimilar functionality for YAML and which greatly inspired this small\npackage.\n\nExample\n-------\n\nSuppose we have the following configuration saved in ``config.toml``\n\n.. code:: toml\n\n  [db]\n  host = "$DB_HOST"\n  port = "$DB_PORT"\n  username = "$DB_USERNAME"\n  password = "$DB_PASSWORD"\n  name = "my_database"\n\nwith the environment variables being set to the following\n\n.. code::\n\n  DB_HOST=some-host.tld\n  DB_PORT=3306\n  DB_USERNAME=user01\n  DB_PASSWORD=veryToughPas$w0rd\n\nthis config can then be parsed with ``envTOML`` in the following way:\n\n\n.. code:: python\n\n  import envtoml\n\n  cfg = envtoml.load(open(\'./config.toml\'))\n\n  print(cfg)\n  # {\'db\': {\'host\': \'some-host.tld\',\n  #   \'port\': 3306,\n  #   \'username\': \'user01\',\n  #   \'password\': \'veryToughPas$w0rd\',\n  #   \'name\': \'my_database\'}}\n\nTests\n-----\n\nAs this project makes use of `Poetry <https://poetry.eustace.io/>`_, after\ninstalling it the tests can be ran by executing the following from the\nproject\'s root directory:\n\n.. code:: bash\n\n    poetry run nosetests tests\n\nThey can also be ran with `coverage <https://nose.readthedocs.io/en/latest/plugins/cover.html>`_:\n\n.. code:: bash\n\n    poetry run nosetests --with-coverage tests\n\n\nLicense\n-------\n\nLicensed under the MIT license (see `LICENSE <./LICENSE>`_ file for more\ndetails).\n',
    'author': 'mr.Shu',
    'author_email': 'mr@shu.io',
    'url': 'https://github.com/mrshu/envtoml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
