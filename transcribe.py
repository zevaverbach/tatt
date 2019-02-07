import sys

import click

from config import STT_SERVICES


@click.group()
def cli():
    pass


@cli.command()
@click.option('-f', '--free-only', is_flag=True)
def services(free_only):
    """Lists available speech-to-text services."""
    print_all_services(free_only)


@cli.command()
@click.option('-d', '--dry-run', default=False, help=(
  'Do a dry run without actually submitting the media file for transcription'))
@click.argument('media_filepath', type=click.File('r'))
@click.argument('service_name', type=str)
def this(dry_run, media_filepath, service_name):
    """Transcribe All The Things!™"""
    if service_name not in STT_SERVICES:
        print()
        raise click.ClickException(
            f'No such service! {print_all_services(print_=False)}')
    if dry_run:
        print('If this weren\'t a dry run, I would transcribe '
             f'{media_filepath.name} using {service_name}')
        print(STT_SERVICES[service_name])
    else:
        print(
          f'Okay, transcribing {media_filepath.name} using {service_name}...')
        print(STT_SERVICES[service_name]['function'])


def print_all_services(free_only=False, print_=True):
    # TODO: make a jinja template for this
    all_services_string = (
         '\n\nHere are all the available ' +
         f'{"free " if free_only else ""}speech-to-text services:' +
        '\n\n' +
        '\n'.join(['{}{}{}{}'.format('\t', service_name, '\t\t',

                       f'({info["free"].replace("_", " ")})' 
                       if isinstance(info["free"], str) else ""
                       
                                      )

                     for service_name, info in
                     STT_SERVICES.items()])
        + '\n'
    )
    if print_:
        print(all_services_string)
    return all_services_string
