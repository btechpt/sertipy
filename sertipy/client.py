__all__ = ['Sertiva']

import logging
import requests

from typing import List, Dict

from sertipy.auth import SertivaAuth
from sertipy.exceptions import SertipyException

logger = logging.getLogger(__name__)


class SertivaBaseRequest:
    def __init__(self, auth):
        self.prefix = 'https://api.sertiva.id/api/v2/'
        self.auth = auth

    def _auth_headers(self) -> Dict[str, str]:
        return {"Authorization": "Bearer {0}".format(self.auth.get_token())}

    def _internal_call(self, method: str, url: str, **kwargs) -> Dict[str, any]:
        allowed_methods = {
            'GET': requests.get,
            'POST': requests.post,
            'PATCH': requests.patch,
            'DELETE': requests.delete
        }
        payload = kwargs.get("payload", None)

        try:
            if kwargs.get("number_of_page", None):
                response = allowed_methods[method](self.prefix + url, headers=self._auth_headers(),
                                                   params={'page': str(kwargs.get("number_of_page", None))}, json=payload)
            else:
                response = allowed_methods[method](self.prefix + url, headers=self._auth_headers(), json=payload)

            response.raise_for_status()
            results = response.json()

        except requests.exceptions.HTTPError as http_error:
            response = http_error.response
            logger.error(f'[SERTIPY] Failed to request {url}')

            raise SertipyException(
                response.status_code,
                "%s:\n %s" % (response.url, response.json()['message']),
                reason=response.reason, )

        logger.info('[SERTIPY] Success to request internal API Sertiva')

        return results


class SertivaDesign(SertivaBaseRequest):
    def list(self, number_of_page: int = 1):
        """ To get list design certificate"""
        logger.debug('[SERTIPY] Sending GET request list designs to Sertiva')
        return self._internal_call('GET', 'designs', **{"number_of_page": number_of_page})

    def detail(self, design_id: str):
        """ To get detail design certificate
        :param design_id: design_id
        """
        logger.debug('[SERTIPY] Sending GET request detail design to Sertiva')
        return self._internal_call('GET', f'designs/{design_id}')


class SertivaTemplate(SertivaBaseRequest):
    def list(self, number_of_page: int = 1):
        """ To get list templates"""
        logger.debug('[SERTIPY] Sending GET request list templates to Sertiva')
        return self._internal_call('GET', 'templates', **{"number_of_page": number_of_page})

    def detail(self, template_id: str):
        """ To get detail template certificate
        :param template_id: id form template
        """
        logger.debug('[SERTIPY] Sending GET request detail template to Sertiva')
        return self._internal_call('GET', f'templates/{template_id}')

    def create(self, design_id: str, title: str, description: str):
        """ To create new templates
        :param design_id: id from design
        :param title: title template
        :param description: description from template
        """
        payload = {
            "design_id": design_id,
            "title": title,
            "description": description
        }
        logger.debug('[SERTIPY] Sending POST request create template to Sertiva')
        return self._internal_call('POST', 'templates', **{"payload": payload})

    def update(self, template_id: str, title: str, description: str):
        """ To edit templates
        :param template_id: id form template
        :param title: title template
        :param description: description from template
        """
        payload = {
            "title": title,
            "description": description
        }
        logger.debug('[SERTIPY] Sending PATCH request update template to Sertiva')
        return self._internal_call('PATCH', f'templates/{template_id}', **{"payload": payload})


class SertivaRecipient(SertivaBaseRequest):
    def list(self, template_id: str, number_of_page: int = 1):
        """ To get list recipients"""
        logger.debug('[SERTIPY] Sending GET request List Draft Recipient to Sertiva')
        return self._internal_call('GET', f'templates/{template_id}/recipients', **{"number_of_page": number_of_page})

    def create(self, template_id: str, recipient_data: List[dict]):
        """ To get create new draft recipients
        :param template_id: id form template
        :param recipient_data: data recipient (contain recipient_id)
        """
        payload = {
            'recipients': recipient_data
        }
        logger.debug('[SERTIPY] Sending POST request Create Draft Recipient to Sertiva')
        return self._internal_call('POST', f'templates/{template_id}/recipients', **{"payload": payload})

    def update(self, template_id: str, recipient_data: List[dict]):
        """ To update recipients
        :param recipient_data: data recipient (contain recipient_id)
        :param template_id: id from sertiva
        """
        payload = {
            'recipients': recipient_data
        }
        logger.debug('[SERTIPY] Sending PATCH request Update Draft Recipient to Sertiva')
        return self._internal_call('PATCH', f'templates/{template_id}/recipients', **{"payload": payload})

    def delete(self, template_id: str, recipient_ids: List[str]):
        """ To delete recipients
        :param template_id: id form template
        :param recipient_ids: list id recipient
        """
        payload = {
            'recipient_ids': recipient_ids
        }
        logger.debug('[SERTIPY] Sending DELETE request Delete Draft Recipient to Sertiva')
        return self._internal_call('DELETE', f'templates/{template_id}/recipients', **{"payload": payload})


class SertivaCredential(SertivaBaseRequest):
    def list(self, number_of_page: int = 1):
        """ To get list credentials"""
        logger.debug('[SERTIPY] Sending GET request list credentials to Sertiva')
        return self._internal_call('GET', 'credentials', **{"number_of_page": number_of_page})

    def detail(self, credential_id: str):
        """ To get detail credential
        :parameter credential_id: id credential(certificate) from Sertiva
        """
        logger.debug('[SERTIPY] Sending GET request detail credential to Sertiva')
        return self._internal_call('GET', f'credentials/{credential_id}')


class SertivaMain(SertivaBaseRequest):
    def issue(self, template_id: str, issuance_date: str,
              expiration_date: str, recipient_ids: List[str] = None, recipients: List[dict] = None):
        """ To issue new credential/certificate
        when param recipients None and recipient ids None.
        it means, issue new credential will all data recipients draft in the template
        :param template_id: id template form Sertiva
        :param issuance_date: Credential/Certificate issuance date
        :param expiration_date: Credential/Certificate expiration date

        :param recipient_ids: list ids recipient -> issue new credential with list ids recipient
        :param recipients: list data recipient -> issue new credential with directly data recipients
        """
        payload = {
            'template_id': template_id,
            'issuance_date': issuance_date,
            'expiration_date': expiration_date
        }

        if recipient_ids:
            payload['recipient_ids'] = recipient_ids
            logger.debug('[SERTIPY] Sending POST request issue new credential to Sertiva '
                         'with ids recipient')
            return self._internal_call('POST', 'issue', **{"payload": payload})

        if recipients:
            payload['recipients'] = recipients
            logger.debug('[SERTIPY] Sending POST request issue new credential to Sertiva '
                         'with directly data recipients')
            return self._internal_call('POST', 'issue', **{"payload": payload})

        logger.debug('[SERTIPY] Sending POST request issue new credential to Sertiva '
                     'with all draft recipients in the template')
        return self._internal_call('POST', 'issue', **{"payload": payload})

    def verify(self, credential_ids: List[str]):
        """ To verify validation credential/certificate
        :parameter credential_ids: list credential id from Sertiva
        """
        payload = {
            "credential_ids": credential_ids
        }
        logger.debug('[SERTIPY] Sending POST request verify validation credential to Sertiva')
        return self._internal_call('POST', 'verify', **{"payload": payload})

    def revoke(self, credential_ids: List[str], reason: str):
        """ To revoke credential/certificate
        :parameter credential_ids: list credential id from Sertiva
        :parameter reason: reason revoke credential/certificate
        """
        payload = {
            'reason': reason,
            'credential_ids': credential_ids
        }
        logger.debug('[SERTIPY] Sending DELETE request revoke credential to Sertiva')
        return self._internal_call('DELETE', 'revoke', **{"payload": payload})


class Sertiva:
    def __init__(self, client_id: str, client_secret: str):
        self.auth = SertivaAuth(client_id, client_secret)
        self.designs = SertivaDesign(self.auth)
        self.templates = SertivaTemplate(self.auth)
        self.recipients = SertivaRecipient(self.auth)
        self.credentials = SertivaCredential(self.auth)
        self.mains = SertivaMain(self.auth)
