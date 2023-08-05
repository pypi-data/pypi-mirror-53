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

"""Searching for images based on regions and fragments."""

import functools
import os

import cv2


class Query:
    """Base class for queries."""

    difficulty = 1  # How much compute does this query need?

    def is_match(self, image_path, data):
        """Does this image match the query?"""
        raise NotImplementedError()  # pragma: no cover 

    def __str__(self):
        return self.format_string.format(self)


class RegionQuery(Query):
    """Query for regions of specific type and size."""

    format_string = (
        'RegionQuery({0.region_type}, '
        '{0.min_width} <= width <= {0.max_width}, '
        '{0.min_height} <= height <= {0.max_height})'
    )

    def __init__(self, region_type, width, height, tolerance=25):
        self.region_type = region_type
        multiplier = 1 + tolerance / 100
        self.max_width = width * multiplier
        self.min_width = width / multiplier
        self.max_height = height * multiplier
        self.min_height = height / multiplier

    def is_match(self, image_path, data):
        """Is there a matching (within tolerance) region?"""
        if not isinstance(data, list):
            raise Exception('Region queries require a region index')
        for x1, y1, x2, y2, region_type in data:
            if (
                region_type == self.region_type
                and self.min_width <= x2 - x1 <= self.max_width
                and self.min_height <= y2 - y1 <= self.max_height
            ):
                return True
        return False


class FragmentQuery(Query):
    """Query for a fragment image."""

    difficulty = 10
    format_string = 'FragmentQuery({0.frag_path}, tolerance={0.tolerance})'

    def __init__(self, frag_path, tolerance=10):
        self.frag_path = frag_path
        self.tolerance = tolerance / 100

    @staticmethod
    @functools.lru_cache(maxsize=1)
    def _load_image(image_path):
        """Cache images between queries."""
        with open(image_path, 'r'):
            pass  # Check that we can read the image (OpenCV doesn't).
        return cv2.imread(image_path)

    def is_match(self, image_path, data):
        """Is the best template match below tolerance?"""
        if not hasattr(self, 'frag'):
            self.frag = FragmentQuery._load_image(self.frag_path)
        image = FragmentQuery._load_image(image_path)
        res = cv2.matchTemplate(self.frag, image, cv2.TM_SQDIFF_NORMED)
        best = res.min()
        return best < self.tolerance


def find(index, queries):
    """Find images in the index that match all the queries."""
    queries = sorted(queries, key=lambda q: q.difficulty)
    for name in sorted(index):
        matched_queries = set()
        path = os.path.join(index.root_path, name)
        data = index[name]
        if all(query.is_match(path, data) for query in queries):
            yield name
