__all__ = ['SertivaAuth']

import errno
import json
import logging
import requests

from sertipy.exceptions import SertipyException

logger = logging.getLogger(__name__)


class CacheHandler:
    def __init__(self, cache_path=None):
        self.cached_token_info = None

        if cache_path:
            self.cached_token_path = cache_path
        else:
            cache_path = '.cache'
            self.cached_token_path = cache_path

    def get_cached_token(self) -> str:
        """
        Get and return a token dictionary object from the cached file.
        """
        logger.info('[SERTIPY] Get access token from cache')
        token_info = self.cached_token_info

        if token_info:
            return token_info

        try:
            f = open(self.cached_token_path)
            token_string = f.read()
            f.close()

            if not token_string:
                return token_info

            token_info = json.loads(token_string)
            self.cached_token_info = token_info
        except IOError as error:
            if error.errno == errno.ENOENT:
                logger.debug('[SERTIPY] cached file or directory does not exists')
            else:
                logger.warning(f'[SERTIPY] could not read cached file at {self.cached_token_path}')

        return token_info

    def saved_token_to_cache(self, token_info: str) -> None:
        """
        Save a token dictionary object to the cache and return None.
        """

        logger.info('[SERTIPY] Saving access token to cache')

        try:
            # saving token to path
            f = open(self.cached_token_path, "w")
            f.write(json.dumps(token_info))
            f.close()

            # saving cache to instance variable
            self.cached_token_info = token_info
        except IOError:
            logger.warning(f"[SERTIPY] Could not write token to cache at {self.cached_token_path}")


class SertivaAuth:
    """
    client_id, client_secret from sertiva
    """

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_cache = CacheHandler()

    def get_token(self):
        # get token from cache
        access_token = self.auth_cache.get_cached_token()

        if access_token:
            return access_token

        # request token
        access_token = self.__get_access_token()

        # saving to cache
        self.auth_cache.saved_token_to_cache(access_token['data']['access_token'])

        return self.auth_cache.get_cached_token()

    def __get_access_token(self):
        logger.info('[SERTIPY] Request access token to Sertiva')
        url = 'https://api.sertiva.id/api/v2/authorization'
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "issue verify revoke"
        }
        logger.debug('[SERTIPY] Sending POST request token to Sertiva Authorization')

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            results = response.json()
        except requests.exceptions.HTTPError as http_error:
            response = http_error.response
            logger.error('[SERTIPY] Failed to request access token')

            raise SertipyException(
                response.status_code,
                "%s:\n %s" % (response.url, response.json()['message']),
                reason=response.reason,)

        logger.info('[SERTIPY] Success to request access token')

        return results
