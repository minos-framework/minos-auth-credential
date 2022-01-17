import logging

from aiohttp import (
    web,
)
from aiomisc.service.aiohttp import (
    AIOHTTPService,
)
import asyncio
import aiopg
from .config import (
    CredentialConfig,
)
from .handler import (
    add_credentials,
    validate_credentials,
)

logger = logging.getLogger(__name__)


class AuthRestService(AIOHTTPService):
    def __init__(self, address: str, port: int, config: CredentialConfig):
        self.config = config
        super().__init__(address, port)

    async def create_application(self) -> web.Application:
        app = web.Application()

        app["config"] = self.config
        app["postgres_pool"] = await self.create_pool()
        await self.initialize_database(app["postgres_pool"])

        app.router.add_route("POST", "/credentials", add_credentials)
        app.router.add_route("POST", "/credentials/validate", validate_credentials)

        return app

    async def create_pool(self):
        dsn = f"dbname={self.config.database.dbname} user={self.config.database.user} " \
              f"password={self.config.database.password} host={self.config.database.host} " \
              f"port={self.config.database.port}"

        return await aiopg.create_pool(dsn)

    async def initialize_database(self, postgres_pool):
        async with postgres_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(_CREATE_UUID_EXTENSION)
                await cur.execute(_CREATE_TABLE_QUERY)


_CREATE_UUID_EXTENSION = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
""".strip()

_CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS credentials (
    uuid UUID NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (uuid, username)
);
""".strip()
