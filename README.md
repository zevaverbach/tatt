# Transcribe All The Things™

Tatt creates a uniform API for multiple speech-to-text (STT) services.

## Installation

    pip install tatt


## Dependencies

An AWS account (the only supported STT provider as of Feb 12, 2019), and a recording to transcribe!


## Usage

### List All Commands
    transcribe --help

### List All STT Services
    transcribe services

### Get Something Transcribed
    transcribe this <path_to_media_file> <service_name>

### List Transcripts
    transcribe list # a full list of all transcripts, completed and in_progress
    transcribe list <transcript_basename> # the status of a particular transcript

### Get A Completed Transcript
    transcript get <transcript_basename> # prints to stdout
    transcript get -f <transcript_basename> # saves to a file in the format <basename>.json


## Services Supported

  - [Amazon Transcribe](https://aws.amazon.com/transcribe/)

### Planned
  - [Watson](https://www.ibm.com/watson/services/speech-to-text/) 
  - [Google Speech](https://cloud.google.com/speech-to-text/)
  - [Kaldi](https://github.com/kaldi-asr/kaldi) [ and/or things built on it ](https://github.com/lowerquality/gentle)
  - [Speechmatics](https://www.speechmatics.com/)
  - [Mozilla's new open-source STT thing](https://github.com/mozilla/DeepSpeech)

