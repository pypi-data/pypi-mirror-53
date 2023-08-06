import logging

import requests
from bs4 import BeautifulSoup

from .exceptions import DaftException


class Request:
    def __init__(self, debug=False):
        self._headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
        self._debug = debug

    def get(self, url, params=None):
        req = requests.get(url, headers=self._headers, params=params)
        if self._debug:
            logging.info("URL: " + req.url)
            logging.info("Status code: " + str(req.status_code))

        if req.status_code != 200:
            raise DaftException(reason=req.reason)

        soup = BeautifulSoup(req.content, 'html.parser')
        return soup

    def post(self, url, params=None):
        req = requests.post(url, params=params, headers=self._headers)

        if self._debug:
            logging.info("URL: " + req.url)
            logging.info("Status code: " + str(req.status_code))

        if req.status_code != 200:
            raise DaftException(reason=req.reason)

        return req
