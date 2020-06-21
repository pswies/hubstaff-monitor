import pytest

from monitor.api_client import APIClient


# shortcuts used for brevity of writing tests
API = 'https://api.hubstaff.com/v1'
APP_TOKEN = 'app-token-987'
AUTH_TOKEN = 'auth-token-123'


@pytest.fixture
def config():
    return {
        'Email': 'jsmith@example.com',
        'Password': 'qwe123',
        'AuthToken': '',
        'AppToken': '',
        'APIEndpoint': API,
        'OutputPath': 'output.html',
    }


@pytest.fixture
def client(config):
    return APIClient(config)


@pytest.fixture
def authorization(requests_mock, client):
    """Include this in a test to make the client authorized."""
    requests_mock.post(f'{API}/auth', json={'user': {'auth_token': 'test-auth-token'}})
    client.authorize()
