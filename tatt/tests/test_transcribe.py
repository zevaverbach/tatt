from unittest import mock

from click.testing import CliRunner

from tatt.transcribe import cli
from tatt.vendors.amazon import Transcriber


def test_services():
    runner = CliRunner()
    result = runner.invoke(cli, ['services'])
    assert result.exit_code == 0
    assert 'amazon\t\t$0.006 per 15 seconds' in result.output
    assert ('Here are all the available speech-to-text-services:' 
            in result.output)


@mock.patch('tatt.transcribe.get_transcription_jobs')
def test_status(get_transcription_jobs):
    runner = CliRunner()
    result = runner.invoke(cli, ['status', 'hi'])
    assert get_transcription_jobs.called
    get_transcription_jobs.assert_called_with(name='hi')

# list, get

@mock.patch('tatt.transcribe.get_service')
def test_this(get_service):
    runner = CliRunner()
    result = runner.invoke(cli, ['this', 'hi.mp3', 'amazon'])
    get_service.assert_called_once()
    get_service.assert_called_with('amazon')


@mock.patch('tatt.transcribe.get_transcription_jobs')
def test_list(get_transcription_jobs):
    runner = CliRunner()
    result = runner.invoke(cli, ['list'])
    get_transcription_jobs.assert_called_once()
    get_transcription_jobs.assert_called_with(None, None, None)

    result = runner.invoke(cli, ['list', '-n', 'hi.mp3'])
    get_transcription_jobs.assert_called_with(None, 'hi.mp3', None)
