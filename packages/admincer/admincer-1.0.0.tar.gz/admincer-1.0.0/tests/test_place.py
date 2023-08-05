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

"""Tests for placing fragments into regions."""

import os

from PIL import Image, ImageDraw
import pytest

import admincer.index as idx
import admincer.place as pl

from conftest import Colors as cc

# Fragment indices.
A = idx.FragmentIndex('a', {
    '1': (10, 10),
    '2': (20, 20),
})
B = idx.FragmentIndex('b', A)
C = idx.FragmentIndex('c', {
    '1/1': (10, 10),
    '1/2': (10, 10),
    '2/1': (20, 20),
    '2/2': (20, 20),
})
D = idx.FragmentIndex('d', C)
E = idx.FragmentIndex('e', {
    '1': (9, 9),
    '2': (11, 11),
    '3': (18, 22),
    '4': (22, 18),
})

# Images with regions.
X = idx.RegionIndex('x', {
    '1': [
        (10, 10, 20, 20, 'a'),
        (20, 20, 30, 30, 'b'),
        (30, 30, 50, 50, 'a'),
        (50, 50, 70, 70, 'b'),
    ],
})
Y = idx.RegionIndex('y', {
    '1': [(10, 10, 20, 20, 'a')],
    '2': [(10, 10, 20, 20, 'b')],
    '3': [(10, 10, 30, 30, 'a')],
    '4': [(10, 10, 30, 30, 'b')],
})


def test_fragment_picker():
    fp = pl.FragmentPicker({'a': [A], 'b': [B]})
    assert fp.pick(10, 10, 'a') == 'a/1'
    assert fp.pick(10, 10, 'b') == 'b/1'
    assert fp.pick(20, 20, 'a') == 'a/2'
    assert fp.pick(20, 20, 'b') == 'b/2'


def test_fragment_picker_randomness():
    fp = pl.FragmentPicker({None: [A, B]})
    picks = [fp.pick(10, 10, 'a') for _ in range(100)]
    # Check that each eligible was picked between 20 and 80 times out of 100.
    for i in 'ab':
        assert 20 < len([p for p in picks if p == i + '/1']) < 80


def test_gen_recipes():
    rg = pl.gen_recipes(X, [('a', [A]), ('b', [B])], {'b': 'pad'})
    recipe = next(rg)
    assert recipe.image_path == 'x/1'
    assert recipe.placements == [
        ('a/1', (10, 10, 20, 20), 'scale'),
        ('a/2', (30, 30, 50, 50), 'scale'),
        ('b/1', (20, 20, 30, 30), 'pad'),
        ('b/2', (50, 50, 70, 70), 'pad'),
    ]
    # Reverse order of fragment indices.
    rg = pl.gen_recipes(X, [('b', [B]), ('a', [A])])
    recipe = next(rg)
    assert [p[0] for p in recipe.placements] == ['b/1', 'b/2', 'a/1', 'a/2']


def test_gen_recipes_randomness():
    rg = pl.gen_recipes(Y, [('a', [C]), ('b', [D])])
    recipes = [next(rg) for _ in range(100)]
    variety = {
        '{}-{}'.format(recipe.image_path, recipe.placements[0][0])
        for recipe in recipes
    }
    assert variety == {
        'y/1-c/1/1', 'y/1-c/1/2',
        'y/2-d/1/1', 'y/2-d/1/2',
        'y/3-c/2/1', 'y/3-c/2/2',
        'y/4-d/2/1', 'y/4-d/2/2',
    }


def test_close_enough():
    """Try placing fragments into imprecisely matching regions."""
    rg = pl.gen_recipes(X, [('a', [E]), ('b', [E])])
    recipe = next(rg)
    assert len(recipe.placements) == 4


@pytest.fixture()
def wb_100x100():
    """White 100x100 with blue lines on left and top."""
    image = Image.new('RGB', (100, 100), cc.WHITE)
    draw = ImageDraw.Draw(image)
    draw.rectangle([(0, 0), (2, 100)], cc.BLUE)
    draw.rectangle([(0, 0), (100, 2)], cc.BLUE)
    return image


@pytest.mark.parametrize(
    'region,resize_mode,in_corner,out_corner,plc_width,plc_height', [
    ((0, 0, 10, 10), 'scale', (5, 5), (10, 10), 10, 10),
    ((0, 0, 14, 14), 'scale', (7, 7), (14, 14), 14, 14),
    ((0, 0, 8, 8), 'scale', (4, 4), (8, 8), 8, 8),
    ((0, 0, 10, 10), 'crop', (5, 5), (10, 10), 10, 10),  # Same as scale.
    ((0, 0, 14, 14), 'crop', (5, 5), (10, 10), 10, 10),
    ((0, 0, 8, 8), 'crop', (5, 5), (8, 8), 8, 8),
    ((0, 0, 10, 10), 'pad', (5, 5), (10, 10), 10, 10),  # Same as scale.
    ((0, 0, 14, 14), 'pad', (5, 5), (10, 10), 14, 14),
    ((0, 0, 8, 8), 'pad', (5, 5), (8, 8), 8, 8),
])
def test_fragment_placement(
    wb_100x100,
    region, resize_mode, in_corner, out_corner, plc_width, plc_height,
):
    """Test placement of fragments."""
    image = wb_100x100
    fragment = Image.new('RGB', (10, 10), cc.GREEN)
    draw = ImageDraw.Draw(fragment)
    draw.rectangle([(0, 0), (5, 5)], cc.RED)

    pl.place_fragment(image, fragment, region, resize_mode)
    rg_x, rg_y = in_corner
    gw_x, gw_y = out_corner
    # Check that specific points of placed fragment are where they should be.
    assert image.getpixel((rg_x - 2, rg_y - 2)) == cc.RED
    assert image.getpixel((rg_x + 2, rg_y - 2)) == cc.GREEN
    assert image.getpixel((rg_x - 2, rg_y + 2)) == cc.GREEN
    assert image.getpixel((gw_x - 2, gw_y - 2)) == cc.GREEN
    assert image.getpixel((gw_x + 2, gw_y - 2)) == cc.WHITE
    assert image.getpixel((gw_x - 2, gw_y + 2)) == cc.WHITE
    # Check that overall modified area has the right size.
    assert image.getpixel((plc_width - 1, 1)) != cc.BLUE
    assert image.getpixel((plc_width + 1, 1)) == cc.BLUE
    assert image.getpixel((1, plc_height - 1)) != cc.BLUE
    assert image.getpixel((1, plc_height + 1)) == cc.BLUE


@pytest.mark.parametrize('resize_mode,expect_colors', [
    ('scale', [cc.RED, cc.RED, cc.PINK,
               cc.RED, cc.RED, cc.BLUE, cc.WHITE]),
    ('crop',  [cc.RED, cc.PINK, cc.WHITE,
               cc.BLUE, cc.WHITE, cc.BLUE, cc.WHITE]),
    ('pad',   [cc.RED, cc.PINK, cc.WHITE,
               cc.WHITE, cc.WHITE, cc.WHITE, cc.WHITE]),
])
def test_transparent_placement(wb_100x100, resize_mode, expect_colors):
    """Place a partially transparent fragment in different resize modes."""
    image = wb_100x100
    fragment = Image.new('RGBA', (10, 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fragment)
    draw.rectangle([(0, 0), (5, 5)], (255, 0, 0, 255))
    draw.rectangle([(5, 0), (10, 5)], (255, 0, 0, 127))

    pl.place_fragment(image, fragment, (0, 0, 20, 20), resize_mode)
    points = [(4, 4), (8, 4), (15, 5), (1, 8), (4, 8), (1, 15), (4, 15)]
    for p, ec in zip(points, expect_colors):
        assert image.getpixel(p) == ec


@pytest.fixture()
def recipe(regdir, fragdir):
    """One simple rendering recipe."""
    return pl.Recipe(
        os.path.join(str(regdir), 'white2.png'),
        [
            (os.path.join(str(fragdir), 'red.gif'),
                (0, 0, 10, 20), 'scale'),
            (os.path.join(str(fragdir), 'green.png'),
                (20, 20, 50, 60), 'scale'),
            (os.path.join(str(fragdir), 'subdir', 'orange.jpg'),
                (5, 5, 10, 10), 'crop'),
        ],
    )


def test_render_recipe(tmpdir, recipe):
    target_path = str(tmpdir.join('out.png'))
    recipe.render(target_path)
    output = Image.open(target_path)
    assert output.getpixel((1, 1)) == cc.RED
    assert output.getpixel((21, 21)) == cc.GREEN
    assert output.getpixel((7, 7)) == cc.ORANGE


def test_render_recipes(tmpdir, regdir, recipe):
    src_index = idx.reg_index(str(regdir))
    target_dir = tmpdir.mkdir('td')
    recipes = [recipe, recipe]
    pl.render_recipes(src_index, recipes, str(target_dir))

    # Check that the files were rendered and the index created.
    assert target_dir.join('00000.png').check(file=1)
    assert target_dir.join('00001.png').check(file=1)
    assert target_dir.join('regions.csv').check(file=1)

    # Check index correctness.
    tgt_index = idx.reg_index(str(target_dir))
    assert list(tgt_index.keys()) == ['00000.png', '00001.png']
    assert tgt_index['00000.png'] == src_index['white2.png']
    assert tgt_index['00001.png'] == src_index['white2.png']
