import requests
from typing import TYPE_CHECKING
from http.client import INTERNAL_SERVER_ERROR
from urllib.parse import urljoin
from returns.result import Success, Failure


from ..utils.jwt_helper import JWTHelper

from ..decorators.preview_result import preview_result

if TYPE_CHECKING:
    from typing import List
    from returns.result import Result

    from ..typing import Env, TransactionHistory, TransactionHistoryResponse, JWSTransaction


_BASE_URL = "https://api.storekit-sandbox.itunes.apple.com/"


class StoreKitException(Exception):
    def __init__(self, *, message: str, status_code: int) -> None:
        self.message = message
        self.status_code = status_code


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
    ) -> "Result[TransactionHistory, StoreKitException]":
        response_result = self._get_transaction_history_response(
            original_transaction_id=original_transaction_id, preview=preview
        )
        match response_result:
            case Failure(error):
                error_response: "requests.Response" = error.response
                return Failure(
                    StoreKitException(
                        message=error_response.reason,
                        status_code=error_response.status_code,
                    )
                )
            case Success(response):
                json_response = response
            case _:
                return Failure(
                    StoreKitException(
                        message="something weird happened",
                        status_code=INTERNAL_SERVER_ERROR,
                    )
                )

        decoded_signed_transactions: "List[JWSTransaction]" = []
        for signed_transaction in json_response["signedTransactions"]:
            parsed_decoded_signed_transaction = self._map_signed_transaction_to_transaction(signed_transaction=signed_transaction)
            decoded_signed_transactions.append(parsed_decoded_signed_transaction)

        parsed_response = self._parse_transaction_history_response(response=json_response, transactions=decoded_signed_transactions)
        return Success(parsed_response)

    def _parse_transaction_history_response(self, *, response: "TransactionHistoryResponse", transactions: "List[JWSTransaction]"):
        parsed_response: "TransactionHistory" = {
            "revision": response["revision"],
            "bundle_id": response["bundleId"],
            "environment": response["environment"],
            "has_more": response["hasMore"],
            "transactions": transactions
        }
        return parsed_response

    def _map_signed_transaction_to_transaction(self, *, signed_transaction: str):
        decoded_signed_transaction = self.jwt_helper.decode_jws(payload=signed_transaction)
        parsed_decoded_signed_transaction: "JWSTransaction" = {
            "transaction_id": decoded_signed_transaction["transactionId"],
            "original_transaction_id": decoded_signed_transaction["originalTransactionId"],
            "web_order_line_item_id": decoded_signed_transaction["webOrderLineItemId"],
            "bundle_id": decoded_signed_transaction["bundleId"],
            "product_id": decoded_signed_transaction["productId"],
            "subscription_group_identifier": decoded_signed_transaction["subscriptionGroupIdentifier"],
            "purchase_date": decoded_signed_transaction["purchaseDate"],
            "original_purchase_date": decoded_signed_transaction["originalPurchaseDate"],
            "expires_date": decoded_signed_transaction["expiresDate"],
            "quantity": decoded_signed_transaction["quantity"],
            "type": decoded_signed_transaction["type"],
            "in_app_ownership_type": decoded_signed_transaction["inAppOwnershipType"],
            "signed_date": decoded_signed_transaction["signedDate"],
            "environment": decoded_signed_transaction["environment"]
        }
        return parsed_decoded_signed_transaction

    @preview_result("response.json")
    def _get_transaction_history_response(
        self, *, original_transaction_id: str, preview: bool
    ) -> "Result[TransactionHistoryResponse, requests.HTTPError]":
        url = urljoin(_BASE_URL, f"inApps/v1/history/{original_transaction_id}")
        response = requests.get(url=url, headers=self.headers)

        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            return Failure(error)

        json_response: "TransactionHistoryResponse" = response.json()
        return Success(json_response)
