import logging

from aiohttp import (
    web,
)
from aiomisc.service.aiohttp import (
    AIOHTTPService,
)

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

        app.router.add_route("POST", "/credentials", add_credentials)
        app.router.add_route("POST", "/credentials/validate", validate_credentials)

        return app
