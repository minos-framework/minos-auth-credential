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

    def test_config_database(self):
        config = CredentialConfig(path=self.config_file_path)
        database = config.database

        self.assertEqual("credential_db", database.database)
        self.assertEqual("minos", database.user)
        self.assertEqual("min0s", database.password)
        self.assertEqual("localhost", database.host)
        self.assertEqual(5432, database.port)

    @mock.patch.dict(os.environ, {"AUTH_CREDENTIAL_REST_HOST": "::1"})
    def test_overwrite_with_environment_rest_host(self):
        config = CredentialConfig(path=self.config_file_path)
        self.assertEqual("::1", config.rest.host)

    @mock.patch.dict(os.environ, {"AUTH_CREDENTIAL_REST_PORT": "4040"})
    def test_overwrite_with_environment_rest_port(self):
        config = CredentialConfig(path=self.config_file_path)
        self.assertEqual(4040, config.rest.port)

    @mock.patch.dict(os.environ, {"AUTH_CREDENTIAL_DATABASE_NAME": "db_test_name"})
    def test_overwrite_with_environment_database_name(self):
        config = CredentialConfig(path=self.config_file_path)
        self.assertEqual("db_test_name", config.database.dbname)

    @mock.patch.dict(os.environ, {"AUTH_CREDENTIAL_DATABASE_USER": "test_user"})
    def test_overwrite_with_environment_database_user(self):
        config = CredentialConfig(path=self.config_file_path)
        self.assertEqual("test_user", config.database.user)

    @mock.patch.dict(os.environ, {"AUTH_CREDENTIAL_DATABASE_PASSWORD": "some_pass"})
    def test_overwrite_with_environment_database_password(self):
        config = CredentialConfig(path=self.config_file_path)
        self.assertEqual("some_pass", config.database.password)

    @mock.patch.dict(os.environ, {"AUTH_CREDENTIAL_DATABASE_HOST": "localhost.com"})
    def test_overwrite_with_environment_database_host(self):
        config = CredentialConfig(path=self.config_file_path)
        self.assertEqual("localhost.com", config.database.host)

    @mock.patch.dict(os.environ, {"AUTH_CREDENTIAL_DATABASE_PORT": "2020"})
    def test_overwrite_with_environment_database_port(self):
        config = CredentialConfig(path=self.config_file_path)
        self.assertEqual(2020, config.database.port)


if __name__ == "__main__":
    unittest.main()
