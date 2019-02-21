from tatt.vendors import SERVICES


def test_services():
    for service in SERVICES.values():
        assert hasattr(service, 'Transcriber')
        assert hasattr(service, 'NAME')
        assert hasattr(service, 'cost_per_15_seconds')
