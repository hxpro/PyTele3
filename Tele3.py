import requests
from typing import List, Dict
from collections import OrderedDict
from xmltodict import parse, unparse


class APIException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class API:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.ssid = None
        self.contacts_list = []
        self.contacts_info = {}
        self.domains_list = []
        self.domains_info = {}

    def _api_call(self, api_function: str, params=None):
        url = 'https://www.tele3.cz/api/'
        if api_function == 'login':
            self.ssid = None
        if not self.ssid and api_function != 'login':
            raise APIException('Unknown SSID, use API.login() first')
        payload = unparse({'api': {'ssid': self.ssid, api_function: params}})
        if self.debug:
            print('\033[92m' + payload + '\033[0m')
        req_response = requests.post(url, payload)
        response = parse(req_response.text)['api']
        if self.debug:
            print('\033[95m' + req_response.text + '\033[0m')
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
        self.contacts_list = []
        self.domains_list = []

    def usage(self) -> OrderedDict:
        response = self._api_call('get_usage')
        self._expect_status(['1000'])
        response.pop('status')
        response.pop('credit')
        return response

    def domains(self, update: bool = False) -> List[OrderedDict]:
        if (not self.domains_list) or (self.domains_list and update):
            response = self._api_call('list_domains')
            self._expect_status(['1000'])
            self.domains_list = response['list_domains']['domain']
            for d in self.domains_list:
                d['name'] = d.pop('#text')
                d['expire'] = d.pop('@expire')
        return self.domains_list

    def contacts(self, update: bool = False) -> List[OrderedDict]:
        if not self.contacts_list or update:
            response = self._api_call('list_contacts')
            self._expect_status(['1000'])
            self.contacts_list = response['list_contacts']['contact']
        return self.contacts_list

    def contact(self, contact_id: str, update: bool = False) -> Dict:
        if contact_id not in self.contacts_info.keys() or update:
            response = self._api_call('info_contact', contact_id)
            self._expect_status(['1000'])
            contact = dict(response.get('info_contact'))
            contact['contact_id'] = contact.pop('contact')
            self.contacts_info[contact_id] = contact
        return self.contacts_info[contact_id]

    def domain(self, domain_name: str, update: bool = False) -> Dict:
        if domain_name not in self.domains_info.keys() or update:
            response = self._api_call('info_domain', domain_name)
            self._expect_status(['1000'])
            domain = dict(response.get('info_domain'))
            self.domains_info[domain_name] = domain
        return self.domains_info[domain_name]

    def import_contact(self, contact_id: str):
        self._api_call('import_contact', params=contact_id)
        self._expect_status(['1000'])

    def renew(self, domain: str, period: int):
        self._api_call('renew_domain', params={'domain': domain, 'period': period})
        self._expect_status(['1000'])
