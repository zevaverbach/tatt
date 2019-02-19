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
@click.option('-f', '--file', is_flag=True, help='save to file')
@click.argument('name')
def get(name, file):
    """Downloads and/or saves completed transcript."""
    job = helpers.get_transcription_jobs_dict().get(name)
    if not job:
        raise click.ClickException(f'no such transcript {name}')
    if job['status'].lower() != 'completed':
        raise click.ClickException(f'transcript status is {job["status"]}')
    service = helpers.get_service(job['service_name'])
    if not file:
        pprint(service.retrieve_transcript(name))
    else:
        with open(f'{name}.json', 'w') as fout:
            fout.write(json.dumps(service.retrieve_transcript(name)))
            print(f'Okay, downloaded {name}.json')



@cli.command()
@click.option('-n', '--name', type=str, help="transcription job name")
@click.option('--service', type=str, help="STT service name")
@click.option('--status', type=str, help="completed | failed | in_progress")
def list(name, service, status):
    """Lists available STT services."""
    if service is not None and service not in config.STT_SERVICES:
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
@click.option('-d', '--dry-run', is_flag=True, help=(
  'Do a dry run without actually submitting the media file for transcription'))
@click.argument('media_filepath', type=str)
@click.argument('service_name', type=str)
def this(dry_run, media_filepath, service_name):
    """Sends a media file to be transcribed."""
    if service_name not in config.STT_SERVICES:
        print()
        raise click.ClickException(
            f'No such service! {print_all_services(print_=False)}')

    service = helpers.get_service(service_name)
    s = service(media_filepath)

    if dry_run:
        print('If this weren\'t a dry run, I would transcribe '
             f'{media_filepath} using {service_name}')
        pprint(vars(s))
    else:
        print(
          f'Okay, transcribing {media_filepath} using {service_name}...')

        try:
            job_num = s.transcribe()
        except exceptions.AlreadyExistsError as e:
            raise click.ClickException(str(e))
        print(f'Okay, job {job_num} is being transcribed.  Use "get" '
               'command to download it.')
