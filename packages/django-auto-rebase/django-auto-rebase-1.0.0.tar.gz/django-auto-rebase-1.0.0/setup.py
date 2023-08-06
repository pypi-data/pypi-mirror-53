# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['django_auto_rebase']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2,<3.0']

entry_points = \
{'console_scripts': ['dar = django_auto_rebase.rebase:main']}

setup_kwargs = {
    'name': 'django-auto-rebase',
    'version': '1.0.0',
    'description': '',
    'long_description': "# Django Auto Rebase\n\n## What is this?\nThis is a command-line tool that allows you to rebase a conflicting Django\nmigration on top of the other Django migration renaming (and renumbering) the\nmigration filename and also editing the `dependencies` attribute on the\n`Migration` class within the file.\n\n## Installation\n```bash\n$ pip install django-auto-rebase\n```\n\n## Usage\n```bash\n$ dar [app-name] [migration-file-to-be-rebased]\n```\n\n## Requirements\n* Python 3.7 (for now. file an issue if you need an earlier version supported)\n* Django 2.2 (earlier versions will likely work, but it's untested for now.\n\n## Limitations\n* Only works on leaf nodes that have migration conflicts.\n* Only works on leaf nodes within the same app.\n\n## FAQ\n### Is this a Django Command?\nNo, although this package is tightly coupled to Django, it is NOT a Django\napp that you need to add to your `INSTALLED_APPS` or call through a `manage.py`.\n\n### How does it find the root Django path?\nThe first thing the script does after parsing your arguments is it walks up\nthe current working directory until it finds the `manage.py` file that all if\nnot most Django applications have.  The folder that holds the first\n`manage.py` directory is appended to `sys.path`.\n\n### Why do you even need this?\nWell, you don't really need it, but _I_ find it helpful.\n\nSuppose the migration tree looks like this:\n```\n0001_xxx <-- 0002_xxx <-- 0003_xxx\n```\n\nThen two developers, working in separate branches, generate their own `0004_xxx`\nmigration.  Once the first developer gets their code merged to master, the\nsecond developer's migration tree is immediately stale/in conflict because\n_its_ `0004_xxx` will still be pointing at  `0003_xxx` as a dependency.  You\nmay find yourself getting this error message:\n\n```\nConflicting migrations detected; multiple leaf nodes in the migration graph:\n(0004_xxx, 0004_yyy in my_app_name).\nTo fix them run 'python manage.py makemigrations --merge'\n```\n\nAs the message suggests, you could run `makemigrations --merge`, which\ngenerates a new leaf node `0005_xxx` and specifies the two `0004_xxx`\nmigrations as a dependencies.  This works in small doses, but I'm not a huge fan.\n(see below)\n\n### What's wrong with makemigrations --merge?\nThe magic numbers of each migration starts meaning less and less.\n\nStrictly speaking, they really do mean nothing - Django doesn't care at all\nabout the number:  A 0004_xxx migration could depend on a migration named\n9999_xxx, which depends on 1234_xxx.\n\nPractically speaking, I do find value in seeing the dependency order of the\nmigration tree follow their actual numbers.  This tool helps rebase two conflicting\nmigrations with ease.\n\n\n## Author\n\n[Christopher Sabater Cordero](https://github.com/cs-cordero)\n",
    'author': 'Christopher Cordero',
    'author_email': 'ccordero@protonmail.com',
    'url': 'https://github.com/cs-cordero/django-auto-rebase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
