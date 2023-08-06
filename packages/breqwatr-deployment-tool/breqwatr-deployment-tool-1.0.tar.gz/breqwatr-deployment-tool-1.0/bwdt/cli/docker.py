""" Commands for operating Docker on the host """
# pylint disable=broad-except,W0703
import click

import bwdt.auth
from bwdt.constants import KOLLA_IMAGE_TAGS, SERVICE_IMAGE_TAGS
from bwdt.container import Docker, get_image_as_filename, offline_image_exists


def _all_images():
    """ Return dict of all images """
    images = {}
    images.update(SERVICE_IMAGE_TAGS)
    images.update(KOLLA_IMAGE_TAGS)
    return images


@click.group(name='docker')
def docker_group():
    """ Command group for local docker commands """


def _pull(repository, tag):
    """ Reusable pull command """
    if tag is None:
        tag = _all_images()[repository]
    click.echo('Pulling {}:{}'.format(repository, tag))
    Docker().pull(repository=repository, tag=tag)


@click.argument('repository')
@click.option('--tag', default=None,
              help='optional tag to pull, default=(current stable)')
@click.command(name='pull')
def pull_one(repository, tag):
    """ Pull an image from the upstream registry """
    _pull(repository, tag)


@click.option('--tag', default=None, required=False,
              help='optional tag to pull. Default=(current stable)')
@click.command(name='pull-all')
def pull_all(tag):
    """ Pull all images """
    all_images = _all_images()
    i = 1
    count = len(all_images)
    for repository in all_images:
        click.echo('Pulling image {} of {}'.format(i, count))
        _pull(repository, tag)
        i += 1


def _export_image(repository, tag, pull, force):
    """ Re-usable command to export image to directory """
    if tag is None:
        tag = _all_images()[repository]
    if offline_image_exists(repository, tag) and not force:
        base = bwdt.auth.get()['offline_path']
        filename = get_image_as_filename(repository, tag, base)
        click.echo('Skipping (already exists): {}'.format(filename))
        return
    client = Docker()
    # try:
    if pull:
        click.echo('Pulling {}:{}'.format(repository, tag))
        client.pull(repository=repository, tag=tag)
    offln_path = bwdt.auth.get()['offline_path']
    click.echo('Saving {}:{} to {}'.format(repository, tag, offln_path))
    client.export_image(repository, tag)


@click.argument('repository')
@click.option('--tag', required=False, help='Image tag', default=None)
@click.option('--pull/--no-pull', required=False, default=True,
              help='Use --no-pull to keep older image for this export')
@click.option('--force/--keep-old', required=False, default=False,
              help='--force will overwrite files found at the destination')
@click.command(name='export-image')
def export_image(repository, tag, pull, force):
    """ Export an image to directory """
    _export_image(repository, tag, pull, force)

@click.option('--pull/--no-pull', required=False, default=True,
              help='Use --no-pull to keep older image for this export')
@click.option('--tag', default=None, required=False,
              help='optional tag to pull. Default=(current stable)')
@click.option('--force/--keep-old', required=False, default=False,
              help='--force will overwrite files found at the destination')
@click.command(name='export-image-all')
def export_image_all(pull, tag, force):
    """ Export all images to directory  """
    all_images = _all_images()
    i = 1
    count = len(all_images)
    for repository in all_images:
        click.echo('Exporting image {} of {}'.format(i, count))
        _export_image(repository, tag, pull, force)
        i += 1


docker_group.add_command(pull_one)
docker_group.add_command(pull_all)
docker_group.add_command(export_image)
docker_group.add_command(export_image_all)
