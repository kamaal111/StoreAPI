import base64
import json
import jwt
import time
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..typing import Env, JWSTransactionResponse


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

    def decode_jws(self, *, payload: str) -> "JWSTransactionResponse":
        segment = payload.split(".")[1]
        extra = (b"=" * (-len(segment) % 4)).decode()
        decoded_segment = base64.b64decode(f"{segment}{extra}")
        return json.loads(decoded_segment)

    @staticmethod
    def _get_private_key():
        with open("store_key.p8", "r") as private_key:
            return private_key.read()
