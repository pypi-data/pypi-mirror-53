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

"""Indexing images in directories."""

import csv
import os

from PIL import Image


def extract_regions(reg_index, region_type):
    """Return the contents of the regions as images.

    Parameters
    ----------
    reg_index : Index
        Index of source images and their regions.
    region_type : str
        Region type to extract.

    Returns
    -------
    regions : iterable(Image)
        Extracted regions as PIL images.

    """
    for rel_path, regions in reg_index.items():
        boxes = [r[:4] for r in regions if r[4] == region_type]
        if not boxes:
            continue
        image_path = os.path.join(reg_index.root_path, rel_path)
        image = Image.open(image_path)
        for box in boxes:
            yield image.crop(box)
