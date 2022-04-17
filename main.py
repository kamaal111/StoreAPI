import jwt
import time
from os import environ
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization


load_dotenv()


def main():
    key_id = environ.get("KEY_ID")
    if not key_id:
        raise Exception("no key id provided")
    issuer_id = environ.get("ISSUER_ID")
    if not issuer_id:
        raise Exception("no issuer id provided")
    app_id = environ.get("APP_ID")
    if not app_id:
        raise Exception("no app id provided")

    with open(".ssh/id_rsa", "r") as id_rsa:
        private_key = id_rsa.read()

    now = time.time()
    issued_at = int(now)
    minute = 60
    expiration_date = now + (minute * 50)
    payload_data = {
        "iss": issuer_id,
        "iat": issued_at,
        "exp": expiration_date,
        "aud": "appstoreconnect-v1",
        "bid": app_id,
    }
    key = serialization.load_ssh_private_key(private_key.encode(), password=b"")
    jwt_payload = jwt.encode(payload=payload_data, key=key, algorithm="RS256")  # type: ignore

    print(jwt_payload)


if __name__ == "__main__":
    main()
