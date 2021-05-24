from datetime import datetime as date
import json
import uuid

import responses
from unittest import TestCase

from sertipy.client import Sertiva


class TestSertiva(TestCase):
    def setUp(self) -> None:
        self.sertiva = Sertiva('', '')
        self.responses = responses.RequestsMock()
        self.responses.start()

        self.responses.add(
            responses.POST, 'https://api.sertiva.id/api/v2/authorization',
            body=f'{json.dumps({"data": {"token_type": "Bearer", "expires_in": 0, "access_token": "ACCESS TOKEN"}})}',
            status=200,
            content_type='application/json')

        self.addCleanup(self.responses.stop)
        self.addCleanup(self.responses.reset)


class TestSertivaDesign(TestSertiva):
    def test_list(self):
        # given
        data = {"code": 200, "status": "success", "data": {"designs": [], "meta": {}}}
        self.responses.add(
            responses.GET, 'https://api.sertiva.id/api/v2/designs',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.sertiva.designs.list()

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(data, resp)

    def test_detail(self):
        # given
        test_id = uuid.uuid4()
        data = {"code": 200, "status": "success", "data": {}}
        self.responses.add(
            responses.GET, f'https://api.sertiva.id/api/v2/designs/{test_id}',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.sertiva.designs.detail(test_id)

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(data, resp)


class TestSertivaTemplate(TestSertiva):
    def test_list(self):
        # given
        data = {"code": 200, "status": "success", "data": {"templates": [], "meta": {}}}

        self.responses.add(
            responses.GET, 'https://api.sertiva.id/api/v2/templates',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.sertiva.templates.list()

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(data, resp)

    def test_detail(self):
        # given
        test_id = uuid.uuid4()
        data = {"code": 200, "status": "success", "data": {}}

        self.responses.add(
            responses.GET, f'https://api.sertiva.id/api/v2/templates/{test_id}',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.sertiva.templates.detail(test_id)

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(data, resp)

    def test_create(self):
        # given
        design_id = str(uuid.uuid4())
        title = "Some Title"
        description = "Some Description"
        data = {"code": 200, "status": "success",
                "data": {"design_id": design_id, "title": title, "description": description}}

        self.responses.add(
            responses.POST, 'https://api.sertiva.id/api/v2/templates',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.sertiva.templates.create(design_id, title, description)

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(data, resp)

    def test_update(self):
        # given
        template_id = str(uuid.uuid4())
        title = "Some Title"
        description = "Some Description"
        data = {"code": 200, "status": "success",
                "data": {"id": template_id, "title": title, "description": description}}

        self.responses.add(
            responses.PATCH, f'https://api.sertiva.id/api/v2/templates/{template_id}',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.sertiva.templates.update(template_id, title, description)

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(data, resp)


class TestSertivaRecipient(TestSertiva):
    def test_list(self):
        # given
        template_id = str(uuid.uuid4())
        data = {"code": 200, "status": "success", "data": {"recipients": [], "meta": {}}}
        self.responses.add(
            responses.GET, f'https://api.sertiva.id/api/v2/templates/{template_id}/recipients',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.sertiva.recipients.list(template_id)

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(data, resp)

    def test_create(self):
        # given
        template_id = str(uuid.uuid4())
        recipients = [
            {"name": "r1", "email": "r1@email.com"},
            {"name": "r2", "email": "r2@email.com"}
        ]

        data = {"code": 200, "status": "success",
                "data": {"recipients": recipients}}

        self.responses.add(
            responses.POST, f'https://api.sertiva.id/api/v2/templates/{template_id}/recipients',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.sertiva.recipients.create(template_id, recipients)

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(data, resp)

    def test_update(self):
        # given
        template_id = str(uuid.uuid4())
        recipients = [
            {"id": str(uuid.uuid4()), "phone": "08123218"},
            {"id": str(uuid.uuid4()), "phone": "02149199"}
        ]

        data = {"code": 200, "status": "success",
                "data": {"recipients": recipients}}

        self.responses.add(
            responses.PATCH, f'https://api.sertiva.id/api/v2/templates/{template_id}/recipients',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.sertiva.recipients.update(template_id, recipients)

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(data, resp)

    def test_delete(self):
        # given
        template_id = str(uuid.uuid4())
        recipient_ids = [
            str(uuid.uuid4()),
            str(uuid.uuid4())
        ]

        data = {"code": 200, "status": "success",
                "data": {"recipient_ids": recipient_ids}}

        self.responses.add(
            responses.DELETE, f'https://api.sertiva.id/api/v2/templates/{template_id}/recipients',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.sertiva.recipients.delete(template_id, recipient_ids)

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(data, resp)


class TestSertivaCredential(TestSertiva):
    def test_list(self):
        # given
        data = {"code": 200, "status": "success", "data": {"credentials": [], "meta": {}}}
        self.responses.add(
            responses.GET, 'https://api.sertiva.id/api/v2/credentials',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.sertiva.credentials.list()

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(data, resp)

    def test_detail(self):
        # given
        test_id = uuid.uuid4()
        data = {"code": 200, "status": "success", "data": {}}
        self.responses.add(
            responses.GET, f'https://api.sertiva.id/api/v2/credentials/{test_id}',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.sertiva.credentials.detail(test_id)

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(data, resp)


class TestSertivaMain(TestSertiva):
    def test_issue(self):
        # given
        template_id = str(uuid.uuid4())
        issuance_date = str(date.now())
        expiration_date = str(date.now())

        recipient_ids = [
            str(uuid.uuid4()),
            str(uuid.uuid4()),
            str(uuid.uuid4())
        ]

        recipients = [
            {"id": str(uuid.uuid4()), "name": "r1", "phone": "08123218", "fields": {}},
            {"id": str(uuid.uuid4()), "name": "r2", "phone": "02149199", "fields": {}}
        ]

        data = {"code": 200, "status": "success",
                "data": {"credentials": []}}

        self.responses.add(
            responses.POST, f'https://api.sertiva.id/api/v2/issue',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when from recipients
        resp = self.sertiva.mains.issue(template_id, issuance_date, expiration_date)

        # then from recipients
        self.assertEqual(data, resp)

        # when with recipient ids
        resp = self.sertiva.mains.issue(template_id, issuance_date, expiration_date, recipient_ids=recipient_ids)

        # then with recipient ids
        self.assertEqual(data, resp)

        # when with recipients
        resp = self.sertiva.mains.issue(template_id, issuance_date, expiration_date, recipients=recipients)

        # then with recipients
        self.assertEqual(data, resp)

        # then
        self.assertEqual(len(self.responses.calls), 3)

    def test_verify(self):
        # given
        credential_ids = [str(uuid.uuid4())]

        data = {"code": 200, "status": "success",
                "data": [{"id": x, "verification": []} for x in credential_ids]}

        self.responses.add(
            responses.POST, f'https://api.sertiva.id/api/v2/verify',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.sertiva.mains.verify(credential_ids)

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(data, resp)

    def test_revoke(self):
        # given
        reason = "Some Reason"
        credential_ids = [str(uuid.uuid4())]

        data = {"code": 200, "status": "success",
                "data": [{
                    "status": "revoked",
                    "credential": {}
                }]}

        self.responses.add(
            responses.DELETE, f'https://api.sertiva.id/api/v2/revoke',
            body=f'{json.dumps(data)}',
            status=200,
            content_type='application/json')

        # when
        resp = self.sertiva.mains.revoke(credential_ids, reason)

        # then
        self.assertEqual(len(self.responses.calls), 1)
        self.assertEqual(data, resp)
