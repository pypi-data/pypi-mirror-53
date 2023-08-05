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

import argparse
import os
import sys

import admincer.index as idx
import admincer.extract as ex
import admincer.find as fnd
import admincer.place as pl
import admincer.util as util

__all__ = ['main']

parser = argparse.ArgumentParser(description='Batch image editor')
subparsers = parser.add_subparsers(help='sub-command help')


def command(*args, **kw):
    """Return a decorator for command functions.

    This decorator will create a subparser for the command function passing
    all the arguments of `command()` to `.add_parser()`. If no name and help
    are provided for the command, they will be taken from the function name
    and docstring (only the first line of the docstring is used) of the
    decorated function.

    """

    def decorator(func):
        nonlocal args, kw

        if not args:
            args = [func.__name__]
        if 'help' not in kw:
            kw['help'] = func.__doc__.split('\n')[0]

        cmd = subparsers.add_parser(*args, **kw)
        for arg in reversed(getattr(func, '__args__', [])):
            cmd.add_argument(*arg['args'], **arg['kw'])
        cmd.set_defaults(func=func)

        return func

    return decorator


def arg(*args, **kw):
    """Return a decorator that will add an argument to a command function.

    All parameters passed to the decorator will be passed to `.add_argument()`
    call of the subparser corresponding to the decorated function.

    """

    def decorator(func):
        nonlocal args, kw

        if not hasattr(func, '__args__'):
            func.__args__ = []
        func.__args__.append({'args': args, 'kw': kw})

        return func

    return decorator


def parse_xy_options(argitems, multivalue=False):
    """Collect options of the form x=y or x=y1:y2 into a list of tuples."""
    ret = []

    for s in argitems:
        if '=' in s:
            x, y = s.split('=')
        else:
            x, y = None, s

        if multivalue:
            y = y.split(':')

        ret.append((x, y))

    return ret


def take(n, iterable):
    """Return an iterable with n first items of the original iterable."""
    for i, item in enumerate(iterable):
        yield item
        if i >= n - 1:
            return


@command(aliases=['pl'])
@arg('source', help='Directory for source images and region maps')
@arg('target', help='Directory for output images')
@arg('--fragments', '-f', action='append', default=[],
    metavar='REGION-TYPE=DIR[:DIR...]',
    help='Add fragment directory/ies for specific region types')
@arg('--resize-mode', '-r', action='append', default=[],
    metavar='REGION-TYPE=MODE',
    help='Resize mode for region types: "scale" (default), "pad" or "crop"')
@arg('--count', '-n', default=1, type=int, help='Number of images to generate')
def place(args):
    """Place fragments into designated regions of source images."""
    reg_index = idx.reg_index(args.source)
    frag_dirs = parse_xy_options(args.fragments, multivalue=True)
    frag_indices = [(rt, map(idx.frag_index, dirs)) for rt, dirs in frag_dirs]
    resize_modes = dict(parse_xy_options(args.resize_mode))
    recipe_gen = pl.gen_recipes(reg_index, frag_indices, resize_modes)
    recipes = take(args.count, recipe_gen)
    pl.render_recipes(reg_index, recipes, args.target)


@command(aliases=['ex'])
@arg('source', help='Directory for source images')
@arg('--target-dir', '-t', action='append', default=[],
     metavar='REGION-TYPE=DIR',
     help='Target directory for extracting regions of specific type')
def extract(args):
    """Extract the contents of fragments to directories by type."""
    reg_index = idx.reg_index(args.source)
    target_dirs = dict(parse_xy_options(args.target_dir))

    for region_type, target_dir in target_dirs.items():
        os.makedirs(target_dir, exist_ok=True)
        regions = ex.extract_regions(reg_index, region_type)
        for i, region in enumerate(regions):
            out_path = os.path.join(target_dir, '{:05d}.png'.format(i))
            region.save(out_path)


@command(aliases=['f'])
@arg('dir', help='Directory in which to search')
@arg('--fragment', '-f', action='append', default=[],
     metavar='PATH[:T]', type=util.fragment,
     help='Look for fragments similar to specific image')
@arg('--region', '-r', action='append', default=[],
     metavar='TYPE:WxH[:T]', type=util.region,
     help='Look for regions of specific types and sizes')
def find(args):
    """Find images with regions of specific types and sizes."""
    dir_index = idx.some_index(args.dir)
    queries = args.region + args.fragment
    if not queries:
        sys.exit('find requires at least one of: -r/--region, -f/--fragment')
    for found in fnd.find(dir_index, queries):
        print(found)


def main():
    """Run the CLI."""
    args = parser.parse_args()
    if callable(getattr(args, 'func', None)):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)
