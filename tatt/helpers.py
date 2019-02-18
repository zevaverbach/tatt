from tatt import config
from tatt import vendors


def make_string_all_services(free_only=False):
    all_services_string = (
          '\nHere are all the available '
         f'{"free " if free_only else ""}speech-to-text services:'
          '\n\n'
          '\n'.join(['{}{}{}{}'.format('\t', service_name, '\t\t',

                       f'({info["free"].replace("_", " ")})' 
                       if isinstance(info["free"], str) else ""
                       
                                      )

                     for service_name, info in
                     config.STT_SERVICES.items()])
          '\n'
    )
    return all_services_string


def get_service(service_name):
    return getattr(getattr(vendors, service_name), config.SERVICE_CLASS_NAME)


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


def get_transcription_jobs(service_name=None, name=None, status=None):
    all_jobs = {}
    for stt_name, data in config.STT_SERVICES.items():
        if service_name is None or service_name == stt_name:
            service = get_service(stt_name)
            service._setup() # check for AWS credentials and create buckets
            jobs = service.get_transcription_jobs(job_name_query=name,
                                                  status=status)
            if jobs:
                all_jobs[stt_name] = jobs
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
