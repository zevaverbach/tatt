import json
import os
from pathlib import PurePath
from subprocess import check_output
from typing import List, Dict, Union
import uuid

import boto3

from tatt import config
from tatt import exceptions
from .vendor import TranscriberBaseClass

NAME = "amazon"
BUCKET_NAME_MEDIA = config.BUCKET_NAME_FMTR_MEDIA.format(NAME)
BUCKET_NAME_TRANSCRIPT = config.BUCKET_NAME_FMTR_TRANSCRIPT.format(NAME)
TRANSCRIPT_TYPE = dict


def _check_for_config() -> bool:
    return (
        config.AWS_CONFIG_FILEPATH.exists() and config.AWS_CREDENTIALS_FILEPATH.exists()
    )


class Transcriber(TranscriberBaseClass):

    name = NAME
    cost_per_15_seconds = 0.024 / 4
    bucket_names = {"media": BUCKET_NAME_MEDIA, "transcript": BUCKET_NAME_TRANSCRIPT}

    no_config_error_message = 'please run "aws configure" first'
    transcript_type = TRANSCRIPT_TYPE
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe.html
    _language_list = [
        "en-US",
        "es-US",
        "en-AU",
        "fr-CA",
        "en-GB",
        "de-DE",
        "pt-BR",
        "fr-FR",
        "it-IT",
        "ko-KR",
    ]

    if _check_for_config():
        tr = boto3.client("transcribe")
        s3 = boto3.resource("s3")

    def __init__(self, filepath):
        super().__init__(filepath)
        self._setup()
        self.filepath = PurePath(filepath)
        self.basename = str(os.path.basename(self.filepath))

    @classmethod
    def check_for_config(cls):
        return _check_for_config()

    @property
    def media_file_uri(self):
        return (
            f"https://s3-{config.AWS_REGION}.amazonaws.com/"
            f"{self.bucket_names['media']}/{self.basename}"
        )

    @classmethod
    def _setup(cls):
        super()._setup()
        for bucket_name in cls.bucket_names.values():
            if not cls.check_for_bucket(bucket_name):
                cls.make_bucket(bucket_name)

    @classmethod
    def check_for_bucket(cls, bucket_name: str) -> bool:
        return bool(cls.s3.Bucket(bucket_name).creation_date)

    @classmethod
    def make_bucket(cls, bucket_name):
        cls.s3.create_bucket(Bucket=bucket_name)

    def transcribe(self, **kwargs) -> str:
        super().transcribe(**kwargs)
        self._upload_file()
        try:
            return self._request_transcription(**kwargs)
        except self.tr.exceptions.ConflictException:
            raise exceptions.AlreadyExistsError(
                f"{self.basename} already exists on {NAME}"
            )

    def _upload_file(self):
        self.s3.Bucket(self.bucket_names["media"]).upload_file(
            str(self.filepath), self.basename
        )

    def _request_transcription(
        self, language_code="en-US", num_speakers=2, enable_speaker_diarization=True
    ) -> str:
        job_name = self.basename

        kwargs = dict(
            TranscriptionJobName=job_name,
            LanguageCode=language_code,
            MediaFormat=self.basename.split(".")[-1].lower(),
            Media={"MediaFileUri": self.media_file_uri},
            OutputBucketName=self.bucket_names["transcript"],
        )

        if enable_speaker_diarization:
            kwargs.update(
                dict(
                    Settings={
                        "ShowSpeakerLabels": True,
                        "MaxSpeakerLabels": num_speakers,
                    }
                )
            )

        self.tr.start_transcription_job(**kwargs)
        return job_name

    @classmethod
    def get_transcription_jobs(
        cls, status: str = None, job_name_query: str = None
    ) -> List[dict]:

        kwargs = {"MaxResults": 100}

        if status is not None:
            kwargs["Status"] = status.upper()
        if job_name_query is not None:
            kwargs["JobNameContains"] = job_name_query

        jobs_data = cls.tr.list_transcription_jobs(**kwargs)
        key = "TranscriptionJobSummaries"

        jobs = cls.homogenize_transcription_job_data(jobs_data[key])

        while jobs_data.get("NextToken"):
            token = jobs_data["NextToken"]
            jobs_data = cls.tr.list_transcription_jobs(NextToken=token)
            jobs += cls.homogenize_transcription_job_data(jobs_data[key])

        return jobs

    @classmethod
    def retrieve_transcript(cls, transcription_job_name: str) -> TRANSCRIPT_TYPE:
        job = cls.tr.get_transcription_job(TranscriptionJobName=transcription_job_name)[
            "TranscriptionJob"
        ]

        if not job["TranscriptionJobStatus"] == "COMPLETED":
            return

        transcript_file_uri = job["Transcript"]["TranscriptFileUri"]
        transcript_path = transcript_file_uri.split("amazonaws.com/", 1)[1]

        transcript_bucket = transcript_path.split("/", 1)[0]
        transcript_key = transcript_path.split("/", 1)[1]

        s3_object = cls.s3.Object(transcript_bucket, transcript_key).get()
        transcript_json = s3_object["Body"].read().decode("utf-8")
        return json.loads(transcript_json)

    @staticmethod
    def homogenize_transcription_job_data(transcription_job_data):
        return [
            {
                "created": jd["CreationTime"],
                "name": jd["TranscriptionJobName"],
                "status": jd["TranscriptionJobStatus"],
            }
            for jd in transcription_job_data
        ]
