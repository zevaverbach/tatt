import io
import json
import os
import pathlib
import shutil
import tempfile
from time import sleep
from typing import List

from google.api_core import operations_v1
from google.cloud import (
    speech_v1p1beta1 as speech,
    storage,
    exceptions as gc_exceptions,
        )

from tatt import exceptions, helpers, config
from .vendor import TranscriberBaseClass

NAME = 'google'
BUCKET_NAME_TRANSCRIPT = config.BUCKET_NAME_FMTR_TRANSCRIPT_GOOGLE.format(
        'goog')


def _check_for_config():
    return os.getenv('GOOGLE_APPLICATION_CREDENTIALS') is not None


class Transcriber(TranscriberBaseClass):

    SUPPORTED_FORMATS = ['flac']
    cost_per_15_seconds = .009
    no_config_error_message = (
            'Please sign up for the Google Speech-to-Text API '
            'and put the path to your credentials in an '
            'environment variable "GOOGLE_APPLICATION_CREDENTIALS"'
            )

    if _check_for_config():
        speech_client = speech.SpeechClient()
        storage_client = storage.Client()
        transcript_bucket = storage_client.get_bucket(BUCKET_NAME_TRANSCRIPT)

    def __init__(self, filepath):
        super().__init__(filepath)

    @classmethod
    def _setup(cls):
        super()._setup()
        if not shutil.which('gsutil'):
            raise exceptions.DependencyRequired(
                'Please install gcloud using the steps here:'
                'https://cloud.google.com/storage/docs/gsutil_install')

        cls._make_bucket_if_doesnt_exist(BUCKET_NAME_TRANSCRIPT)

    @classmethod
    def _make_bucket_if_doesnt_exist(cls, bucket_name):
        try:
            cls.storage_client.create_bucket(bucket_name)
        except gc_exceptions.Conflict:
            # this might fail if a bucket by the name exists *anywhere* on GCS?
            return
        else:
            print('made Google Cloud Storage Bucket for transcripts')

    def convert_file_format_if_needed(self):
        if self.file_format not in self.SUPPORTED_FORMATS:
            if not shutil.which('ffmpeg'):
                raise exceptions.DependencyRequired('please install ffmpeg')
            self.filepath = helpers.convert_file(self.filepath, 'flac')

    @property
    def file_format(self):
        return pathlib.Path(self.filepath).suffix[1:].lower()

    @property
    def transcript_name(self):
        return self.basename + '.txt'

    @staticmethod
    def check_for_config() -> bool:
        return _check_for_config()

    def transcribe(self) -> str:
        self.convert_file_format_if_needed()
        self._request_transcription()

    def _check_if_transcript_exists(self, transcript_name=None):
        return storage.Blob(
                    bucket=self.transcript_bucket, 
                    name=transcript_name or self.transcript_name
                           ).exists(self.storage_client)

    def _request_transcription(
            self, 
            language_code='en-US',
            model='video',
            ) -> str:
        """Returns the job_name"""
        if self._check_if_transcript_exists():
            raise exceptions.AlreadyExistsError(
                f'{self.basename} already exists on {NAME}')
        num_audio_channels = helpers.get_num_audio_channels(self.filepath)

        with io.open(self.filepath, 'rb') as audio_file:
            content = audio_file.read()
            audio = speech.types.RecognitionAudio(content=content)

        config = speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=44100,
            audio_channel_count=num_audio_channels,
            enable_separate_recognition_per_channel=True,
            enable_word_confidence=True,
            enable_word_time_offsets=True,
            language_code=language_code,
            enable_automatic_punctuation=True,
            model=model,
            )

        self.operation = self.speech_client.long_running_recognize(config, 
                                                                   audio)

        print('transcribing...')
        while not self.operation.done():
            sleep(1)
            print('.')

        result_list = []

        for result in self.operation.result().results:
            result_list.append(str(result))

        print('saving transcript')
        transcript_path = '/tmp/transcript.txt'
        with open(transcript_path, 'w') as fout:
            fout.write('\n'.join(result_list))
        print('uploading transcript')
        self.upload_file(BUCKET_NAME_TRANSCRIPT, transcript_path)
        os.remove(transcript_path)

        return self.basename

    @classmethod
    def retrieve_transcript(cls, transcription_job_name: str) -> dict:
        """Get transcript from BUCKET_NAME_TRANSCRIPT"""
        if not cls._check_if_transcript_exists(
                cls,
                transcript_name=transcription_job_name):
            raise exceptions.DoesntExistError('no such transcript!')
        blob = cls.transcript_bucket.blob(transcription_job_name)
        f = tempfile.NamedTemporaryFile(delete=False)
        f.close()

        blob.download_to_filename(f.name)
        with open(f.name) as fin:
            transcript_text = fin.read()

        os.remove(f.name)
        return transcript_text

    def upload_file(self, bucket_name, path):
        blob = self.transcript_bucket.blob(self.transcript_name)
        blob.upload_from_filename(path)

    @classmethod
    def get_transcription_jobs(cls, job_name_query=None, status=None) -> List[dict]:

        if status and status.lower() != 'completed':
            return []

        jobs = []

        for t in cls.transcript_bucket.list_blobs():
            if job_name_query is not None and t.name != job_name_query:
                continue
            jobs.append({'name': t.name, 'status': 'COMPLETED'})

        return jobs
