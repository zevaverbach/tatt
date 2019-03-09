import pathlib
import re
import subprocess
from typing import Dict, List

import audioread

from tatt import config, exceptions, vendors
from tatt.vendors.vendor import TranscriberBaseClass


def make_string_all_services(free_only=False):
    all_services_string_formatter = (
        "\nHere are all the available {}speech-to-text-services:\n\n"
        )

    format_fill = ""
    if free_only:
        format_fill = "free "
    all_services_string = all_services_string_formatter.format(format_fill)

    

    for service_name, module in vendors.SERVICES.items():
        transcriber = getattr(module, config.SERVICE_CLASS_NAME)
        if free_only and transcriber.cost_per_15_seconds > 0:
            continue
        all_services_string += (
   f'\t{service_name}\t\t${transcriber.cost_per_15_seconds} per 15 seconds\n'
        )

    return all_services_string + '\n'


def get_job(job_name):
    job = get_transcription_jobs_dict().get(job_name)
    if not job:
        raise exceptions.DoesntExistError
    if job['status'].lower() != 'completed':
        raise exceptions.NotAvailable(f'transcript status is {job["status"]}')
    return job


def get_transcript(job_name) -> tuple:
    job = get_job(job_name)
    service = get_service(job['service_name'])
    transcript = service.retrieve_transcript(job_name)
    return transcript, service


def get_transcript_format(job_name) -> str:
    job = get_job(job_name)
    service = get_service(job['service_name'])
    return service.transcript_type


def get_service(service_name) -> TranscriberBaseClass:
    module = vendors.SERVICES[service_name]
    return getattr(module, config.SERVICE_CLASS_NAME)


def print_transcription_jobs(jobs):
    max_job_name_length = max(len(job['name']) 
                                  for job_list in jobs.values()
                                  for job in job_list)
    max_service_name_length = max(len(provider_name) for provider_name in jobs)
    print()
    print('Service',
          'Job Name', 
          (max_job_name_length - len('Job Name')) * ' ',
          '  Status')
    print('-------',
          '--------',
          (max_job_name_length - len('Job Name')) * ' ', 
          '  ------')

    for provider_name, job_list in jobs.items():
        for job in job_list:
            num_spaces_between = max_job_name_length - len(job['name'])
            print(provider_name, job['name'], ' ' * num_spaces_between,
                    job['status'], sep='  ')
    print()


def get_transcription_jobs(
        service_name=None, 
        name=None, 
        status=None
        ) -> Dict[str, List[dict]]:
    all_jobs = {}
    for stt_name in vendors.SERVICES:
        if service_name is None or service_name == stt_name:
            service = get_service(stt_name)
            service._setup()
            jobs = service.get_transcription_jobs(job_name_query=name,
                                                  status=status)
            if jobs:
                if name:
                    jobs = get_exact_name_matches(jobs, name)
                    # this is because AWS Transcribe doesn't have exact file
                    # search
                    if not jobs:
                        continue
                all_jobs[stt_name] = jobs

    if name and len(all_jobs) == 0:
        raise exceptions.DoesntExistError

    return all_jobs


def get_exact_name_matches(jobs, name):
    exact_match_jobs = []
    for job in jobs:
        if job['name'] == name:
            exact_match_jobs.append(job)
    return exact_match_jobs


def get_transcription_jobs_dict():
    jobs = get_transcription_jobs()
    return {
            job['name']: {
                'service_name': service_name,
                'status': job['status']
                }
            for service_name, job_list in jobs.items()
            for job in job_list
            }


def get_num_audio_channels(filepath):
    return get_media_info(filepath).channels


def get_sample_rate(filepath):
    return get_media_info(filepath).samplerate


def get_media_info(filepath):
    if isinstance(filepath, pathlib.PurePosixPath):
        filepath = str(filepath)
    with audioread.audio_open(filepath) as f:
        return f


def shell_call(command):
    return subprocess.check_output(command, shell=True)


def change_file_extension(filepath, format_name):
    extension = pathlib.Path(filepath).suffix
    if isinstance(filepath, pathlib.PurePosixPath):
        filepath = str(filepath)
    return filepath.replace(extension, f'.{format_name}')


def convert_file(filepath, format_name):
    if format_name != 'flac':
        raise NotSupported('Only flac is supported currently.')
    else:
        convert_flags = '-c:a flac'

    output_filepath = change_file_extension(filepath, format_name)
    shell_call(f'ffmpeg -y -i {filepath} {convert_flags} {output_filepath}')
    return output_filepath
