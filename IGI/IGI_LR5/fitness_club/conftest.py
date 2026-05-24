import pytest


@pytest.fixture
def api():
    pytest.importorskip('django')
    from django.test import Client
    return Client()
