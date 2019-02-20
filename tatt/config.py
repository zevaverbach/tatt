import os
from pathlib import Path
import sqlite3


STT_SERVICES = {
        'amazon': {
                'cost_per_minute': .024,
                'free': '60_minutes_per_month_for_the_first_12_months',
            },
        }


AWS_BUCKET_NAME_FMTR_MEDIA = 'tatt-media-{}'
AWS_BUCKET_NAME_FMTR_TRANSCRIPT = 'tatt-transcript-{}'
AWS_CONFIG_FILEPATH = (
    os.getenv('AWS_CONFIG_FILEPATH') 
    or Path.home() / '.aws/config'
)
AWS_REGION = 'us-east-1'

SERVICE_CLASS_NAME = 'transcribe'
