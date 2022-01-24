"""tests.test_api_gateway.test_rest.service module."""

import json
import unittest

import aiohttp
from aiohttp.test_utils import (
    AioHTTPTestCase,
)

from minos.auth_credential import (
    CredentialConfig,
    CredentialRestService,
)
from tests.utils import (
    BASE_PATH,
)


class TestCredentialRestService(AioHTTPTestCase):
    CONFIG_FILE_PATH = BASE_PATH / "config.yml"

    def setUp(self) -> None:
        self.config = CredentialConfig(self.CONFIG_FILE_PATH)
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        rest_service = CredentialRestService(
            address=self.config.rest.host, port=self.config.rest.port, config=self.config
        )

        return await rest_service.create_application()

    async def test_create_credential(self):
        url = "/credentials"
        response = await self.client.request(
            "POST", url, data=json.dumps({"username": "test_user_1", "password": "HelloTestUser"})
        )

        self.assertEqual(200, response.status)
        self.assertIn("credential_uuid", await response.text())

    async def test_create_credential_existing_user(self):
        url = "/credentials"
        response = await self.client.request(
            "POST", url, data=json.dumps({"username": "test_user_1", "password": "HelloTestUser"})
        )

        self.assertEqual(400, response.status)
        self.assertDictEqual({"error": "Username is already taken."}, json.loads(await response.text()))

    async def test_create_credential_uncomplete_parameters(self):
        url = "/credentials"
        response = await self.client.request("POST", url)

        self.assertEqual(400, response.status)
        self.assertDictEqual({"error": "Wrong data. Provide username and password."}, json.loads(await response.text()))

    async def test_validate_credential(self):
        url = "/credentials/validate"

        headers = {"Authorization": aiohttp.BasicAuth("test_user_1", "HelloTestUser").encode()}
        response = await self.client.request(
            "POST", url, headers=headers, data=json.dumps({"username": "test_user_1", "password": "HelloTestUser"})
        )

        self.assertEqual(200, response.status)
        self.assertIn("credential_uuid", await response.text())


if __name__ == "__main__":
    unittest.main()
