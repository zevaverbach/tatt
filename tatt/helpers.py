from typing import Dict, List

from tatt import config, exceptions, vendors

LB = '\n'
TAB = '\t'


def make_string_all_services(free_only=False):
    all_services_string_formatter = (
        "\nHere are all the available {}speech-to-text-services:\n\n"
        )

    format_fill = ""
    if free_only:
        format_fill = "free "
    all_services_string = all_services_string_formatter.format(format_fill)

    for service_name, module in vendors.SERVICES.items():
        if free_only and module.cost_per_15_seconds > 0:
            continue
        all_services_string += (
   f'{TAB}{service_name}{TAB}{TAB}${module.cost_per_15_seconds} per 15 seconds'
        )

    return all_services_string + '\n'


def get_job(job_name):
    job = get_transcription_jobs_dict().get(job_name)
    if not job:
        raise exceptions.DoesntExistError
    if job['status'].lower() != 'completed':
        raise exceptions.NotAvailable(f'transcript status is {job["status"]}')
    return job


def get_transcript(job_name):
    job = get_job(job_name)
    service = get_service(job['service_name'])
    return service.retrieve_transcript(job_name)


def get_service(service_name):
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
            service._setup() # check for AWS credentials and create buckets
            jobs = service.get_transcription_jobs(job_name_query=name,
                                                  status=status)
            if jobs:
                all_jobs[stt_name] = jobs

    if name and len(all_jobs) == 0:
        raise exceptions.DoesntExistError

    return all_jobs


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
