import base64
import binascii
import jwt
import time
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..typing import Env


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
        for segment in payload.split("."):
            extra = (b"=" * (-len(segment) % 4)).decode()
            try:
                decoded_segment = base64.b64decode(segment + extra)
                print(decoded_segment)
            except binascii.Error as error:
                print(f"{error=}")

        return ""

    @staticmethod
    def _get_private_key():
        with open("store_key.p8", "r") as private_key:
            return private_key.read()
