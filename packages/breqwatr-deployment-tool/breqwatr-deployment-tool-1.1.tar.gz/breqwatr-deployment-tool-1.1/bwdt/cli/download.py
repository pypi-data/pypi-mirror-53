""" Commands for downloading from s3 """
import os
import sys

import click

from bwdt.aws.s3 import S3
from bwdt.constants import CLOUDYML_KEY, OSTOOLS_KEY, S3_BUCKET


@click.group(name='download')
def download_group():
    """ Download files for offline install """


def _handle_path(path, key, force):
    """ Handle download paths """
    if os.path.isdir(path):
        path = '{}/{}'.format(path, key)
    else:
        err = 'ERROR: path {} must be a directory and exist\n'.format(path)
        sys.stderr.write(err)
        sys.exit(1)
    if os.path.exists(path) and not force:
        err = 'ERROR: File {} exists. Use --force to overwrite\n'.format(path)
        sys.stderr.write(err)
        sys.exit(1)


@click.argument('path')
@click.option('--force/--no-force', default=False,
              help='Use --force to overwrite file if it already exists')
@click.command()
def ostools(path, force):
    """ Download the offline OS Tools Tarball """
    _handle_path(path, OSTOOLS_KEY, force)
    click.echo('Saving {}'.format(path))
    full_path = '{}/{}'.format(path, OSTOOLS_KEY)
    S3().download(full_path, S3_BUCKET, OSTOOLS_KEY)


@click.argument('path')
@click.option('--force/--no-force', default=False,
              help='Use --force to overwrite file if it already exists')
@click.command(name='cloud-yml')
def cloud_yml(path, force):
    """ Download a commented cloud.yml template """
    _handle_path(path, CLOUDYML_KEY, force)
    click.echo('Saving {}/{}'.format(path, CLOUDYML_KEY))
    full_path = '{}/{}'.format(path, CLOUDYML_KEY)
    S3().download(full_path, S3_BUCKET, CLOUDYML_KEY)


download_group.add_command(ostools)
download_group.add_command(cloud_yml)
