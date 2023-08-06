# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['jinja2_git']
install_requires = \
['jinja2>=2.10,<3.0']

setup_kwargs = {
    'name': 'jinja2-git',
    'version': '1.0.0',
    'description': 'Jinja2 extension to handle git-specific things',
    'long_description': "# Jinja2 extension to handle git-specific things\n\n[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)\n[![Travis](https://travis-ci.org/sobolevn/jinja2-git.svg?branch=master)](https://travis-ci.org/sobolevn/jinja2-git)\n[![Coveralls](https://coveralls.io/repos/github/sobolevn/jinja2-git/badge.svg?branch=master)](https://coveralls.io/github/sobolevn/jinja2-git?branch=master)\n[![Python versions](https://img.shields.io/pypi/pyversions/jinja2-git.svg)](https://pypi.python.org/pypi/jinja2-git)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\n\n## Installation\n\n```bash\n$ pip install jinja2-git\n```\n\n\n## Reasoning\n\nThis plugin is used to render commit hash in `jinja2` templates. We are\nusing it to render our template version in `cookicutter`:\n\n- [wemake-django-template](https://github.com/wemake-services/wemake-django-template)\n- [wemake-vue-template](https://github.com/wemake-services/wemake-vue-template)\n\n\n## Usage\n\nAdd it as an extension for\n[jinja2](http://jinja.pocoo.org/docs/2.10/extensions/) or\n[cookiecutter](http://cookiecutter.readthedocs.io/en/latest/advanced/template_extensions.html).\n\nAnd then inside a template:\n\n```python\nfrom jinja2 import Environment\n\nenv = Environment(extensions=['jinja2_git.GitExtension'])\ntemplate = env.from_string('Commit is: {% gitcommit %}')\n# => Commit is: c644682f4899d7e98147ce3a61a11bb13c52b3a0\n```\n\nOr short version:\n\n```python\nfrom jinja2 import Environment\n\nenv = Environment(extensions=['jinja2_git.GitExtension'])\ntemplate = env.from_string('Commit is: {% gitcommit short=True %}')\n# => Commit is: c644682\n```\n\n\n## License\n\n[MIT](https://github.com/sobolevn/jinja2-git/blob/master/LICENSE)\n",
    'author': 'Nikita Sobolev',
    'author_email': 'mail@sobolenv.me',
    'url': 'https://github.com/sobolevn/jinja2-git',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
