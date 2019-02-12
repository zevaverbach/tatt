# Transcribe All The Things™

Tatt creates a uniform API for multiple speech-to-text (STT) services.

## Installation

    `pip install git+https://github.com/zevaverbach/tatt`


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

  - Amazon Transcribe

### Planned
  - Watson 
  - Google Speech
  - Kaldi and/or things built on it
  - Speechmatics
  - Mozilla's new open-source STT thing

