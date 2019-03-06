from tatt.vendors.google import Transcriber


def test_request_transcription():
    t = Transcriber('/Users/zev/d/saying_things_stuff.flac')
    t._request_transcription()
