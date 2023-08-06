import sys
import requests
import logging

from requests import HTTPError

log = logging.getLogger(sys.modules[__name__].__name__)


class ConfigFetcher:
    def __init__(self,
                 api_key,
                 base_url):
        self._api_key = api_key
        self._session = requests.Session()
        self._headers = {'X-ConfigCat-UserAgent': 'ConfigCat-CircleCI',
                         'Content-Type': "application/json"}
        self._base_url = base_url.rstrip('/')

    def get_flag_keys(self):
        log.info("Fetching the current ConfigCat configuration from %s.", self._base_url)
        uri = 'https://' + self._base_url + '/configuration-files/' + self._api_key + '/config_v2.json'
        try:
            response = self._session.get(uri, headers={'X-ConfigCat-UserAgent': 'ConfigCat-CircleCI',
                                                       'Content-Type': "application/json"}, timeout=(10, 30))
            response.raise_for_status()
            json = response.json()
            keys = []
            for key, value in json.items():
                keys.append(key)

            log.info("Successful fetch, %s settings found: %s.", len(keys), keys)
            return keys
        except HTTPError as err:
            log.error("HTTP error recieved: %s.", str(err.response))
            return []
        except:
            log.exception(sys.exc_info()[0])
            return []

    def close(self):
        if self._session:
            self._session.close()
