import json
from pprint import pprint
import sqlite3
import sys

import click

from tatt import config, exceptions, helpers, vendors
from tatt.helpers import get_transcription_jobs, get_service


@click.group()
def cli():
    pass


@cli.command()
@click.option('-s', '--save', is_flag=True, help='save to file')
@click.option('-p', '--pretty', is_flag=True, 
              help='pretty print, will make output non-pipeable')
@click.argument('name')
def get(name, save, pretty):
    """Downloads and/or saves completed transcript."""
    try:
        transcript = json.dumps(helpers.get_transcript(name), 
                                indent=4 if pretty else None)
    except exceptions.DoesntExistError:
        raise click.ClickException(f'no such transcript {name}')
    except exceptions.NotAvailable as e:
        raise click.ClickException(str(e))

    file = None
    if save:
        filepath = f'{name}.json', 'w'
        file = open(filepath)

    click.echo(transcript, file=file)

    if file:
        click.echo(f'Saved transcript to {filepath}.')
        file.close()



@cli.command()
@click.option('--service', type=str, help="STT service name")
@click.option('-n', '--name', type=str, help="transcription job name")
@click.option('--status', type=str, help="completed | failed | in_progress")
def list(service, name, status):
    """Lists available STT services."""
    if service is not None and service not in vendors.SERVICES:
        raise click.ClickException(f'no such service: {service}')

    try:
        all_jobs = get_transcription_jobs(service, name, status)
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
@click.argument('job_name', type=str)
def status(job_name):
    jobs = get_transcription_jobs(name=job_name)
    if not jobs or not list(jobs.values())[0]:
        raise click.ClickException('no job by that name')
    click.echo(list(jobs.values())[0][0]['status'])


@cli.command()
@click.argument('media_filepath', type=str)
@click.argument('service_name', type=str)
def this(media_filepath, service_name):
    """Sends a media file to be transcribed."""
    try:
        service = get_service(service_name)
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
