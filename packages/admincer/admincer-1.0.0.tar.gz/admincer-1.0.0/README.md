# AdMincer

AdMincer is a command line tool for enriching datasets of screenshots used in
ML-based ad detection. It can probably be used with other object-detection
datasets, but ad detection is the main use case we're after.

## Usage

From the command line, run `$ admincer <command>` to get information on command
options and usage. At the moment only one command is available: `place`.

### Place

This command places fragment images into the regions of source images. It takes
a directory with source images that have regions marked on them and multiple
mappings of region type to fragment directory:

    $ admincer place -f ad=ads/dir -f label=labels:other/labels -n 5 source target

This will take images with marked regions from `source/`, place images from
`ads/dir/` into the regions of type `ad` and images from `labels/` and
`other/labels/` into the `label` regions. It will generate 5 images and store
them in `target/`.

The placements are performed in the order of region types on the command line.
In the example above first all `ad` regions will be placed and then all `label`
regions.

#### Region marking

Regions of the images can be defined via a CSV file in the following format
(the numbers are X and Y coordinates of the top left corner followed by the
bottom right corner):

    image,xmin,ymin,xmax,ymax,label
    image1.png,50,50,80,90,region_type1
    image2.gif,10,10,20,20,region_type2

They can also be defined via TXT files of the same name as the image. The TXT
files should be in the format commonly used with YOLO object detector (the
numbers are region type number followed by coordinates of the center of the
region and then its width and height, coordinates and sizes are rescaled so
the full image is 1x1):

    0 0.075 0.15 0.05 0.1
    1 0.225 0.15 0.05 0.1

It's possible to provide names for the region type numbers via placing a file
with `.names` extension into the directory. It should simply contian the names
in the successive lines:

    region_type1
    region_type2

When the names file is provided it's also possible to mix CSV and TXT region
definitions but not for the same image.

Note: regions that extend beyond the boundaries of the image will be clipped.

#### Resize modes

When the fragments placed into the regions are not of the same size as the
regions, there are several possible options for resizing them. The default
is to scale the fragment to match the size of the region. Another option is to
cut off the part of the fragment that doesn't fit and place the rest into the
part of the region that it would cover. Yet another approach is to cut off some
parts and pad the remaining image to the size of the region. These modes are
called `scale`, `crop` and `pad` respectively and they can be configured via
`--resize-mode` command line option. Example: 

    $ admincer place -f ad=ads/dir -f label=labels -r pad -r label=crop ...

Here the first `-r` sets the default resize mode and the second one overrides
it for `label` region type.

### Extract

This command extracts the contents of marked regions from source images. It
takes a directory with source images with marked regions (see above) and
multiple mappings of region type to target directory:

    $ admincer extract --target-dir ad=ads/dir -t label=labels source

This will load the images and region maps from `source` and will extract the
contents of the regions labeled `ad` and `label` into `ads/dir` and `labels`
directories respectively.

### Find

This command finds source images that have regions of specific types and sizes.
For example the following command will find all images in `source` directory
that have regions of the type `ad` 100 pixels wide by 50 pixels high.

    $ admincer find --region=ad:100x50 source

There's certain tolerance for size mismatches. Normally it's +25% and -20%.
Tolerance can be configured via an additional parameter of the region query:

    $ admincer find -r ad:100x50:100 source

Here height and width can be up to 100% larger and up to 50% smaller. In
general the tolerance value X allows the region to be X% larger than specified
or the specification to be X% larger than the region.

Multiple `--region`/`-r` options can be given. In this case images that contain
at least one region matching each query will be found (i.e. multiple queries
are combined using `and` operator).

## Questions

- Fragment matching policy (current one allows scaling by 80% to 125%).
- What to do if there are no valid candidate fragments for placement? Right now
  we bomb out with an exception.
- Do we want sampling with/without replacement? Or maybe some kind of
  deterministic selection? Right now it's with replacement.
