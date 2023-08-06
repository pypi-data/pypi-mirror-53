"""
:Project: Cruncher
:Contents: __init__.py
:copyright: © 2019 Daniel Morell
:license: GPL-3.0, see LICENSE for more details.
:Author: DanielCMorell
"""
# Standard Library Imports
import os

# Package Imports
import click

# Local Imports
from .core import CrunchHandler, OUTPUT_FILE_FORMATS


@click.command()
@click.option(
    '-i', '--image', 'image',
    type=click.Path(exists=True, readable=True, file_okay=True),
    help='The absolute path to the image to be crunched.'
)
@click.option(
    '-d', '--directory', 'directory',
    type=click.Path(exists=True, readable=True, dir_okay=True),
    default=os.getcwd(),
    show_default='current directory',
    help='The absolute path to the directory of images to be crunched.'
)
@click.option(
    '-o', '--output', 'output',
    type=click.Path(),
    default=None,
    show_default='current directory /crunched',
    help='The the directory to place the crunched images in.'
)
@click.option(
    '-f', '--format', 'file_format',
    type=click.Choice(OUTPUT_FILE_FORMATS, case_sensitive=False),
    default='JPEG',
    show_default=True,
    help='The output image format of the final crunched image.'
)
@click.option(
    '-q', '--quality', 'quality',
    type=click.IntRange(1, 100, clamp=True),
    default=80,
    show_default=True,
    help='The quality of the image after it is crunched. [range: 1 - 100]'
)
@click.option(
    '-s', '--size', 'size',
    type=(int, int),
    default=(None, None),
    help='The pixel width / height of the image after it is crunched. [Format: -S <WIDTH HEIGHT>]'
)
@click.option(
    '-a', '--append', 'append',
    type=str,
    default=None,
    help='Append a string to the filename.'
)
@click.option(
    '--ignore-orientation', 'orientation',
    is_flag=True,
    help='Include this flag to ignore the original image orientation. I.e. if '
         '--size is landscape all portrait images will be cropped as landscape.'
)
@click.option(
    '-m', '--keep-metadata', 'metadata',
    is_flag=True,
    help='Include this flag to keep the image meta/exif. It is removed by default.'
)
@click.option(
    '-v', '--versions', 'nversions',
    default=1,
    show_default=True,
    help='The number of versions to create for each image. If this is set to more '
         'than one you will be prompted to enter --format, --quality, --size, '
         '--append, --ignore-orientation, and --keep-metadata.'
)
@click.option(
    '-r', '--recursive', 'recursive',
    is_flag=True,
    help='Get images from sub directories also. Only applicable if --directory '
         'is used.'
)
@click.option(
    '-c', '--config', 'config',
    type=click.Path(),
    default=None,
    help='Specify a JSON file with your settings, this will override all other settings.'
)
def cli(image, directory, output, file_format, quality, size, append,
        metadata, orientation, nversions, recursive, config):
    """
    Cruncher

    This is a simple CLI image optimization wrapper for the Python Image
    Library fork Pillow. Cruncher takes images and scales them to
    the specified size and quality.
    """

    cruncher = CrunchHandler(image=image, directory=directory, output=output, file_format=file_format,
                                   quality=quality, size=size, append=append, metadata=metadata,
                                   orientation=orientation, nversions=nversions, recursive=recursive,
                                   config=config)
    cruncher.run_cruncher()

    # Calculate Stats
    stats = cruncher.get_stats()
    click.echo(
        f"\nDone :: All images have been crunched."
        f"\n\nStats ::"
        f"\nImages crunched: {stats['images']}"
        f"\nVersions:        {stats['versions']}"
        f"\nImages created:  {stats['new_images']}"
        f"\nInput Size:      {stats['input_bytes'][0]} {stats['input_bytes'][1]}"
        f"\nOutput Size:     {stats['output_bytes'][0]} {stats['output_bytes'][1]}"
        f"\nPercent Reduced: {stats['percent_gain']}%"
        f"\nAverage Reduce:  {stats['average_gain']}%"
    )


if __name__ == '__main__':
    cli()

__version__ = '0.1.1'
