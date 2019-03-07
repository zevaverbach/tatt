import os
from pathlib import Path
import sqlite3


BUCKET_NAME_FMTR_MEDIA = 'tatt-media-{}'
BUCKET_NAME_FMTR_TRANSCRIPT = 'tatt-transcript-{}'
BUCKET_NAME_FMTR_TRANSCRIPT_GOOGLE = 'tatt_transcript_{}'


def GOOGLE_SPEECH_USE_ENHANCED():
    enhanced = os.getenv('GOOGLE_SPEECH_USE_ENHANCED')
    if enhanced and enhanced == 'true':
        return True
    else:
        return False


if os.getenv('AWS_CONFIG_FILEPATH'):
    AWS_CONFIG_FILEPATH = Path(os.getenv('AWS_CONFIG_FILEPATH'))
else:
    AWS_CONFIG_FILEPATH = Path.home() / '.aws/config'

if os.getenv('AWS_CREDENTIALS_FILEPATH'):
    AWS_CREDENTIALS_FILEPATH = Path(os.getenv('AWS_CREDENTIALS_FILEPATH'))
else:
    AWS_CREDENTIALS_FILEPATH = Path.home() / '.aws/credentials'

AWS_REGION = 'us-east-1'

SERVICE_CLASS_NAME = 'Transcriber'
