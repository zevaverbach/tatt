# Transcribe All The Things™

tatt is a CLI for creating and managing speech-to-text transcripts.

![demo](demo.gif)

## Installation

    pip install tatt

## Dependencies

1. A recording to transcribe.
2. a) An AWS account or b) a Google Cloud account with the speech-to-text API and
   Cloud Storage enabled.


## Usage

### List All Commands
    $ transcribe --help

    Usage: transcribe [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      get       Downloads and/or saves completed transcript.
      list      Lists available STT services.
      services  Lists available speech-to-text services.
      status    Check the status of a transcription job.
      this      Sends a media file to be transcribed.

### List All STT Services
    $ transcribe services

    Here are all the available speech-to-text services:

      amazon		$0.006 per 15 seconds
      google		$0.009 per 15 seconds

### Get Something Transcribed
    $ transcribe this <path_to_media_file> <service_name>

    Okay, transcribing <path_to_media_file> using <service_name>...
    Okay, job <job_name> is being transcribed.  Use "get" command to download it.

### List Transcripts
    $ transcribe list

    Service Job Name                                Status
    ------- --------                                ------
    amazon  tester.mp3                              IN_PROGRESS
    amazon  messed_up.mp4                           FAILED
    amazon  done_test.mp3                           COMPLETED
    amazon  also_done.MP3                           COMPLETED
    google  hey_there.mp3                           COMPLETED


    $ transcribe list <job_name>

    Service Job Name                                Status
    ------- --------                                ------
    amazon  <job_name>                              IN_PROGRESS


### Get A Completed Transcript
    $ transcript get <job_name> # prints to stdout

    {'accountId': '416321668733',
     'jobName': 'a1bace5e-8b08-4ce4-b08c-834a23aafcf1',
     'results': {'items': [{'alternatives': [{'confidence': '0.9774',
                                              'content': 'Hi'}],
                            'end_time': '1.5',
                            'start_time': '1.23',
                            'type': 'pronunciation'},
                           {'alternatives': [{'confidence': '0.9429',
                                              'content': 'is'}],
                            'end_time': '1.71',
                            'start_time': '1.5',
                            'type': 'pronunciation'},
                           ...

    $ transcript get -f <job_name>

    Okay, downloaded <job_name>.json


## Services Supported

  - [Amazon Transcribe](https://aws.amazon.com/transcribe/)
  - [Google Speech](https://cloud.google.com/speech-to-text/)

### Planned
  - [Watson](https://www.ibm.com/watson/services/speech-to-text/) 
  - [Kaldi](https://github.com/kaldi-asr/kaldi) [ and/or things built on it ](https://github.com/lowerquality/gentle)
  - [Speechmatics](https://www.speechmatics.com/)
  - [Mozilla's new open-source STT thing](https://github.com/mozilla/DeepSpeech)

