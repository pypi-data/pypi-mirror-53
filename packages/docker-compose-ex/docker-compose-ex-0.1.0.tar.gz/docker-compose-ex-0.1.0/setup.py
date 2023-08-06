# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['docker_compose_ex']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.1,<6.0']

entry_points = \
{'console_scripts': ['docker-compose-ex = docker_compose_ex:compose_ext.main']}

setup_kwargs = {
    'name': 'docker-compose-ex',
    'version': '0.1.0',
    'description': 'Docker Compose with `extends` option',
    'long_description': '',
    'author': 'Vitaliy Kucheryaviy',
    'author_email': 'ppr.vitaly@gmail.com',
    'url': 'https://github.com/vitalik/docker-compose-ex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
