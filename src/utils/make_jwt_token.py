import jwt
import time
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..typing import Env
    from typing import Optional

__private_key: "Optional[str]" = None


def make_jwt_token(*, env: "Env"):
    global __private_key
    if __private_key:
        private_key = __private_key
    else:
        with open("store_key.p8", "r") as store_key:
            __private_key = store_key.read()
            private_key = __private_key

    now = time.time()
    issued_at = int(now)
    minute = 60
    expiration_date = int(now + (minute * 50))
    payload_data = {
        "iss": env["issuer_id"],
        "iat": issued_at,
        "exp": expiration_date,
        "aud": "appstoreconnect-v1",
        "bid": env["app_id"],
    }
    headers = {"alg": "ES256", "kid": env["app_id"], "typ": "JWT"}
    jwt_payload = jwt.encode(
        payload=payload_data, key=private_key, algorithm="RS256", headers=headers
    )

    return jwt_payload
