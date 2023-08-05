# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['checkon', 'checkon.scripts.checkon_trial']

package_data = \
{'': ['*'], 'checkon.scripts.checkon_trial': ['checkon_trial/*']}

install_requires = \
['attrs==19.1.0',
 'click==7.0',
 'hyperlink>=19.0,<20.0',
 'inflection>=0.3.1,<0.4.0',
 'junitparser>=1.3,<2.0',
 'marshmallow-dataclass==6.0.0rc5',
 'marshmallow>=3.0,<4.0',
 'pendulum>=2.0,<3.0',
 'pyrsistent>=0.14.11,<0.15.0',
 'requests>=2.22,<3.0',
 'requirements-parser>=0.2.0,<0.3.0',
 'sqlalchemy>=1.3,<2.0',
 'tabulate>=0.8.3,<0.9.0',
 'toml>=0.10.0,<0.11.0',
 'tox-run-command>=0.4.0,<0.5.0',
 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['checkon = checkon.cli:cli']}

setup_kwargs = {
    'name': 'checkon',
    'version': '0.1.4',
    'description': "Support backward compatibility by running your users' test suites.",
    'long_description': "========\nOverview\n========\n\n.. start-badges\n\n.. list-table::\n    :stub-columns: 1\n\n    * - docs\n      - |docs|\n    * - tests\n      - | |travis|\n        |\n    * - package\n      - | |version| |wheel| |supported-versions| |supported-implementations|\n        | |commits-since|\n\n.. |docs| image:: https://readthedocs.org/projects/checkon/badge/?style=flat\n    :target: https://readthedocs.org/projects/checkon\n    :alt: Documentation Status\n\n\n.. |travis| image:: https://img.shields.io/travis/com/metatooling/checkon/master\n    :alt: Travis-CI Build Status\n    :target: https://travis-ci.com/metatooling/checkon\n\n.. |version| image:: https://img.shields.io/pypi/v/checkon.svg\n    :alt: PyPI Package latest release\n    :target: https://pypi.org/pypi/checkon\n\n.. |commits-since| image:: https://img.shields.io/github/commits-since/metatooling/checkon/v0.1.4.svg\n    :alt: Commits since latest release\n    :target: https://github.com/metatooling/checkon/compare/v0.1.4...master\n\n.. |wheel| image:: https://img.shields.io/pypi/wheel/checkon.svg\n    :alt: PyPI Wheel\n    :target: https://pypi.org/pypi/checkon\n\n.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/checkon.svg\n    :alt: Supported versions\n    :target: https://pypi.org/pypi/checkon\n\n.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/checkon.svg\n    :alt: Supported implementations\n    :target: https://pypi.org/pypi/checkon\n\n\n.. end-badges\n\n\nCheckon is a tool to help library maintainers ensure backward-compatibilty by running downstream applications' test suites with library pre-release versions.\n\nSupported meta-runners:\n\n- tox_\n\nSupported test-runners:\n\n- PyTest_\n- Trial_\n\n\nCurrently missing support for:\n\n- unittest_\n- nose_\n\n\nInstallation\n============\n\n::\n\n    pip install checkon\n\nDocumentation\n=============\n\n\nhttps://checkon.readthedocs.io/\n\n\n.. _tox: https://tox.readthedocs.io/en/latest/index.html\n.. _PyTest: https://pytest.org\n.. _Trial: https://twistedmatrix.com/trac/wiki/TwistedTrial\n.. _unittest: https://docs.python.org/3/library/unittest.html\n.. _nose: https://nose.readthedocs.io/en/latest/\n",
    'author': 'Checkon contributors',
    'author_email': 'checkon@cordaz.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
