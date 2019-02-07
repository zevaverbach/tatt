import os

from tatt.vendors import (
        amazon,
        )


STT_SERVICES = {
        'amazon': {
                'cost_per_minute': .024,
                'free': '60_minutes_per_month_for_the_first_12_months',
                'function': amazon.transcribe,
            },
        }


DEFAULT_BUCKET_NAME_FORMATTER = 'tatt_{}'
AWS_CREDENTIALS_FILEPATH = os.getenv('AWS_CREDENTIALS_FILEPATH') or '~/.aws/credentials'
