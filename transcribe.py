from pprint import pprint
import sqlite3
import sys

import click

import config
import helpers
from tatt import vendors


@click.group()
def cli():
    pass


@cli.command()
@click.argument('uid', required=False)
def retrieve(name=None, service=None):
    pending_jobs = [get_service(service_name).get_pending_jobs(name)
                    for service_name, data in config.STT_SERVICES
                    if service is None
                    or service == service_name]
    if not pending_jobs:
        click.ClickException('no pending jobs currently!') 
    for job in pending_jobs:
        print(dict(job))


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

    service = get_service(service_name)
    s = service(media_filepath)

    if dry_run:
        print('If this weren\'t a dry run, I would transcribe '
             f'{media_filepath} using {service_name}')
        pprint(vars(s))
    else:
        print(
          f'Okay, transcribing {media_filepath} using {service_name}...')

        job_num = s.transcribe()
        db.create_pending_job(job_num, s.basename, service_name)
        print(f'Okay, job {job_num} is being transcribed.  Use "retrieve" '
               'command to download it.')


def get_service(service_name):
    return getattr(getattr(vendors, service_name), config.SERVICE_CLASS_NAME)


