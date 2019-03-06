import json

import pytest

from tatt.helpers import make_json_friendly


@pytest.fixture
def json_string():
    return '''
results {\n  alternatives {\n    transcript: "Testing, this is Zev, Ivory box saying things."\n    confidence: 0.8002681732177734\n    words {\n      start_time {\n        seconds: 4\n      }\n      end_time {\n        seconds: 5\n        nanos: 500000000\n      }\n      word: "Testing,"\n      confidence: 0.8863372206687927\n    }\n    words {\n      start_time {\n        seconds: 5\n        nanos: 500000000\n      }\n      end_time {\n        seconds: 6\n        nanos: 600000000\n      }\n      word: "this"\n      confidence: 0.8322266936302185\n    }\n    words {\n      start_time {\n        seconds: 6\n        nanos: 600000000\n      }\n      end_time {\n        seconds: 6\n        nanos: 900000000\n      }\n      word: "is"\n      confidence: 0.7659578323364258\n    }\n    words {\n      start_time {\n        seconds: 6\n        nanos: 900000000\n      }\n      end_time {\n        seconds: 7\n        nanos: 300000000\n      }\n      word: "Zev,"\n      confidence: 0.9128385782241821\n    }\n    words {\n      start_time {\n        seconds: 7\n        nanos: 300000000\n      }\n      end_time {\n        seconds: 7\n        nanos: 700000000\n      }\n      word: "Ivory"\n      confidence: 0.7265068292617798\n    }\n    words {\n      start_time {\n        seconds: 7\n        nanos: 700000000\n      }\n      end_time {\n        seconds: 7\n        nanos: 900000000\n      }\n      word: "box"\n      confidence: 0.7768470644950867\n    }\n    words {\n      start_time {\n        seconds: 7\n        nanos: 900000000\n      }\n      end_time {\n        seconds: 8\n        nanos: 700000000\n      }\n      word: "saying"\n      confidence: 0.8872994780540466\n    }\n    words {\n      start_time {\n        seconds: 8\n        nanos: 700000000\n      }\n      end_time {\n        seconds: 9\n        nanos: 400000000\n      }\n      word: "things."\n      confidence: 0.9128385782241821\n    }\n  }\n  channel_tag: 1\n  language_code: "en-us"\n}\nresults {\n  alternatives {\n    transcript: " 2019"\n    confidence: 0.7211145758628845\n    words {\n      start_time {\n        seconds: 10\n        nanos: 300000000\n      }\n      end_time {\n        seconds: 11\n        nanos: 500000000\n      }\n      word: "2019"\n      confidence: 0.7581846714019775\n    }\n  }\n  channel_tag: 2\n  language_code: "en-us"\n}\n
'''

def test_make_json_friendly(json_string):
    friendly = make_json_friendly(json_string)
    print(friendly)
    assert json.loads(friendly)
