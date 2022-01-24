import base64
import logging
from datetime import (
    datetime,
)
from uuid import (
    uuid4,
)

from aiohttp import (
    web,
)
from sqlalchemy import (
    exc,
)
from sqlalchemy.orm import (
    sessionmaker,
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
            return web.json_response({"error": "Wrong data. Provide username and password."}, status=400)
    except Exception:
        return web.json_response({"error": "Wrong data. Provide username and password."}, status=400)

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
        return web.json_response({"error": "Username is already taken."}, status=400)

    s.close()
    return web.json_response({"credential_uuid": str(uuid)})


async def validate_credentials(request: web.Request) -> web.Response:
    """ Handle Credentials endpoints """

    user, password = await _decode_authorization_header(request)

    Session = sessionmaker(bind=request.app["db_engine"])

    s = Session()

    r = s.query(Credential).filter(Credential.username == user).first()
    s.close()

    if AuthCrypto().check_encrypted_password(password, r.password):
        return web.json_response({"credential_uuid": str(r.uuid)})

    return web.json_response({"error": "User/password not valid"}, status=400)


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
