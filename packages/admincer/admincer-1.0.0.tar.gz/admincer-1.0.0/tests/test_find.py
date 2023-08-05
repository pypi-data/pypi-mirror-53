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

"""Tests for image search."""

from PIL import Image
import pytest

import admincer.find as fnd
import admincer.index as idx


@pytest.fixture(scope='session')
def index():
    return idx.RegionIndex('', {
        'foo': [
            (10, 10, 20, 30, '1'),
            (0, 0, 50, 60, '2'),
            (5, 5, 10, 10, '3'),
        ],
        'bar': [
            (10, 10, 20, 30, '1'),
            (0, 0, 50, 70, '2'),
        ],
        'baz': [
            (0, 0, 50, 60, '2'),
            (5, 5, 10, 10, '3'),
        ],
    })


@pytest.mark.parametrize('params,result', [
    (('foo', 100, 200),
     'RegionQuery(foo, 80.0 <= width <= 125.0, 160.0 <= height <= 250.0)'),
    (('bar', 100, 200, 100),
     'RegionQuery(bar, 50.0 <= width <= 200.0, 100.0 <= height <= 400.0)'),
])
def test_region_query(params, result):
    """Test the RegionQuery constructor."""
    rq = fnd.RegionQuery(*params)
    assert str(rq) == result


@pytest.mark.parametrize('queries,expected', [
    ([fnd.RegionQuery('1', 10, 20)], ['bar', 'foo']),
    ([fnd.RegionQuery('1', 10, 20),
      fnd.RegionQuery('2', 50, 50)], ['foo']),
    ([fnd.RegionQuery('1', 10, 20),
      fnd.RegionQuery('2', 50, 50)], ['foo']),
])
def test_find_region(index, queries, expected):
    found = list(fnd.find(index, queries))
    assert found == expected


@pytest.mark.parametrize('needles,expected', [
    (['0.png'], ['0.jpg', '2.jpg']),
    (['1.png'], ['0.jpg', '3.jpg']),
    (['2.png'], ['0.jpg', '1.jpg', '2.jpg']),
    (['2.png', '3.png'], ['1.jpg']),
])
def test_find_fragment(fragfind_dir, needles, expected):
    """Test finding images by fragments."""
    index = idx.some_index(str(fragfind_dir.join('haystack')))
    queries = [
        fnd.FragmentQuery(str(fragfind_dir.join('needles').join(needle)))
        for needle in needles
    ]
    found = list(fnd.find(index, queries))
    assert found == expected


def test_find_fragment_and_region(fragfind_dir):
    """Test finding images by fragments and regions."""
    index = idx.some_index(str(fragfind_dir.join('haystack')))
    queries = [
        fnd.RegionQuery('r1', 10, 10),
        fnd.FragmentQuery(str(fragfind_dir.join('needles').join('2.png')))
    ]
    found = list(fnd.find(index, queries))
    assert found == ['0.jpg']
