# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyuscf']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'pyuscf',
    'version': '0.2.1',
    'description': 'USCF Member Service Area (MSA) for Python',
    'long_description': "# pyuscf: USCF Member Service Area (MSA) for Python\n\nThe United States Chess Federation (USCF) website for publicly available\nchess member information. The package is nothing more than a client, but there\nare some limitations on searching for chess members' information.\n\nVisit www.uschess.org for further information on the limitations.\n\n## Usage\n\n```python\n>>> from pyuscf import Msa\n>>> player = Msa(12743305)\n>>> player.get_name()\n'FABIANO CARUANA'\n>>> player.get_regular_rating()\n'2895* 2019-08-01'\n>>> player.get_fide_rating()\n'2818 2019-08-01'\n>>>\n```",
    'author': 'Juan Antonio Sauceda',
    'author_email': 'jasgordo@gmail.com',
    'url': 'https://gitlab.com/skibur/pyuscf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
