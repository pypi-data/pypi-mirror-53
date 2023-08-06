#!/usr/bin/env python
#

#   -*- coding: utf-8 -*-
#
#   This file is part of PyBuilder
#
#   Copyright 2011-2015 PyBuilder Team
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

#
# This script allows to support installation via:
#   pip install git+git://<project>@<branch>
#
# This script is designed to be used in combination with `pip install` ONLY
#
# DO NOT RUN MANUALLY
#

import sys

from setuptools import setup

with open("README.md", "r") as readme:
    description = readme.read()

with open("LICENSE", "r") as readme:
    license_x = readme.read()

license_x_y = " : ".join(x for x in license_x.split("\n")[:3] if x)

description = "{} \n\n {}".format(description, license_x_y)

setup(
    name='Golla',
    version='0.0.0',
    include_package_data=True,
    url='https://github.com/AbhimanyuHK/Golla',
    license=license_x_y,
    author='Abimanyu HK',
    author_email='manyu1994@hotmail.com',
    description='A SQL ORM Tool',
    long_description=description,
    long_description_content_type="text/markdown"
)
