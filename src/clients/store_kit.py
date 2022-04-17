import requests
from typing import TYPE_CHECKING
from urllib.parse import urljoin
from returns.result import Success, Failure

from ..utils.make_jwt_token import make_jwt_token

if TYPE_CHECKING:
    from returns.result import Result

    from ..typing import Env


_BASE_URL = "https://api.storekit-sandbox.itunes.apple.com/"


class StoreKit:
    env: "Env"

    def __init__(self, *, env: "Env"):
        self.env = env

    @property
    def headers(self):
        jwt_token = make_jwt_token(env=self.env)
        return {
            "Authorization": f"Bearer {jwt_token}",
        }

    def get_transaction_history(
        self, *, original_transaction_id: str
    ) -> "Result[requests.Response, requests.HTTPError]":
        url = urljoin(_BASE_URL, f"inApps/v1/history/{original_transaction_id}")
        response = requests.get(url=url, headers=self.headers)

        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            return Failure(error)

        return Success(response)
