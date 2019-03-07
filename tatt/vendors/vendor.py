import abc
import os
from pathlib import PurePath
from typing import List

from tatt import exceptions


class TranscriberBaseClass:

    __metaclass__ = abc.ABCMeta

    def __init__(self, filepath):
        self._setup()
        self.filepath = PurePath(filepath)
        self.basename = str(os.path.basename(self.filepath))

    @property
    @abc.abstractmethod
    def no_config_error_message(self):
        """
        This must be defined as a class attribute, to be printed when raising
        such an error.
        """
        pass

    @property
    @abc.abstractmethod
    def cost_per_15_seconds(self):
        """This must be defined as a class attribute."""
        pass

    @classmethod
    def _setup(cls):
        if not cls.check_for_config():
            raise exceptions.ConfigError(cls.no_config_error_message)

    @staticmethod
    @abc.abstractmethod
    def check_for_config() -> bool:
        pass

    @abc.abstractmethod
    def transcribe(self) -> str:
        """
        This should do any required logic, 
        then call self._request_transcription.
        It should return the job_name.
        """
        pass

    @abc.abstractmethod
    def _request_transcription(self) -> str:
        """Returns the job_name"""
        pass

    @classmethod
    @abc.abstractmethod
    def retrieve_transcript(transcription_job_name: str) -> dict:
        pass

    @classmethod
    @abc.abstractmethod
    def get_transcription_jobs() -> List[dict]:
        pass

