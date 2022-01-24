import logging

from aiohttp import (
    web,
)
from aiomisc.service.aiohttp import (
    AIOHTTPService,
)
from sqlalchemy import (
    create_engine,
)

from .config import (
    CredentialConfig,
)
from .database.models import (
    Base,
)
from .handler import (
    add_credentials,
    validate_credentials,
)

logger = logging.getLogger(__name__)


class CredentialRestService(AIOHTTPService):
    def __init__(self, address: str, port: int, config: CredentialConfig):
        self.config = config
        self.engine = None
        super().__init__(address, port)

    async def create_application(self) -> web.Application:
        app = web.Application()

        app["config"] = self.config
        self.engine = await self.create_engine()
        await self.create_database()

        app["db_engine"] = self.engine

        app.router.add_route("POST", "/credentials", add_credentials)
        app.router.add_route("POST", "/credentials/validate", validate_credentials)

        return app

    async def create_engine(self):
        DATABASE_URI = (
            f"postgresql+psycopg2://{self.config.database.user}:{self.config.database.password}@"
            f"{self.config.database.host}:{self.config.database.port}/{self.config.database.dbname}"
        )

        return create_engine(DATABASE_URI)

    async def create_database(self):
        Base.metadata.create_all(self.engine)
