import datetime
import json
from typing import List, Dict, Union

import dateutil.parser
import requests
from requests import Response


class BotmanApi:
    def __init__(self, base_url: str, token: str, cert=False, timeout: int = 5):
        self.base_url = base_url + "{path}"
        self.token = token
        self.last_response = None
        self.cert = cert
        self.timeout = timeout

    def _headers(self) -> dict:
        return {"X-API-KEY": self.token}

    def _parse_response(self, response: Response):
        if "application/json" in response.headers.get('content-type', "") and response.content:
            content = json.loads(response.content.decode('utf-8'))
            return content
        else:
            return {}

    def _post(self, endpoint: str, data: dict = None) -> Union[dict, bool]:
        try:
            response = requests.post(endpoint, json=data, headers=self._headers(), verify=self.cert, timeout=self.timeout)
            self.last_response = response
            result = self._parse_response(response)
            return result
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return {}

    def _get(self, endpoint: str, params: dict = None) -> dict:
        try:
            response = requests.get(endpoint, params=params, headers=self._headers(), verify=self.cert, timeout=self.timeout)
            self.last_response = response
            result = self._parse_response(response)
            return result
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return {}

    def get_bot_status(self) -> bool:
        endpoint = self.base_url.format(path='bot/status')
        content = self._get(endpoint)
        if content.get('success', False):
            return content['data']['status']
        else:
            return False

    def get_api_status(self) -> bool:
        endpoint = self.base_url.format(path='status')
        content = self._get(endpoint)
        if content.get('success', False):
            return content['data']['status']
        else:
            return False

    def start_bot(self) -> bool:
        endpoint = self.base_url.format(path='bot/start')
        content = self._post(endpoint)
        return content.get('success', False)

    def stop_bot(self) -> bool:
        endpoint = self.base_url.format(path='bot/stop')
        content = self._post(endpoint)
        return content.get('success', False)

    def restart_bot(self) -> bool:
        endpoint = self.base_url.format(path='bot/restart')
        content = self._post(endpoint)
        return content.get('success', False)

    def uptime(self) -> Union[datetime.timedelta, bool]:
        endpoint = self.base_url.format(path='bot/uptime')
        content = self._get(endpoint)
        if content.get('success', False):
            return datetime.timedelta(seconds=content['data']['uptime'])
        else:
            return False

    def start_date(self) -> Union[datetime.datetime, bool]:
        endpoint = self.base_url.format(path='bot/start-date')
        content = self._get(endpoint)
        if content.get('success', False):
            if content['data']['start_date'] is None:
                return None
            return dateutil.parser.parse(content['data']['start_date'])
        else:
            return False

    def get_data(self, table: str, columns: List[str] = None, limit: int = 300, offset: int = 0, ordering: int = 1) -> Union[List[Dict], bool]:
        endpoint = self.base_url.format(path='bot/data/{table}'.format(table=table))

        params = {
            "columns": ", ".join(columns) if columns else None,
            "limit": limit,
            "offset": offset,
            "ordering": ordering
        }
        content = self._get(endpoint, params=params)
        if content.get('success', False):
            return content['data']
        else:
            return False

    def get_specific_data(self, table: str, data_id: Union[int, str], columns: List[str] = None) -> Union[dict, bool]:
        endpoint = self.base_url.format(path='bot/data/{table}/{data_id}'.format(table=table, data_id=data_id))

        params = {
            "columns": ", ".join(columns) if columns else None,
        }
        content = self._get(endpoint, params=params)
        if content.get('success', False):
            return content['data']
        else:
            return False

    def count_data(self, table: str) -> int:
        endpoint = self.base_url.format(path='bot/data/{table}/count'.format(table=table))

        content = self._get(endpoint, params={})
        if content.get('success', False):
            return content['data']
        else:
            return False

    def distribution(self, text: str, when: datetime.datetime = None, web_preview: bool = True, notification: bool = True) -> bool:
        endpoint = self.base_url.format(path='bot/distribution')
        data = {
            "text": text,
            "web_preview": web_preview,
            "notification": notification
        }
        if when:
            data.update(when=when.isoformat())

        content = self._post(endpoint, data=data)
        return content.get('success', False)

    def send_message(self, chat_id: Union[int, str], text: str) -> bool:
        endpoint = self.base_url.format(path='bot/messages/send')
        data = {
            "chat_id": chat_id,
            "text": text,
        }

        content = self._post(endpoint, data=data)
        return content.get('success', False)

    def get_users(self, limit: int = 300, offset: int = 0, ordering: int = 1) -> Union[List[Dict], bool]:
        endpoint = self.base_url.format(path='bot/users')

        params = {
            "limit": limit,
            "offset": offset,
            "ordering": ordering
        }
        content = self._get(endpoint, params=params)
        if content.get('success', False):
            return content['data']
        else:
            return False

    def get_user(self, user_id: Union[int, str]) -> Union[dict, bool]:
        endpoint = self.base_url.format(path='bot/users/{user_id}'.format(user_id=user_id))

        content = self._get(endpoint, params={})
        if content.get('success', False):
            return content['data']
        else:
            return False

    def get_stats(self) -> Union[Dict, bool]:
        endpoint = self.base_url.format(path='bot/stats')

        content = self._get(endpoint, params={})
        if content.get('success', False):
            return content['data']
        else:
            return False
