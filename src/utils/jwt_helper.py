import jwt
import time
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..typing import Env
    from typing import Optional

_internal_private_key: "Optional[str]" = None


class JWTHelper:
    ALGORITHM = "ES256"

    def __init__(self) -> None:
        pass

    def make_token(self, *, env: "Env"):
        private_key = JWTHelper._get_private_key()

        now = time.time()
        issued_at = int(now)
        minute = 60
        expiration_date = issued_at + (minute * 50)
        payload_data = {
            "iss": env["issuer_id"],
            "iat": issued_at,
            "exp": expiration_date,
            "aud": "appstoreconnect-v1",
            "bid": env["app_id"],
        }
        headers = {"alg": self.ALGORITHM, "kid": env["key_id"], "typ": "JWT"}
        jwt_payload = jwt.encode(payload=payload_data, key=private_key, headers=headers)

        return jwt_payload

    def decode_token(self, *, payload: str):
        private_key = JWTHelper._get_private_key()
        return jwt.decode(jwt=payload, key=private_key, algorithms=[self.ALGORITHM])

    @staticmethod
    def _get_private_key():
        global _internal_private_key
        if _internal_private_key:
            private_key = _internal_private_key
        else:
            with open("store_key.p8", "r") as store_key:
                _internal_private_key = store_key.read()
                private_key = _internal_private_key

        return private_key
