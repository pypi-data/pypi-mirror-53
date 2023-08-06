""" Commands to configure BWDT """
import click

import bwdt.auth as auth


@click.option('--key-id', help='Auth Key ID', default=None)
@click.option('--key', help='Auth Key', default=None)
@click.option('--online/--offline', help='Online/Offline mode', default=True)
@click.option('--offline-path', default=None,
              help='Path to offline installer files')
@click.command()
def configure(key_id, key, online, offline_path):
    """ Launch the configuration setup """
    made_dir = auth.mkdir()
    if made_dir:
        click.echo('Created directory {}'.format(auth.get_dir_path()))
    click.echo('Writing {}'.format(auth.get_file_path()))
    offline = not online
    data = auth.get()
    if data is not None:
        if key_id is None:
            key_id = data['key_id']
        if key is None:
            key = data['key']
        if offline is None:
            offline = data['offline']
        if offline_path is None:
            offline_path = data['offline_path']
    auth.set(key_id=key_id, key=key, offline=offline,
             offline_path=offline_path)
    data = auth.get()
    click.echo('Key ID: {}'.format(data['key_id']))
    click.echo('Offline: {}'.format(data['offline']))
    click.echo('Offline Path: {}'.format(data['offline_path']))
