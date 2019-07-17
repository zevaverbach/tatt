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
@click.option("-s", "--save", is_flag=True, help="save to file")
@click.option(
    "-p", "--pretty", is_flag=True, help="pretty print, will make output non-pipeable"
)
@click.argument("name")
def get(name, save, pretty):
    """Downloads and/or saves completed transcript."""
    try:
        transcript, service = helpers.get_transcript(name)
    except exceptions.DoesntExistError:
        raise click.ClickException(f"no such transcript {name}")
    except exceptions.NotAvailable as e:
        raise click.ClickException(str(e))

    file = None
    if service.transcript_type == dict:
        transcript = json.dumps(transcript, indent=4 if pretty else None)
        filepath = f"{name}.json"
    else:
        filepath = f"{name}.txt"

    if save:
        file = open(filepath, "w")

    click.echo(transcript, file=file)

    if file:
        click.echo(f"Saved transcript to {filepath}.")
        file.close()


@cli.command()
@click.option("--service", type=str, help="STT service name")
@click.option("--status", type=str, help="completed | failed | in_progress")
def list(service, status):
    """Lists all transcription jobs."""
    if service is not None and service not in vendors.SERVICES:
        raise click.ClickException(f"no such service: {service}")

    try:
        all_jobs = get_transcription_jobs(service_name=service, status=status)
    except exceptions.ConfigError as e:
        raise click.ClickException(str(e))
    else:
        if not all_jobs:
            raise click.ClickException("no transcripts currently!")

        helpers.print_transcription_jobs(all_jobs)


@cli.command()
@click.option("-f", "--free-only", is_flag=True, help="only free services")
def services(free_only):
    """Lists available speech-to-text services."""
    click.echo(helpers.make_string_all_services(free_only))


@cli.command()
@click.argument("job_name", type=str)
def status(job_name):
    """Check the status of a transcription job."""
    try:
        jobs = get_transcription_jobs(name=job_name)
    except exceptions.DoesntExistError:
        raise click.ClickException("no job by that name")
    for job_list in jobs.values():
        for job in job_list:
            click.echo(f'{job["name"]}\t{job["status"]}')
            break
        break


@cli.command()
@click.argument("service_name", type=click.Choice(vendors.SERVICES))
def languages(service_name):
    service = get_service(service_name)
    languages_string = "\n" + "\n".join(service.language_list())
    click.echo(f"{service.name} supports {languages_string}")


@cli.command()
@click.option(
    "--punctuation",
    is_flag=True,
    default=True,
    help="only for Google Speech, defaults to True",
)
@click.option(
    "--speaker-id/--no-speaker-id",
    is_flag=True,
    default=True,
    help="only for google and amazon, defaults to True",
)
@click.option(
    "--num_speakers",
    default=2,
    type=int,
    help="only for google and amazon, defaults to 2",
)
@click.option(
    "--model",
    default="phone_call",
    help='only for Google Speech, defaults to "phone_call"',
)
@click.option(
    "--use-enhanced",
    is_flag=True,
    default=True,
    help="only for Google Speech, defaults to True",
)
@click.option(
    "--language-code",
    default="en-US",
    help="only for google and amazon, defaults to en-US",
)
@click.argument("media_filepath", type=str)
@click.argument("service_name", type=str)
def this(
    media_filepath,
    service_name,
    punctuation,
    speaker_id,
    num_speakers,
    model,
    use_enhanced,
    language_code,
):
    """Sends a media file to be transcribed."""
    if service_name == "google":
        transcribe_kwargs = dict(
            enable_automatic_punctuation=punctuation,
            enable_speaker_diarization=speaker_id,
            model=model,
            use_enhanced=use_enhanced,
            num_speakers=num_speakers,
            language_code=language_code,
        )
    elif service_name == "amazon":
        transcribe_kwargs = dict(
            enable_speaker_diarization=speaker_id,
            num_speakers=num_speakers,
            language_code=language_code,
        )
    else:
        transcribe_kwargs = {}

    try:
        service = get_service(service_name)
    except KeyError as e:
        raise click.ClickException(
            f"No such service! {helpers.make_string_all_services()}"
        )

    try:
        s = service(media_filepath)
    except exceptions.ConfigError as e:
        raise click.ClickException(str(e))

    click.echo(f"Okay, transcribing {media_filepath} using {service_name}...")

    try:
        job_num = s.transcribe(**transcribe_kwargs)
    except exceptions.AlreadyExistsError as e:
        raise click.ClickException(str(e))
    click.echo(
        f'Okay, job {job_num} is being transcribed.  Use "get" '
        "command to download it."
    )
