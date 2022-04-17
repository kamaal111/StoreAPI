import jwt
from os import environ
from dotenv import load_dotenv

load_dotenv()


def main():
    key_id = environ.get("KEY_ID")
    if not key_id:
        raise Exception("no key id provided")

    payload_data = {"alg": "ES256", "kid": key_id, "typ": "JWT"}
    my_secret = "my_super_secret"
    token = jwt.encode(payload=payload_data, key=my_secret)

    print(token)


if __name__ == "__main__":
    main()
