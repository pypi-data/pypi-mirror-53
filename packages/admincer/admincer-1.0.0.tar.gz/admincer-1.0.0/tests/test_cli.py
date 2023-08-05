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

"""Tests for the CLI."""

import glob
import os

from PIL import Image, ImageDraw
import pytest

from conftest import make_image, Colors as cc


def test_noargs(script_runner):
    """Show brief usage info when called with no arguments."""
    ret = script_runner.run('admincer')
    assert not ret.success
    assert 'Batch image editor' in ret.stdout
    assert ret.stderr == ''


@pytest.fixture()
def fragdir2(tmpdir):
    """Two more directories with fragments."""
    ret = tmpdir.mkdir('fragdir2')
    make_image(ret.mkdir('1').join('blue.gif'), 10, 10, cc.BLUE)
    make_image(ret.mkdir('2').join('pink.gif'), 10, 10, cc.PINK)
    return ret


@pytest.fixture()
def regdir2(tmpdir):
    """One image with several regions for test_place()."""
    ret = tmpdir.mkdir('regdir2')
    make_image(ret.join('img.png'), 200, 200, cc.WHITE)
    ret.join('index.csv').write('\n'.join([
        'image,xmin,ymin,xmax,ymax,label',
        'img.png,0,0,10,24,a',
        'img.png,10,0,40,40,a',
        'img.png,40,0,90,60,a',
        'img.png,0,100,10,110,b'
    ]))
    return ret


def test_place(script_runner, tmpdir, regdir2, fragdir, fragdir2):
    """Place fragments onto a source image."""
    targetdir = tmpdir.join('output')
    ret = script_runner.run(
        'admincer', 'place',
        '--fragments', 'a=' + str(fragdir),
        # Test providing multiple directories for the same region type.
        '-f', 'b={}:{}'.format(fragdir2.join('1'), fragdir2.join('2')),
        '-n', '10',
        str(regdir2), str(targetdir),
    )
    assert ret.success
    assert ret.stdout == ''
    assert ret.stderr == ''
    outputs = [
        Image.open(img_path)
        for img_path in glob.glob(os.path.join(str(targetdir), '*.png'))
    ]
    # Identify unique combinations of colors in the four regions.
    signatures = {
        tuple(o.getpixel(p) for p in [(1, 22), (11, 1), (41, 1), (1, 101)])
        for o in outputs
    }
    # Since the first three regions only have one candidate fragment, there are
    # only two possibilities for the complete signature.
    assert signatures == {
        (cc.RED, cc.GREEN, cc.ORANGE, cc.BLUE),
        (cc.RED, cc.GREEN, cc.ORANGE, cc.PINK),
    }
    assert targetdir.join('regions.csv').check(file=1)


@pytest.fixture()
def regdir3(tmpdir):
    """Image with three regions of the same size."""
    ret = tmpdir.mkdir('regdir3')
    make_image(ret.join('img.png'), 12, 12, cc.WHITE)
    ret.join('index.csv').write('\n'.join([
        'image,xmin,ymin,xmax,ymax,label',
        'img.png,0,0,10,10,a',
        'img.png,0,0,8,8,b',
        'img.png,0,0,12,12,c',
    ]))
    return ret


def test_place_resize_modes(script_runner, tmpdir, regdir3, fragdir2):
    """Place fragments with different resize modes."""
    targetdir = tmpdir.join('output')
    ret = script_runner.run(
        'admincer', 'place',
        '-f', 'a=' + str(fragdir2),
        '-f', 'b=' + str(fragdir2),
        '-f', 'c=' + str(fragdir2),
        '--resize-mode', 'scale',
        '--resize-mode', 'b=pad',
        '--resize-mode', 'c=crop',
        str(regdir3), str(targetdir),
    )
    assert ret.success
    assert ret.stdout == ''
    assert ret.stderr == ''


def test_invalid_resize_mode(script_runner, tmpdir, regdir3, fragdir2):
    ret = script_runner.run(
        'admincer', 'place',
        '-f', 'a=' + str(fragdir2),
        '-f', 'b=' + str(fragdir2),
        '-f', 'c=' + str(fragdir2),
        '-r', 'foobar',
        str(regdir3), str(tmpdir),
    )
    assert not ret.success
    assert ret.stdout == ''
    assert 'must be "scale", "pad" or "crop"' in ret.stderr


def test_extract(script_runner, tmpdir, regdir):
    """Extract regions into a separate directory."""
    r0 = tmpdir.join('r0')
    r1 = tmpdir.join('r1')
    r2 = tmpdir.join('r2')
    ret = script_runner.run(
        'admincer', 'extract',
        '--target-dir', 'r1=' + str(r1),
        '-t', 'r2=' + str(r2),
        '-t', 'r0=' + str(r0),
        str(regdir),
    )

    assert ret.success
    assert ret.stdout == ''
    assert ret.stderr == ''

    # Check that output files were created. We don't check the content of the
    # files here because there's test_extract.py.
    assert r0.check(dir=1)
    assert len(list(r0.visit())) == 0
    assert len(list(r1.visit())) == 3
    assert len(list(r2.visit())) == 1


def test_find_region(script_runner, regdir):
    """Find screenshots with marked regions of specific type and size."""
    ret = script_runner.run(
        'admincer', 'find',
        '--region=r1:10x10',
        '-r', 'r3:30x100:100',
        str(regdir),
    )

    assert ret.success
    assert ret.stdout == 'blue3.png\n'


def test_find_fragment(script_runner, fragfind_dir):
    """Find screenshots with specific fragments."""
    needles_dir = fragfind_dir.join('needles')
    ret = script_runner.run(
        'admincer', 'find',
        '--fragment={}'.format(needles_dir.join('2.png')),
        '-f', '{}:5'.format(needles_dir.join('3.png')),
        str(fragfind_dir.join('haystack')),
    )

    assert ret.success
    assert ret.stdout == '1.jpg\n'


def test_find_region_no_index(script_runner, fragfind_dir):
    """Error when --region is given but there's no region index."""
    needles_dir = fragfind_dir.join('needles')
    ret = script_runner.run(
        'admincer', 'find',
        '-r', 'r1:30x100',
        str(needles_dir),
    )

    assert not ret.success
    assert 'region index' in ret.stderr


def test_find_none(script_runner, regdir):
    """Find with no query produces an error."""
    ret = script_runner.run('admincer', 'find', str(regdir))
    assert not ret.success
    assert 'requires at least one' in ret.stderr
