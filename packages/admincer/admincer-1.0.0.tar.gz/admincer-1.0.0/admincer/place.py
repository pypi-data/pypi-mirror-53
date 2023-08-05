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

"""Place fragments into regions of an image."""

import collections
import csv
import random
import os

from PIL import Image


# How much we can scale fragments to make them fit.
MIN_SCALE = 0.8
MAX_SCALE = 1.25


def get_pad_color(image, region):
    """Determine the color to use for padding fragments placed in this region.

    The return color is the most common color in the bottom and right
    boundaries of the region.

    Parameters
    ----------
    image : Image
        Source image.
    region : (int, int, int, int)
        Region coordinates (x1, y1, x2, y2).

    Returns
    -------
    color : (int, int, int)
        Background color as an RGB triple.

    """
    points = (
        [(x, region[3] - 1) for x in range(region[0], region[2])] +
        [(region[2] - 1, y) for y in range(region[1], region[3])]
    )
    values = [image.getpixel(p) for p in points]
    counts = collections.defaultdict(int)
    for v in values:
        counts[v] += 1
    return max((c, v) for v, c in counts.items())[1]


def _place(image, fragment, region):
    """Place fragment into the region of the image that has the same size."""
    if fragment.mode == 'RGBA':
        image.paste(fragment, region, fragment)
    else:
        image.paste(fragment, region)


def place_fragment(image, fragment, region, resize_mode='scale'):
    """Place fragment into the image.

    Parameters
    ----------
    image : Image
        Image onto which the fragment will be placed.
    fragment : Image
        The fragment to place.
    region : (int, int, int, int)
        Region coordinates (x1, y1, x2, y2).
    resize_mode : str
        A flag that controls the way the image size is adjusted to the size of
        the region. One of 'scale', 'pad' or 'crop'.

    """
    x1, y1, x2, y2 = region
    size = x2 - x1, y2 - y1

    if fragment.size != size:
        if resize_mode == 'scale':
            fragment = fragment.resize(size, Image.HAMMING)
        elif resize_mode == 'pad':
            pad_color = get_pad_color(image, region)
            padded_fragment = Image.new('RGB', size, pad_color)
            size = tuple(min(size[i], fragment.size[i]) for i in range(2))
            fragment = fragment.crop((0, 0) + size)
            _place(padded_fragment, fragment, (0, 0) + size)
            fragment = padded_fragment
        elif resize_mode == 'crop':
            size = tuple(min(size[i], fragment.size[i]) for i in range(2))
            region = (x1, y1, x1 + size[0], y1 + size[1])
            fragment = fragment.crop((0, 0) + size)
        else:
            raise ValueError('Resize mode must be "scale", "pad" or "crop"')

    _place(image, fragment, region)


class Recipe:
    """Fragments placement recipe."""

    def __init__(self, image_path, placements):
        """Constructor.

        Parameters
        ----------
        image_path : str
            Path to the main image.
        placements : [(fragment_path, x1, y1, x2, y2)]
            List of fragment placements.

        """
        self.image_path = image_path
        self.placements = placements

    def render(self, target_path):
        """Render the result of this recipe.

        Parameters
        ----------
        target_path : str
            Path where the result of the rendering will be written.

        """
        image = Image.open(self.image_path)
        for fragment_path, region, resize_mode in self.placements:
            fragment = Image.open(fragment_path)
            place_fragment(image, fragment, region, resize_mode)
        image.save(target_path)


class FragmentPicker:
    """Picks fragments from one or more fragment indices"""

    def __init__(self, fragindex_map):
        self.fragindex_map = fragindex_map

    def pick(self, width, height, region_type):
        """Pick a fragment that matches the region type and size.

        Parameters
        ----------
        width : int
            Width of the region.
        height : int
            Height of the region.
        region_type : str
            Type of the region.

        Returns
        -------
        fragment_path : str
            Full path to the fragment image.

        Raises
        ------
        IndexError
            When there are no valid candidate fragents.

        """
        # Possible optimization: cache candidates by width, height,
        # region_type.
        # TODO: Maybe don't fail if there are no valid candidates but skip that
        # region instead.
        indices = set()
        indices.update(
            self.fragindex_map.get(region_type, []),
            self.fragindex_map.get(None, []),
        )
        candidates = [
            os.path.join(index.root_path, image)
            for index in indices
            for image, (w, h) in index.items()
            if (w * MIN_SCALE <= width <= w * MAX_SCALE and
                h * MIN_SCALE <= height <= h * MAX_SCALE)
        ]
        return random.choice(candidates)


def gen_recipes(regindex, fragindices, resize_modes=None):
    """Generate fragment placement recipes.

    Parameters
    ----------
    regindex : Index
        Index of source images and regions in them.
    fragindices : [(str, [Index])]
        Sequence of pairs: region label, list of fragment indices.

    Returns
    -------
    recipes : generator of Recipe
        Fragments placement recipes.

    Note: the placements follow the order of region labels in `fragindices`.

    """
    if resize_modes is None:
        resize_modes = {}
    if None not in resize_modes:
        resize_modes[None] = 'scale'

    fragindex_map = collections.OrderedDict()
    for label, indices in fragindices:
        fragindex_map.setdefault(label, []).extend(indices)
    fp = FragmentPicker(fragindex_map)

    images = list(regindex)
    while True:
        image = random.choice(images)
        regions = regindex[image]
        image_path = os.path.join(regindex.root_path, image)        
        placements = [
            (
                fp.pick(x2 - x1, y2 - y1, region_type),
                (x1, y1, x2, y2),
                resize_modes.get(region_type, resize_modes[None]),
            )
            for rt in fragindex_map
            for (x1, y1, x2, y2, region_type) in regions
            if region_type == rt
        ]
        yield Recipe(image_path, placements)


def _write_regions_csv(csv_path, regions_dict):
    """Write regions from a dictionary into a CSV file."""
    with open(csv_path, 'wt', encoding='utf-8') as f:
        csv_w = csv.writer(f)
        csv_w.writerow(('image', 'xmin', 'ymin', 'xmax', 'ymax', 'label'))

        for image_name, regions in regions_dict.items():
            for region in regions:
                csv_w.writerow((image_name,) + region)


def render_recipes(regindex, recipes, target_dir):
    """Render multiple recipes to target_dir.

    Parameters
    ----------
    regindex : Index
        Index of source images and regions in them.
    recipes : iterable of Recipe
        The recipes to render.

    """
    regions = {}
    os.makedirs(target_dir, exist_ok=True)

    for i, recipe in enumerate(recipes):
        out_name = '{:05d}.png'.format(i)
        out_path = os.path.join(target_dir, out_name)
        recipe.render(out_path)
        regions[out_name] = regindex[os.path.basename(recipe.image_path)]

    _write_regions_csv(os.path.join(target_dir, 'regions.csv'), regions)
