import json
import os
from pathlib import PurePath
from subprocess import check_output
import uuid

import boto3

from tatt import config
from tatt import exceptions

NAME = 'amazon'
BUCKET_NAME_MEDIA = config.AWS_BUCKET_NAME_FMTR_MEDIA.format(NAME)
BUCKET_NAME_TRANSCRIPT = config.AWS_BUCKET_NAME_FMTR_TRANSCRIPT.format(NAME)
if check_for_config():
    tr = boto3.client('transcribe')
    s3 = boto3.resource('s3')


class transcribe:

    bucket_names = {'media': BUCKET_NAME_MEDIA,
                    'transcript': BUCKET_NAME_TRANSCRIPT}
    service_name = 'amazon'

    def __init__(self, filepath):
        self._setup()
        self.filepath = PurePath(filepath)
        self.basename = str(os.path.basename(self.filepath))
        self.media_file_uri = (
                f"https://s3-{config.AWS_REGION}.amazonaws.com/"
                f"{self.bucket_names['media']}/{self.basename}")

    @classmethod
    def _setup(cls):
        if not check_for_config():
            raise exceptions.ConfigError('please run "aws configure" first')
        for bucket_name in cls.bucket_names.values():
            if not cls.check_for_bucket(bucket_name):
                cls.make_bucket(bucket_name)

    @staticmethod
    def check_for_bucket(bucket_name):
        return bool(s3.Bucket(bucket_name).creation_date)

    @staticmethod
    def make_bucket(bucket_name):
        s3.create_bucket(Bucket=bucket_name)

    def transcribe(self):
        self._upload_file()
        try:
            return self._request_transcription()
        except tr.exceptions.ConflictException:
            raise exceptions.AlreadyExistsError(
                f'{self.basename} already exists on {self.service_name}')

    def _upload_file(self):
        s3.Bucket(self.bucket_names['media']).upload_file(
                str(self.filepath),
                self.basename)

    def _request_transcription(self, language_code='en-US'):
        job_name = self.basename
        tr.start_transcription_job(
                TranscriptionJobName=job_name,
                LanguageCode=language_code,
                MediaFormat=self.basename.split('.')[-1].lower(),
                Media={
                    'MediaFileUri': self.media_file_uri
                    },
                OutputBucketName=self.bucket_names['transcript']
                )
        return job_name

    @classmethod
    def get_completed_jobs(cls, job_name_query=None):
        return cls.get_transcription_jobs(
                status='completed',
                job_name_query=job_name_query)

    @classmethod
    def get_pending_jobs(cls, job_name_query=None):
        return cls.get_transcription_jobs(
                status='in_progress',
                job_name_query=job_name_query)

    @classmethod
    def get_all_jobs(cls, job_name_query=None):
        return cls.get_transcription_jobs(job_name_query)

    @staticmethod
    def get_transcription_jobs(status=None, job_name_query=None):
        kwargs = {'MaxResults': 100}
        if status is not None:
            kwargs['Status'] = status.upper()
        if job_name_query is not None:
            kwargs['JobNameContains'] = job_name_query
        jobs_data = tr.list_transcription_jobs(**kwargs)
        jobs = homogenize_transcription_job_data(jobs_data['TranscriptionJobSummaries'])
        while jobs_data.get('NextToken'):
            jobs_data = tr.list_transcription_jobs(NextToken=jobs_data['NextToken'])
            jobs += homogenize_transcription_job_data(
                        jobs_data['TranscriptionJobSummaries'])
        return jobs

    @staticmethod
    def retrieve_transcript(transcription_job_name):
        job = tr.get_transcription_job(
            TranscriptionJobName=transcription_job_name
        )['TranscriptionJob']

        if not job['TranscriptionJobStatus'] == 'COMPLETED':
            return

        transcript_file_uri = job['Transcript']['TranscriptFileUri']
        transcript_path = transcript_file_uri.split("amazonaws.com/", 1)[1]

        transcript_bucket = transcript_path.split('/', 1)[0]
        transcript_key = transcript_path.split('/', 1)[1]

        s3_object = s3.Object(transcript_bucket, transcript_key).get()
        transcript_json = s3_object['Body'].read().decode('utf-8')
        return json.loads(transcript_json)




def homogenize_transcription_job_data(transcription_job_data):
    return [{
                'created': jd['CreationTime'],
                'name': jd['TranscriptionJobName'],
                'status': jd['TranscriptionJobStatus']
            }
            for jd in transcription_job_data]


def check_for_config():
    return config.AWS_CONFIG_FILEPATH.exists()


def shell_call(command):
    return check_output(command, shell=True)
