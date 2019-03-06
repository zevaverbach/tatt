import io
import json
import os
import pathlib

from google.cloud import speech_v1p1beta1 as speech

from tatt import exceptions, helpers, config
from .vendor import TranscriberBaseClass

NAME = 'google'
BUCKET_NAME_TRANSCRIPT = config.BUCKET_NAME_FMTR_TRANSCRIPT.format(NAME)


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
        client = speech.SpeechClient()

    def __init__(self, filepath):
        super().__init__(filepath)
        self.convert_file_format_if_needed()

    @classmethod
    def _setup(cls):
        super()._setup()
        if not cls.check_for_bucket(BUCKET_NAME_TRANSCRIPT):
            print('creating a transcript bucket on Google Cloud Storage')
            cls.make_bucket(BUCKET_NAME_TRANSCRIPT)

    @classmethod
    def make_bucket(cls, bucket_name):
        pass

    @classmethod
    def check_for_bucket(cls, bucket_name):
        pass

    def convert_file_format_if_needed(self):
        if self.file_format not in self.SUPPORTED_FORMATS:
            self.filepath = helpers.convert_file(self.filepath, 'flac')

    @property
    def file_format(self):
        return pathlib.Path(self.filepath).suffix[1:].lower()

    @staticmethod
    def check_for_config() -> bool:
        return _check_for_config()

    def transcribe(self) -> str:
        """
        This should do any required logic, 
        then call self._request_transcription.
        It should return the job_name.
        """
        self._request_transcription()

    def _request_transcription(
            self, 
            language_code='en-US',
            model='video',
            ) -> str:
        """Returns the job_name"""
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

        self.operation = self.client.long_running_recognize(config, audio)

        def my_callback(future):
            result = future.result()
            # save json.dumps(result) to file
            # TODO: see what others have done to make this easy (BBC guy)
            self.upload_file(BUCKET_NAME_TRANSCRIPT, filepath)
            # delete file

        self.operation.add_done_callback(my_callback)

        return self.filepath.name

    @classmethod
    def retrieve_transcript(cls, transcription_job_name: str) -> dict:
        """Get transcript from BUCKET_NAME_TRANSCRIPT"""
        # for result in results:

            # leave enable_automatic_punctuation in?  it is applied to the words
            # themselves, so it'll have to be processed...

            # for word in result.alternatives[0].words:
            #     print(word)
            #     print(type(word))
            #     print(dir(word))

        pass

    @classmethod
    def upload_file(cls, bucket_name, path):
        pass

    @classmethod
    def get_transcription_jobs(job_name_query, status):
        """
        Store pending jobs in some simple db or document, 
        then remove them when the transcript appears in the bucket.
        """
        pass

