#!/usr/bin/env python
# pylint: disable-msg=W0404,W0622,W0704,W0613,W0152
# copyright 2004-2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of yams.
#
# yams is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# yams is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with yams. If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages

long_description = open('README').read()


setup(name='pyxst',
      version='0.3.2',
      license='LGPL',
      description="XML Schema Tools for Python",
      long_description=long_description,
      long_description_content_type='text/x-rst',
      author='Logilab',
      author_email='devel@logilab.fr',
      url="https://www.logilab.org/project/pyxst",
      install_requires=[
          'lxml',
          'six'
      ],
      packages=find_packages(),
      )
