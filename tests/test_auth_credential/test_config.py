"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
import os
import unittest
from unittest import (
    mock,
)

from minos.auth_credential import (
    CredentialConfig,
    CredentialConfigException,
)
from tests.utils import (
    BASE_PATH,
)


class TestApiGatewayConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.config_file_path = BASE_PATH / "config.yml"

    def test_config_ini_fail(self):
        with self.assertRaises(CredentialConfigException):
            CredentialConfig(path=BASE_PATH / "test_fail_config.yaml")

    def test_config_rest(self):
        config = CredentialConfig(path=self.config_file_path)
        rest = config.rest

        self.assertEqual("localhost", rest.host)
        self.assertEqual(5568, rest.port)

    @mock.patch.dict(os.environ, {"AUTH_CREDENTIAL_REST_HOST": "::1"})
    def test_overwrite_with_environment_rest_host(self):
        config = CredentialConfig(path=self.config_file_path)
        self.assertEqual("::1", config.rest.host)

    @mock.patch.dict(os.environ, {"AUTH_CREDENTIAL_REST_PORT": "4040"})
    def test_overwrite_with_environment_rest_port(self):
        config = CredentialConfig(path=self.config_file_path)
        self.assertEqual(4040, config.rest.port)



if __name__ == "__main__":
    unittest.main()
