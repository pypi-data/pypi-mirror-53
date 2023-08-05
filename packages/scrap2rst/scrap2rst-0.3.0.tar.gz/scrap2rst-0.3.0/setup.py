# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['scrap2rst']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['scrap2rst = scrap2rst.cmd:main']}

setup_kwargs = {
    'name': 'scrap2rst',
    'version': '0.3.0',
    'description': 'Converting scrapbox syntax into reStructuredText',
    'long_description': '=========\nscrap2rst\n=========\n\n.. image:: https://img.shields.io/pypi/v/scrap2rst.svg\n   :alt: PyPI\n   :target: http://pypi.org/p/scrap2rst\n\n.. image:: https://img.shields.io/pypi/pyversions/scrap2rst.svg\n   :alt: PyPI - Python Version\n\n.. image:: https://img.shields.io/github/license/shimizukawa/scrap2rst.svg\n   :alt: License\n   :target: https://github.com/shimizukawa/scrap2rst/blob/master/LICENSE\n\n.. image:: https://img.shields.io/github/stars/shimizukawa/scrap2rst.svg?style=social&label=Stars\n   :alt: GitHub stars\n   :target: https://github.com/shimizukawa/scrap2rst\n\n\n``scrap2rst`` is an markup syntax converter from scrapbox into reStructuredText.\n\nFeature\n=======\n\n* Page header\n* Heading level2 if the line is strong text.\n* Figure if the line is link to image.\n* Image if the line contains link to image.\n* Link if the line contains link excluding to image url.\n\nStill many limitation are exist.\n\nCommand\n=======\n\nConvert from scrapbox into reStructuredText::\n\n  $ scrap2rst URL -o output.rst\n\n\nLicense\n=======\nLicensed under the MIT Licence.\n\n\nCHANGES\n=======\n\nSee: https://github.com/shimizukawa/scrap2rst/blob/master/CHANGELOG.rst\n\n',
    'author': 'shimizukawa',
    'author_email': 'shimizukawa@gmail.com',
    'url': 'https://github.com/shimizukawa/scrap2rst',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
