import abc
import os
from pathlib import PurePath
from typing import List, Union

from tatt import exceptions


class TranscriberBaseClass:

    __metaclass__ = abc.ABCMeta

    def __init__(self, filepath):
        self._setup()
        if " " in filepath:
            raise exceptions.FormatError("Please don't put any spaces in the filename.")
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
    def transcript_type(self):
        pass

    @property
    @abc.abstractmethod
    def _language_list(self):
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

    @classmethod
    @abc.abstractmethod
    def check_for_config(cls) -> bool:
        pass

    def transcribe(self, **kwargs) -> str:
        """
        This should do any required logic, 
        then call self._request_transcription.
        It should return the job_name.
        """
        if kwargs["language_code"] not in self.language_list():
            raise KeyError(f"No such language code {kwargs['language_code']}")

    @abc.abstractmethod
    def _request_transcription(self) -> str:
        """Returns the job_name"""
        pass

    @classmethod
    def language_list(cls) -> List[str]:
        return sorted(cls._language_list)

    @classmethod
    @abc.abstractmethod
    def retrieve_transcript(cls, transcription_job_name: str) -> Union[str, dict]:
        pass

    @classmethod
    @abc.abstractmethod
    def get_transcription_jobs() -> List[dict]:
        pass
