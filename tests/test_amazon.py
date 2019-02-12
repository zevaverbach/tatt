from tatt.vendors.amazon import transcribe, retrieve_transcript



def test_transcribe_instantiate():
    filepath = '/Users/zev/tester.mp3'
    t = transcribe(filepath)
    assert str(t.filepath) == filepath
    assert t.basename == 'tester.mp3'
    assert t.media_file_uri == (
        f'https://s3-us-east-1.amazonaws.com/tatt-media-amazon/tester.mp3'
            )


def test_retrieve():
    filepath = '/Users/zev/tester.mp3'
    t = retrieve_transcript('4db6808e-a7e8-4d8d-a1b7-753ab97094dc')
    print(t)
    assert t is not None
