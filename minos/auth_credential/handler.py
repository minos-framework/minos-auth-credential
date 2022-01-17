import logging
from typing import (
    Any,
    Optional,
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

    verb = request.method

    return web.json_response({})


async def validate_credentials(request: web.Request) -> web.Response:
    """ Handle Credentials endpoints """

    verb = request.method

    return web.json_response({})
