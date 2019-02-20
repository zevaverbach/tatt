import os
from pathlib import Path
import sqlite3


AWS_BUCKET_NAME_FMTR_MEDIA = 'tatt-media-{}'
AWS_BUCKET_NAME_FMTR_TRANSCRIPT = 'tatt-transcript-{}'

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
