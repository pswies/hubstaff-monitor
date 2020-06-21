import urllib.parse
from datetime import date

import pytest
import requests

from tests.conftest import API, APP_TOKEN, AUTH_TOKEN


def test_authorization_success(requests_mock, config, client):
    requests_mock.post(
        f'{API}/auth',
        json={'user': {'auth_token': 'some-token'}}
    )
    client.authorize()
    assert urllib.parse.unquote(requests_mock.last_request.text) == \
        f"email={config['Email']}&password={config['Password']}"
    assert client.auth_token == 'some-token'


def test_authorization_unauthorized(requests_mock, client):
    requests_mock.post(f'{API}/auth', status_code=401)
    with pytest.raises(requests.HTTPError):
        client.authorize()


def test_skip_authorization_when_token_provided(requests_mock, client):
    client.auth_token = 'already-provided'
    client.authorize()  # making a call would raise requests_mock.NoMockAddress


def test_get_user_names(requests_mock, client, authorization):
    requests_mock.get(
        f'{API}/users',
        json={
            'users': [
                {'id': 1, 'name': 'Mr. Smith'},
                {'id': 2, 'name': 'Mrs. Doe'},
                {'id': 3, 'name': 'Lorem'},
            ],
        },
        headers={'App-Token': APP_TOKEN, 'Auth-Token': AUTH_TOKEN},
    )
    assert client.get_user_names() == {
        1: 'Mr. Smith',
        2: 'Mrs. Doe',
        3: 'Lorem',
    }


def test_get_project_names(requests_mock, client, authorization):
    requests_mock.get(
        f'{API}/projects',
        json={
            'projects': [
                {'id': 100, 'name': 'Project X'},
                {'id': 101, 'name': 'The Hunt'},
                {'id': 102, 'name': 'Ipsum Inc.'},
            ],
        },
        headers={'App-Token': APP_TOKEN, 'Auth-Token': AUTH_TOKEN},
    )
    assert client.get_project_names() == {
        100: 'Project X',
        101: 'The Hunt',
        102: 'Ipsum Inc.',
    }


def test_get_activities(requests_mock, client, authorization):
    check_date = date(2020, 4, 19)
    response_objects = [
        {'id': 550, 'big-object': 'A'},
        {'id': 551, 'big-object': 'B'},
        {'id': 552, 'big-object': 'C'},
    ]
    requests_mock.get(
        f'{API}/activities?start_time=2020-04-19&stop_time=2020-04-20',
        json={'activities': response_objects},
        headers={'App-Token': APP_TOKEN, 'Auth-Token': AUTH_TOKEN},
    )
    assert client.get_activities(check_date) == response_objects
