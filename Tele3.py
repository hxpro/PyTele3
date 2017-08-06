import requests
from typing import List
from xmltodict import parse, unparse


class Domain:
    def __init__(self, data: dict):
        self.name = data['#text']
        self.expiration = data['@expire']

    def __str__(self):
        return self.name


class Contact:
    def __init__(self, data: dict):
        self.contact_id = data['contact_id']
        self.contact_type = data['contact_type']
        self.name = data['name']
        self.organisation = data['organisation']
        self.editable = bool(data['editable'] == 'yes')
        self.deletable = bool(data['deletable'] == 'yes')

    def __str__(self):
        return self.name


class Usage:
    def __init__(self, data: dict):
        self.quota = int(data['quota'])
        self.used = int(data['used'])
        self.remaining = int(data['remaining'])

    def __str__(self):
        return f"{self.used}/{self.quota}"

    def __float__(self):
        return self.used / self.quota


class APIException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class API:

    def __init__(self):
        self.ssid = None

    def _api_call(self, api_function: str, params=None):
        url = 'https://www.tele3.cz/api/'
        if api_function == 'login':
            self.ssid = None
        if not self.ssid and api_function != 'login':
            raise APIException('Unknown ssid, use API.login() first')
        payload = unparse({'api': {'ssid': self.ssid, api_function: params}})
        req_response = requests.post(url, payload)
        response = parse(req_response.text)['api']

        try:
            self.last_status_code = response['status']['@code']
            self.last_status_text = response['status']['#text']
        except:
            raise APIException('Cannot get status code from response')

        try:
            self.credit_currency = response['credit']['@currency']
            self.credit = response['credit']['#text']
        except:
            raise APIException(self.last_status_text)

        return response

    def _expect_status(self, expected_status: List[str]):
        if self.last_status_code not in expected_status:
            raise APIException(self.last_status_text)

    def login(self, user: str, password: str):
        response = self._api_call('login', params={'user': user, 'password': password})
        self._expect_status(['1000'])
        self.ssid = response['ssid']

    def logout(self):
        self._api_call('logout')
        self._expect_status(['1000'])
        self.ssid = None

    def usage(self) -> Usage:
        response = self._api_call('get_usage')
        self._expect_status(['1000'])
        return Usage(response)

    def domains(self) -> List[Domain]:
        response = self._api_call('list_domains')
        self._expect_status(['1000'])
        r = []
        for d in response['list_domains']['domain']:
            r.append(Domain(d))
        return r

    def contacts(self) -> List[Contact]:
        response = self._api_call('list_contacts')
        self._expect_status(['1000'])
        if self.last_status_code != '1000':
            raise APIException(self.last_status_text)
        r = []
        for c in response['list_contacts']['contact']:
            r.append(Contact(c))
        return r

    def import_contact(self, contact_id: str):
        self._api_call('import_contact', params=contact_id)
        self._expect_status(['1000'])
