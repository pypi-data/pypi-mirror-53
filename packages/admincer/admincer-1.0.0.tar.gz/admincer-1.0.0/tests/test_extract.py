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

"""Tests for region extraction."""

import pytest

import admincer.index as idx
import admincer.extract as ex

from conftest import Colors as cc


@pytest.mark.parametrize('region_type, expected_params', [
    ('r0', []),
    ('r1', [(10, 20, cc.WHITE), (10, 10, cc.BLUE), (10, 10, cc.BLUE)]),
    ('r2', [(30, 40, cc.WHITE)]),
])
def test_extract(regdir, region_type, expected_params):
    ri = idx.reg_index(str(regdir))
    extracted_images = list(ex.extract_regions(ri, region_type))
    assert len(extracted_images) == len(expected_params)
    extracted_params = {
        image.size + (image.getpixel((0, 0)),)
        for image in extracted_images
    }
    assert extracted_params == set(expected_params)
