# This file is part of AdMincer,
# Copyright (C) 2019 eyeo GmbH
#
# AdMincer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# AdMincer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with AdMincer. If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup

README_PATH = os.path.join(os.path.dirname(__file__), 'README.md')

with open(README_PATH) as f:
    long_description = f.read()

setup(
    name='admincer',
    use_scm_version=True,
    description='Tool for managing datasets for visual ad detection',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='eyeo GmbH',
    author_email='info@adblockplus.org',
    url='https://gitlab.com/eyeo/machine-learning/admincer/',
    packages=['admincer'],
    entry_points={
        'console_scripts': ['admincer=admincer.__main__:main'],
    },
    include_package_data=True,
    install_requires=[
        'Pillow',
        'opencv-python',
        'setuptools_scm',
    ],
    license='GPLv3',
    zip_safe=False,
    keywords='ad-detection machine-learning dataset',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ],
)
