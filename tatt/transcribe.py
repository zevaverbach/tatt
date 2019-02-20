import json
from pprint import pprint
import sqlite3
import sys

import click

from tatt import config, exceptions, helpers, vendors


@click.group()
def cli():
    pass


@cli.command()
@click.option('-s', '--save', is_flag=True, help='save to file')
@click.argument('name')
def get(name, save):
    """Downloads and/or saves completed transcript."""
    try:
        transcript = get_transcript(name)
    except exceptions.DoesntExistError:
        raise click.ClickException(f'no such transcript {name}')
    except exceptions.NotAvailable as e:
        raise click.ClickException(str(e))

    if not save:
        click.echo(transcript)
    else:
        with open(f'{name}.json', 'w') as fout:
            fout.write(json.dumps(transcript))
        click.echo(f'Okay, downloaded {name}.json')



@cli.command()
@click.option('-n', '--name', type=str, help="transcription job name")
@click.option('--service', type=str, help="STT service name")
@click.option('--status', type=str, help="completed | failed | in_progress")
def list(name, service, status):
    """Lists available STT services."""
    if service is not None and service not in vendors.SERVICES:
        raise click.ClickException(f'no such service: {service}')

    try:
        all_jobs = helpers.get_transcription_jobs(service, name, status)
    except exceptions.ConfigError as e:
        raise click.ClickException(str(e))
    else:
        if not all_jobs:
            raise click.ClickException('no transcripts currently!') 

        helpers.print_transcription_jobs(all_jobs)


@cli.command()
@click.option('-f', '--free-only', is_flag=True, help='only free services')
def services(free_only):
    """Lists available speech-to-text services."""
    click.echo(helpers.make_string_all_services(free_only))


@cli.command()
@click.argument('media_filepath', type=str)
@click.argument('service_name', type=str)
def this(dry_run, media_filepath, service_name):
    """Sends a media file to be transcribed."""
    try:
        service = helpers.get_service(service_name)
    except KeyError as e:
        raise click.ClickException(
            f'No such service! {print_all_services(print_=False)}')

    try:
        s = service(media_filepath)
    except exceptions.ConfigError as e:
        raise click.ClickException(str(e))

    click.echo(
      f'Okay, transcribing {media_filepath} using {service_name}...')

    try:
        job_num = s.transcribe()
    except exceptions.AlreadyExistsError as e:
        raise click.ClickException(str(e))
    click.echo(f'Okay, job {job_num} is being transcribed.  Use "get" '
           'command to download it.')
