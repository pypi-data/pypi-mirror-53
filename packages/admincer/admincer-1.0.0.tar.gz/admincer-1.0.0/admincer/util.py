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

"""Common utilities."""

import argparse

import admincer.find as fnd


def region(reg):
    """Parser for region queries."""
    params = reg.split(':')
    if len(params) not in {2, 3}:
        raise argparse.ArgumentTypeError('expected format: TYPE:WxH[:T]')
    width, height = params[1].split('x')
    params[1:2] = float(width), float(height)
    params[-1] = float(params[-1])
    return fnd.RegionQuery(*params)


def fragment(frg):
    """Parser for fragment queries."""
    params = frg.split(':')
    if len(params) == 2:
        params[1] = float(params[1])
    elif len(params) != 1:
        raise argparse.ArgumentTypeError('expected format: PATH[:T]')
    return fnd.FragmentQuery(*params)
