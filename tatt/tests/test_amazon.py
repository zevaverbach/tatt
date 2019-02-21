from unittest import mock

from tatt.vendors.amazon import Transcriber



def test_transcriber_instantiate():
    filepath = '/Users/zev/tester.mp3'
    t = Transcriber(filepath)
    assert str(t.filepath) == filepath
    assert t.basename == 'tester.mp3'
    assert t.media_file_uri == (
        f'https://s3-us-east-1.amazonaws.com/tatt-media-amazon/tester.mp3'
            )


@mock.patch('tatt.vendors.amazon.tr.get_transcription_job')
def test_transcriber_retrieve(get_transcription_job):
    filepath = '/Users/zev/tester.mp3'
    job_name = '4db6808e-a7e8-4d8d-a1b7-753ab97094dc'
    t = Transcriber.retrieve_transcript(job_name)
    get_transcription_job.assert_called_with(TranscriptionJobName=job_name)


def test_transcriber_get_transcription_jobs():
    result = Transcriber.get_transcription_jobs()
    assert result


def test_transcriber_retrieve_transcript():
    jobs = Transcriber.get_transcription_jobs()
    for j in jobs:
        if j['status'].lower() == 'completed':
            to_get = j['name']
            break
    transcript = Transcriber.retrieve_transcript(to_get)
    assert transcript == {'jobName': 'abcd.mp3', 'accountId': '416321668733', 'results': {'transcripts': [{'transcript': 'Hello there.'}], 'items': [{'start_time': '0.0', 'end_time': '0.35', 'alternatives': [{'confidence': '0.8303', 'content': 'Hello'}], 'type': 'pronunciation'}, {'start_time': '0.35', 'end_time': '0.76', 'alternatives': [{'confidence': '1.0000', 'content': 'there'}], 'type': 'pronunciation'}, {'alternatives': [{'confidence': None, 'content': '.'}], 'type': 'punctuation'}]}, 'status': 'COMPLETED'}
