import base64
import logging
from datetime import (
    datetime,
)
from uuid import uuid4

from aiohttp import (
    web,
)
from sqlalchemy.orm import (
    sessionmaker,
)
from sqlalchemy import (
    exc,
)
from .cryptography.cryptography import (
    AuthCrypto,
)
from .database.models import (
    Credential,
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

    Session = sessionmaker(bind=request.app["db_engine"])

    s = Session()

    now = datetime.now()
    uuid = uuid4()
    credential = Credential(
        uuid=uuid,
        username=content["username"],
        password=AuthCrypto().encrypt_password(content["password"]),
        created_at=now,
        updated_at=now,
    )

    try:
        s.add(credential)
        s.commit()
    except exc.IntegrityError:
        return web.json_response(status=500, text="Username is already taken.")

    s.close()
    return web.json_response({"credential": str(uuid)})


async def validate_credentials(request: web.Request) -> web.Response:
    """ Handle Credentials endpoints """

    user, password = await _decode_authorization_header(request)

    Session = sessionmaker(bind=request.app["db_engine"])

    s = Session()

    r = s.query(Credential).filter(Credential.username == user).first()
    s.close()

    if AuthCrypto().check_encrypted_password(password, r.password):
        return web.json_response()

    return web.json_response(status=400, text="User/password not valid")


async def _decode_authorization_header(request: web.Request):
    auth_token = await _get_authorization_header(request)
    bytes = base64.b64decode(auth_token)
    decoded = bytes.decode("utf-8")

    user, password = decoded.split(":")

    return user, password


async def _get_authorization_header(request: web.Request):
    headers = request.headers
    if "Authorization" in headers and "Basic" in headers["Authorization"]:
        parts = headers["Authorization"].split()
        if len(parts) == 2:
            return parts[1]
