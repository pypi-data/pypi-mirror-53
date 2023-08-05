# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['humanice']

package_data = \
{'': ['*'],
 'humanice': ['locale/de_DE/LC_MESSAGES/*',
              'locale/fi_FI/LC_MESSAGES/*',
              'locale/fr_FR/LC_MESSAGES/*',
              'locale/id_ID/LC_MESSAGES/*',
              'locale/it_IT/LC_MESSAGES/*',
              'locale/ja_JP/LC_MESSAGES/*',
              'locale/ko_KR/LC_MESSAGES/*',
              'locale/nl_NL/LC_MESSAGES/*',
              'locale/pt_BR/LC_MESSAGES/*',
              'locale/ru_RU/LC_MESSAGES/*',
              'locale/sk_SK/LC_MESSAGES/*',
              'locale/tr_TR/LC_MESSAGES/*',
              'locale/vi_VI/LC_MESSAGES/*',
              'locale/zh_CN/LC_MESSAGES/*']}

install_requires = \
['codecov>=2.0,<3.0', 'flake8>=3.7,<4.0', 'pytest>=5.1,<6.0']

setup_kwargs = {
    'name': 'humanice',
    'version': '1.0.0',
    'description': 'Nice humanize functions for Python',
    'long_description': None,
    'author': 'Tim Wedde',
    'author_email': 'timwedde@icloud.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
