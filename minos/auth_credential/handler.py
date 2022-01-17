import logging
from typing import (
    Any,
    Optional,
)
from datetime import datetime
from uuid import (
    uuid4,
)
from aiohttp import (
    ClientConnectorError,
    ClientResponse,
    ClientSession,
    web,
)
from yarl import (
    URL,
)

from .exceptions import (
    NoTokenException,
)

logger = logging.getLogger(__name__)


async def add_credentials(request: web.Request) -> web.Response:
    """ Handle Credentials endpoints """
    try:
        content = await request.json()

        if "username" not in content or "password" not in content:
            return web.HTTPBadRequest(text="Wrong data. Provide username and password.")
    except Exception:
        return web.HTTPBadRequest(text="Wrong data. Provide username and password.")

    async with request.app["postgres_pool"].acquire() as conn:
        async with conn.cursor() as cur:
            now = datetime.now()
            await cur.execute(
                "INSERT INTO CREDENTIALS(uuid, username, password, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)",
                (uuid4(), content['username'], content['password'], now, now))

    return web.json_response({})


async def validate_credentials(request: web.Request) -> web.Response:
    """ Handle Credentials endpoints """

    verb = request.method

    return web.json_response({})
