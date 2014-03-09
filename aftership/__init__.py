"""
AfterShip Python client
API docs: https://www.aftership.com/docs/api
"""

__title__ = 'aftership'
# TODO: update when done
__version__ = '0.0.1'
__author__ = 'Russell Davies'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2014 Russell Davies'


import requests

API_VERSION = '3'

class ImproperlyConfigured(Exception):
    """AfterShip client is somehow improperly configured"""
    pass


class Config(object):
    def __init__(self, api_key=None, api_version=None):
        super(Config, self).__init__()
        self.api_key = None
        self.api_version = API_VERSION
        self._base_url = 'https://api.aftership.com/v{}'
        self._headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'AfterShip/{} (Python)'.format(__version__)
        }

    @property
    def base_url(self):
        return self._base_url.format(self.api_version)

    @property
    def headers(self):
        if not self.api_key:
            raise ImproperlyConfigured("API key not set.")
        self._headers['aftership-api-key'] = self.api_key
        return self._headers

config = Config()


class Courier(object):
    PATH = '/couriers'

    @classmethod
    def all(cls, headers=None):
        """
        Return a list of couriers supported by AfterShip along with their
        names, URLs and slugs.
        """
        url = '{}{}'.format(config.base_url, cls.PATH)
        headers = headers or {}
        headers.update(config.headers)
        r = requests.get(url, headers=headers)
        # TODO: verify is valid json
        return r.json().get('data')

    @classmethod
    def detect(cls, tracking_number, headers=None):
        """
        Return a list of matched couriers of a tracking based on the
        tracking number format. User can limit number of matched couriers
        and change courier priority at courier settings.
        """
        url = '{}{}/detect/{}'.format(config.base_url, cls.PATH, tracking_number)
        headers = headers or {}
        headers.update(config.headers)
        r = requests.get(url, headers=headers)
        # TODO: error handling
        return r.json().get('data')


class Tracking(object):
    PATH = '/trackings'
