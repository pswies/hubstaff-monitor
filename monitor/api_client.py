import configparser
from datetime import date, timedelta
from typing import Dict, List

import requests


class APIClient:
    """A simple client for accessing Hubstaff v1 API."""

    def __init__(self, config: dict):
        self.app_token = config['AppToken']
        self.email = config['Email']
        self.password = config['Password']
        self.endpoint = config['APIEndpoint']
        self.auth_token = config['AuthToken']

    def authorize(self) -> None:
        if self.auth_token:  # authenticate only if necessary
            return

        payload = {
            'email': self.email,
            'password': self.password,
        }
        res = self._call('post', 'auth', payload=payload)
        self.auth_token = res['user']['auth_token']

    def get_user_names(self) -> Dict[int, str]:  # id -> name
        res = self._call('get', 'users')
        return {user['id']: user['name'] for user in res['users']}

    def get_project_names(self) -> Dict[int, str]:  # id -> name
        res = self._call('get', 'projects')
        return {user['id']: user['name'] for user in res['projects']}

    def get_activities(self, check_date: date) -> List[dict]:
        params = {
            'start_time': check_date.isoformat(),
            'stop_time': (check_date + timedelta(days=1)).isoformat(),
        }
        res = self._call('get', 'activities', params=params)
        return res['activities']

    def _call(self, method: str, path: str, params: dict = None, payload: dict = None) -> dict:
        # Future TODO: improve control over authorization; currently, if the
        # client is authorized, it is impossible to re-authorize.
        action = getattr(requests, method)
        url = f'{self.endpoint}/{path}'
 
        headers = {'App-Token': self.app_token}
        if self.auth_token:
            headers['Auth-Token'] = self.auth_token
 
        res = action(url, headers=headers, params=params, data=payload)
        res.raise_for_status()
 
        return res.json()
