from pprint import pprint
import pytest

from tatt.vendors.google import Transcriber
from tatt import exceptions


@pytest.fixture
def audio_filepath():
    return '/Users/zev/d/saying_things_stuff.flac'


@pytest.fixture
def transcript_name():
    return 'saying_things_stuff.flac.txt'


def test_request_transcription_already_exists(audio_filepath):
    with pytest.raises(exceptions.AlreadyExistsError):
        t = Transcriber(audio_filepath)
        filename = t._request_transcription()


def test_make_bucket():
    t = Transcriber._make_bucket_if_doesnt_exist('something-uh-ok')


def test_setup():
    t = Transcriber._setup()


def test_check_if_transcript_exists(audio_filepath):
    t = Transcriber('/Users/zev/d/saying_things_stuff.flac')
    assert t._check_if_transcript_exists() is True


def test_retrieve_transcript(transcript_name):
    transcript = Transcriber.retrieve_transcript(transcript_name)
    assert transcript is not None


def test_retrieve_transcript_doesnt_exist():
    with pytest.raises(exceptions.DoesntExistError):
        Transcriber.retrieve_transcript('no_such_thing.json')


def test_get_transcription_jobs():

