from .vendor import TranscriberBaseClass


class Transcriber(TranscriberBaseClass):

    no_config_error_message = (
            'Please sign up for the Google Speech-to-Text API, get credentials, '
            'and put the path to your credentials (private key) in an '
            'environment variable "GOOGLE_STT_PRIVATE_KEY_PATH"'
            )

    def __init__(self, filepath):
        super().__init__(filepath)

    @classmethod
    def _setup(cls):
        if not cls.check_for_config():
            raise exceptions.ConfigError(cls.no_config_error_message)

    @staticmethod
    @abc.abstractmethod
    def check_for_config() -> bool:
        os.getenv('GOOGLE_STT_PRIVATE_KEY_PATH') is not None

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
    def get_transcription_jobs():
        pass

