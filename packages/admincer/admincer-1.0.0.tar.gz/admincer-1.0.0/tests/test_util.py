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

"""Tests for common utilities."""

import pytest

import admincer.find as fnd
import admincer.util as util


@pytest.mark.parametrize('source,parsed', [
    ('foo:10x10', fnd.RegionQuery('foo', 10, 10)),
    ('bar:100x100:50', fnd.RegionQuery('bar', 100, 100, 50)),
    ('broken', None),
    ('broken:100', None),
    ('broken:cxz', None),
    ('broken:10x10:10:5', None),
])
def test_region_parser(source, parsed):
    if parsed is None:
        with pytest.raises(Exception):
            util.region(source)
    else:
        got = util.region(source)
        assert got.__dict__ == parsed.__dict__


@pytest.mark.parametrize('source,parsed', [
    ('foo/bar.png', fnd.FragmentQuery('foo/bar.png')),
    ('/a/b/c.jpg:42', fnd.FragmentQuery('/a/b/c.jpg', 42)),
    ('broken:1:2', None),
    ('broken:foo', None),
])
def test_fragment_parser(source, parsed):
    if parsed is None:
        with pytest.raises(Exception):
            util.fragment(source)
    else:
        got = util.fragment(source)
        assert got.__dict__ == parsed.__dict__
