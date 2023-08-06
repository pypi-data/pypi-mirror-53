# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['swashbookler']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1,<6.0',
 'beautifulsoup4>=4.8.0,<5.0.0',
 'click>=7.0,<8.0',
 'img2pdf>=0.3.3,<0.4.0',
 'pillow>=6.1,<7.0',
 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['swashbookler = swashbookler.cli:cli']}

setup_kwargs = {
    'name': 'swashbookler',
    'version': '1.0.2',
    'description': 'Allows downloading books from Google Books and converting them to PDFs.',
    'long_description': '# Google Book Downloader\n\n## Downloads books from Google Books!\n\nOnly works for books that provide a full preview.\n\n## Usage\n\nThis project uses [pipenv](https://github.com/pypa/pipenv) for package management.\nOnce pipenv is installed, simply run the downloader using ```pipenv run python main.py [options] ID```.\nOptions are visible using ```pipenv run python main.py -h```.\nThe book ID to download can be found in the URL of the Google Books page.\n',
    'author': 'Coriander Pines',
    'author_email': 'incoming+cvpines-swashbookler-5856924-issue-@incoming.gitlab.com',
    'url': 'https://gitlab.com/cvpines/swashbookler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
