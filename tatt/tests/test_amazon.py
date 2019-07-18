from unittest import mock
from pytest import raises, fixture

from tatt.vendors.amazon import Transcriber


@fixture
def media_filepath():
    return "/Users/zev/tester.mp3"


@fixture
def transcriber_instance(media_filepath):
    return Transcriber(media_filepath)


def test_transcriber_instance(media_filepath, transcriber_instance):
    assert str(transcriber_instance.filepath) == media_filepath
    assert transcriber_instance.basename == "tester.mp3"
    assert transcriber_instance.media_file_uri == (
        f"https://s3-us-east-1.amazonaws.com/tatt-media-amazon/tester.mp3"
    )


@mock.patch("tatt.vendors.amazon.tr.get_transcription_job")
def test_transcriber_retrieve(get_transcription_job):
    job_name = "4db6808e-a7e8-4d8d-a1b7-753ab97094dc"
    t = Transcriber.retrieve_transcript(job_name)
    get_transcription_job.assert_called_with(TranscriptionJobName=job_name)


def test_transcriber_get_transcription_jobs():
    result = Transcriber.get_transcription_jobs()
    assert result


def test_transcriber_retrieve_transcript():
    jobs = Transcriber.get_transcription_jobs()
    assert jobs
    for j in jobs:
        if j["status"].lower() == "completed":
            to_get = j["name"]
            break
    transcript = Transcriber.retrieve_transcript(to_get)
    assert transcript == {
        "jobName": "abcd.mp3",
        "accountId": "416321668733",
        "results": {
            "transcripts": [{"transcript": "Hello there."}],
            "items": [
                {
                    "start_time": "0.0",
                    "end_time": "0.35",
                    "alternatives": [{"confidence": "0.8303", "content": "Hello"}],
                    "type": "pronunciation",
                },
                {
                    "start_time": "0.35",
                    "end_time": "0.76",
                    "alternatives": [{"confidence": "1.0000", "content": "there"}],
                    "type": "pronunciation",
                },
                {
                    "alternatives": [{"confidence": None, "content": "."}],
                    "type": "punctuation",
                },
            ],
        },
        "status": "COMPLETED",
    }


def test_transcribe_with_nonexistent_language_code(transcriber_instance):
    with raises(KeyError):
        transcriber_instance.transcribe(language_code="pretend-lang")
