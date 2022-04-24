import requests
from typing import TYPE_CHECKING
from urllib.parse import urljoin
from returns.result import Success, Failure


from ..utils.jwt_helper import JWTHelper

from ..decorators.preview_result import preview_result

if TYPE_CHECKING:
    from typing import List
    from returns.result import Result

    from ..typing import Env, TransactionHistory, JWSTransaction


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
        self, *, original_transaction_id: str, preview: bool = False
    ) -> "Result[TransactionHistory, Exception]":
        response_result = self._get_transaction_history_response(
            original_transaction_id=original_transaction_id, preview=preview
        )
        match response_result:
            case Failure(error):
                return Failure(error)
            case Success(response):
                json_response = response
            case _:
                return Failure(Exception("something weird happend"))

        decoded_signed_transactions: "List[JWSTransaction]" = []
        for signed_transaction in json_response["signedTransactions"]:
            decoded_signed_transaction = self.jwt_helper.decode_jws(
                payload=signed_transaction
            )
            decoded_signed_transactions.append(decoded_signed_transaction)

        print(decoded_signed_transactions)

        return Success(json_response)

    @preview_result("response.json")
    def _get_transaction_history_response(
        self, *, original_transaction_id: str, preview: bool
    ) -> "Result[TransactionHistory, requests.HTTPError]":
        url = urljoin(_BASE_URL, f"inApps/v1/history/{original_transaction_id}")
        response = requests.get(url=url, headers=self.headers)

        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            return Failure(error)

        json_response: "TransactionHistory" = response.json()
        return Success(json_response)
