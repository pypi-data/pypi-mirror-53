# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flair', 'flair.models']

package_data = \
{'': ['*'], 'flair': ['embeddings/en/*']}

install_requires = \
['bpemb==0.2.9', "torch==1.2.0+cpu"]

setup_kwargs = {
    'name': 'flair_light',
    'version': '0.4.2',
    'description': 'A lightweight version of Flair for sequence tagging.',
    'long_description': None,
    'author': 'snapADDY GmbH',
    'author_email': 'info@snapaddy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'dependency_links': ["https://download.pytorch.org/whl/cpu/torch-1.2.0%2Bcpu-cp36-cp36m-manylinux1_x86_64.whl#torch=1.2.0+cpu"],
    'python_requires': '>=3.6,<4.0',
    'data_files': [('embeddings/en', ['flair/embeddings/en/en.wiki.bpe.vs100000.model'])]
}


setup(**setup_kwargs)
