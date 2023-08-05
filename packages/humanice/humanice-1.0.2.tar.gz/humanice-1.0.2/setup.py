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

setup_kwargs = {
    'name': 'humanice',
    'version': '1.0.2',
    'description': 'Nice humanize functions for Python',
    'long_description': "# humanice\n\n[![CircleCI](https://circleci.com/gh/timwedde/humanice.svg?style=svg)](https://circleci.com/gh/timwedde/humanice)\n[![codecov](https://codecov.io/gh/timwedde/humanice/branch/master/graph/badge.svg)](https://codecov.io/gh/timwedde/humanice)\n\nThis modest package contains various common humanization utilities, like turning a number into a fuzzy human readable duration (i.e. `3 minutes ago`) or into a human readable size or throughput. It works with Python 3 and is localized to a bunch of languages.\n\n\n## Installation\n\n`humanice` can be installed via pip:\n```bash\n$ pip install humanice\n```\n\nAlternatively you can build the package by cloning this repository:\n```bash\n$ git clone https://github.com/timwedde/humanice.git\n$ cd humanice/\n$ python3 setupy.py install\n```\n\n## Usage\n\n### Integer humanization\n\n```python\n>>> import humanice\n>>> humanice.intcomma(12345)\n'12,345'\n>>> humanice.intword(123455913)\n'123.5 million'\n>>> humanice.intword(12345591313)\n'12.3 billion'\n>>> humanice.apnumber(4)\n'four'\n>>> humanice.apnumber(41)\n'41'\n```\n\n### Date & time humanization\n\n```python\n>>> import datetime\n>>> humanice.naturalday(datetime.datetime.now())\n'today'\n>>> humanice.naturaldelta(datetime.timedelta(seconds=1001))\n'16 minutes'\n>>> humanice.naturalday(datetime.datetime.now() - datetime.timedelta(days=1))\n'yesterday'\n>>> humanice.naturalday(datetime.date(2007, 6, 5))\n'Jun 05'\n>>> humanice.naturaldate(datetime.date(2007, 6, 5))\n'Jun 05 2007'\n>>> humanice.naturaltime(datetime.datetime.now() - datetime.timedelta(seconds=1))\n'a second ago'\n>>> humanice.naturaltime(datetime.datetime.now() - datetime.timedelta(seconds=3600))\n'an hour ago'\n```\n\n### Filesize humanization\n\n```python\n>>> humanice.naturalsize(1000000)\n'1.0 MB'\n>>> humanice.naturalsize(1000000, binary=True)\n'976.6 KiB'\n>>> humanice.naturalsize(1000000, gnu=True)\n'976.6K'\n```\n\n### Human-readable floating point numbers\n\n```python\n>>> humanice.fractional(1/3)\n'1/3'\n>>> humanice.fractional(1.5)\n'1 1/2'\n>>> humanice.fractional(0.3)\n'3/10'\n>>> humanice.fractional(0.333)\n'1/3'\n>>> humanice.fractional(1)\n'1'\n```\n\n## Localization\n\n### How to change locale in runtime\n\n```python\n>>> humanice.naturaltime(datetime.timedelta(seconds=3))\n3 seconds ago\n>>> _t = humanice.i18n.activate('ru_RU')\n>>> humanice.naturaltime(datetime.timedelta(seconds=3))\n3 секунды назад\n>>> humanice.i18n.deactivate()\n>>> humanice.naturaltime(datetime.timedelta(seconds=3))\n3 seconds ago\n```\n\nYou can pass additional parameter *path* to `activate` to specify a path to search locales in:\n\n```python\n>>> humanice.i18n.activate('pt_BR')\nIOError: [Errno 2] No translation file found for domain: 'humanice'\n>>> humanice.i18n.activate('pt_BR', path='path/to/my/portuguese/translation/')\n<gettext.GNUTranslations instance ...>\n```\n\n### How to add new phrases to existing locale files\n\n```bash\n$ xgettext -o humanice.pot -k'_' -k'N_' -k'P_:1c,2' -l python humanice/*.py  # extract new phrases\n$ msgmerge -U humanice/locale/ru_RU/LC_MESSAGES/humanice.po humanice.pot # add them to locale files\n$ msgfmt --check -o humanice/locale/ru_RU/LC_MESSAGES/humanice{.mo,.po} # compile to binary .mo\n```\n\n### How to add a new locale\n\n```bash\n$ msginit -i humanice.pot -o humanice/locale/<locale name>/LC_MESSAGES/humanice.po --locale <locale name>\n```\n\nWhere `<locale name>` is locale abbreviation, eg `en_GB`, `pt_BR` or just `ru`, `fr` etc.\n\n\n## Supported Languages\n\n* German\n* Finnish\n* French\n* Indonesian\n* Italian\n* Japanese\n* Korean\n* Dutch\n* Portugese\n* Russian\n* Slovak\n* Turkish\n* Vietnamese\n* Simplified Chinese\n",
    'author': 'Tim Wedde',
    'author_email': 'timwedde@icloud.com',
    'url': 'https://github.com/timwedde/humanice',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
