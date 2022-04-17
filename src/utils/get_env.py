from os import environ
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..typing import Env


def get_env() -> "Env":
    key_id = environ.get("KEY_ID")
    if not key_id:
        raise Exception("no key id provided")
    issuer_id = environ.get("ISSUER_ID")
    if not issuer_id:
        raise Exception("no issuer id provided")
    app_id = environ.get("APP_ID")
    if not app_id:
        raise Exception("no app id provided")

    return {
        "key_id": key_id,
        "issuer_id": issuer_id,
        "app_id": app_id,
    }
