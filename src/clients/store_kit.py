import requests
from typing import TYPE_CHECKING
from urllib.parse import urljoin
from returns.result import Success, Failure

from ..utils.jwt_helper import JWTHelper

if TYPE_CHECKING:
    from returns.result import Result

    from ..typing import Env, Transaction


_BASE_URL = "https://api.storekit-sandbox.itunes.apple.com/"


class StoreKit:
    env: "Env"

    jwt_helper = JWTHelper()

    def __init__(self, *, env: "Env"):
        self.env = env

    @property
    def headers(self):
        jwt_token = self.jwt_helper.make_token(env=self.env)
        return {
            "Authorization": f"Bearer {jwt_token}",
        }

    def get_transaction_history(
        self, *, original_transaction_id: str
    ) -> "Result[Transaction, requests.HTTPError]":
        url = urljoin(_BASE_URL, f"inApps/v1/history/{original_transaction_id}")
        response = requests.get(url=url, headers=self.headers)

        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            return Failure(error)

        json_response: "Transaction" = response.json()

        for signed_transaction in json_response["signedTransactions"]:
            decoded_transaction = self.jwt_helper.decode_token(
                payload=signed_transaction
            )
            print(f"{decoded_transaction=}")

        return Success(json_response)
