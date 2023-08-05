# -*- coding: utf-8 -*-
#
# Copyright 2017 - 2018  Ternaris.
# SPDX-License-Identifier: Apache-2.0

"""ADE setup script"""

import io
import os
import re
from collections import OrderedDict
from setuptools import find_packages, setup

NAME = 'ade-cli'
DESCRIPTION = 'Agile Development Environment'
ENTRY_POINTS = {
    'console_scripts': ['ade = ade_cli.cli:cli']
}

os.chdir(os.path.abspath(os.path.dirname(__file__)))

with io.open(os.path.join(NAME.replace('-', '_'), '__init__.py'), encoding='utf8') as f:
    VERSION = re.search(r'^__version__ = \'(.*?)\'', f.read(), flags=re.MULTILINE).group(1)

with io.open(os.path.join('README.rst'), 'rt', encoding='utf8') as f:
    README = f.read()


def read_requirements_in(path):
    """Read requirements from requirements.in file."""
    with io.open(path, 'rt', encoding='utf8') as f:  # pylint: disable=redefined-outer-name
        return [
            x.rsplit('=')[1] if x.startswith('-e') else x
            for x in [x.strip() for x in f.readlines()]
            if x
            if not x.startswith('-r')
            if not x[0] == '#'
        ]


INSTALL_REQUIRES = read_requirements_in('requirements.in')
EXTRAS_REQUIRE = {}
EXTRAS_REQUIRE['develop'] = read_requirements_in('requirements-develop.in')


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=README,
      author='Ternaris',
      author_email='team@ternaris.com',
      maintainer='Apex.AI',
      maintainer_email='tooling@apex.ai',
      url='https://gitlab.com/ApexAI/ade-cli',
      project_urls=OrderedDict((
          ('Code', 'https://gitlab.com/ApexAI/ade-cli'),
          ('Issue tracker', 'https://gitlab.com/ApexAI/ade-cli/issues'),
      )),
      license='Apache-2.0',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.5.2',
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,
      tests_require=[
          'pytest',
          'mock',
          'testfixtures',
      ],
      setup_requires=['pytest-runner'],
      entry_points=ENTRY_POINTS)
