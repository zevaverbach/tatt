import json
from pprint import pprint
import sqlite3
import sys

import click

import config
import exceptions
import helpers
from tatt import vendors


@click.group()
def cli():
    pass


@cli.command()
@click.option('-f', '--file', is_flag=True)
@click.argument('name')
def get(name, file):
    job = helpers.get_transcription_jobs_dict().get(name)
    if not job:
        raise click.ClickException(f'no such transcript {name}')
    if job['status'].lower() != 'completed':
        raise click.ClickException(f'transcript status is {job["status"]}')
    service = helpers.get_service(job['service_name'])
    if not file:
        pprint(service.retrieve_transcript(name))
    with open(f'{name}.json', 'w') as fout:
        fout.write(json.dumps(service.retrieve_transcript(name)))



@cli.command()
@click.option('-n', '--name', type=str)
@click.option('--service', type=str)
@click.option('--status', type=str)
def list(name, service, status):
    if service is not None and service not in config.STT_SERVICES:
        raise click.ClickException(f'no such service: {service}')

    all_jobs = helpers.get_transcription_jobs(service, name, status)
    if not all_jobs:
        click.ClickException('no transcripts currently!') 

    helpers.print_transcription_jobs(all_jobs)


@cli.command()
@click.option('-f', '--free-only', is_flag=True)
def services(free_only):
    """Lists available speech-to-text services."""
    helpers.print_all_services(free_only)


@cli.command()
@click.option('-d', '--dry-run', is_flag=True, help=(
  'Do a dry run without actually submitting the media file for transcription'))
@click.argument('media_filepath', type=str)
@click.argument('service_name', type=str)
def this(dry_run, media_filepath, service_name):
    """Transcribe All The Things!™"""
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


