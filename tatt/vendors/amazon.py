import os
from pathlib import PurePath
from subprocess import check_output

import boto3

import config

NAME = 'amazon'
BUCKET_NAME = config.DEFAULT_BUCKET_NAME_FORMATTER.format(NAME)):



class ConfigError(Exception):
    pass


class Transcribe:

    bucket_name = BUCKET_NAME

    def __init__(self, filepath):
        self._setup()
        self.s3 = boto3.resource('s3')
        self.filepath = PurePath(filepath)

    def setup(self):
        if not check_for_credentials():
            make_credentials() and check_for_credentials() or raise ConfigError
        if not self.check_for_bucket():
            self.make_bucket()

    def check_for_bucket(self):
        return bool(self.s3.Bucket(self.bucket_name).creation_date)

    def make_bucket(self):
        s3.create_bucket(Bucket=self.bucket_name)

    def transcribe(self):
        upload_file(self.filepath)
        self.request_transcription()

    def upload_file(self):
        basename = os.path.basename(filepath)
        s3.Bucket(bucket_name).upload_file(filepath, basename)
        return basename

    def request_transcription(self):



def check_for_credentials():
    os.path.exists(config.AWS_CREDENTIALS_FILEPATH)


def make_credentials():
    shell_call('aws configure')


def shell_call(command):
    return check_output(command, shell=True)
