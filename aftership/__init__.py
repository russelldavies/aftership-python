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


import json

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


class Resource(object):
    """
    Generic API resource.
    """
    def __init__(self, headers=None, **kwargs):
        self.headers = headers or {}
        self.headers.update(config.headers)

        self.url = '{base_url}/{path}'.format(base_url=config.base_url, path=self.PATH.strip('/'))

    def get(self):
        r = requests.get(self.url, headers=self.headers)
        # TODO: verify is valid json
        return r.json().get('data')


class Courier(Resource):
    PATH = '/couriers'

    @classmethod
    def all(cls, headers=None):
        """
        Return a list of couriers supported by AfterShip along with their
        names, URLs and slugs.
        """
        resource = Courier(headers)
        return resource.get()

    @classmethod
    def detect(cls, tracking_number, headers=None):
        """
        Return a list of matched couriers of a tracking based on the
        tracking number format. User can limit number of matched couriers
        and change courier priority at courier settings.
        """
        resource = Courier(headers)
        resource.url += '/detect/{}'.format(tracking_number)
        return resource.get()


class Tracking(object):
    PATH = '/trackings'

    @classmethod
    def create(cls, tracking_number, headers=None, **kwargs):
        url = '{}/{}'.format(config.base_url, cls.PATH.strip('/'))
        headers = headers or {}
        headers.update(config.headers)
        payload = {
            'tracking': {
                'tracking_number': tracking_number,
            }
        }
        payload['tracking'].update(**kwargs)
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        return r.json().get('data')

    @classmethod
    def _tracking(cls, http_method, headers=None, url_suffix=None, **kwargs):
        headers = headers or {}
        headers.update(config.headers)

        if kwargs.get('tracking_number'):
            # Tracking results of a single tracking.
            try:
                url = '{}/{}/{slug}/{tracking_number}'.format(config.base_url,
                        cls.PATH.strip('/'), kwargs.pop('slug'),
                        kwargs.pop('tracking_number'))
                url = url + '/' + url_suffix if url_suffix else url
            except KeyError as e:
                e.message = "{} must be specified".format(e.args)
        else:
            # Tracking results of multiple trackings.
            url = '{}/{}'.format(config.base_url, cls.PATH.strip('/'))

        payload = {'tracking': kwargs}
        r = http_method(url, headers=headers, data=json.dumps(payload))
        return r.json().get('data')

    @classmethod
    def get(cls, headers=None, **kwargs):
        return cls._tracking(requests.get, headers, **kwargs)

    @classmethod
    def update(cls, headers=None, **kwargs):
        return cls._tracking(requests.put, headers, **kwargs)

    @classmethod
    def reactivate(cls, headers=None, **kwargs):
        return cls._tracking(requets.post, headers, url_suffix='reactivate',
                **kwargs)

    @classmethod
    def last_checkpoint(cls, tracking_number, slug, headers=None, **kwargs):
        headers = headers or {}
        headers.update(config.headers)
        url = '{}/{}/{slug}/{tracking_number}'.format(config.base_url,
                '/last_checkpoint', slug, tracking_number)
        payload = {'tracking': kwargs}
        r = requets.get(url, headers=headers, data=json.dumps(payload))
        return r.json().get('data')
