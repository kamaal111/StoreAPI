from typing import List, Literal, TypedDict


class Env(TypedDict):
    key_id: str
    issuer_id: str
    app_id: str


Environment = Literal["Sandbox", "Production"]
JWSTransactionType = Literal[
    "Auto-Renewable Subscription",
    "Non-Consumable",
    "Consumable",
    "Non-Renewing Subscription",
]
InAppOwnershipType = Literal["FAMILY_SHARED", "PURCHASED"]

class TransactionHistory(TypedDict):
    revision: str
    bundle_id: str
    environment: Environment
    has_more: bool
    transactions: List["JWSTransaction"]

JWSTransaction = TypedDict("JWSTransaction", {
    "transaction_id": str,
    "original_transaction_id": str,
    "web_order_line_item_id": str,
    "bundle_id": str,
    "product_id": str,
    "subscription_group_identifier": str,
    "purchase_date": int,
    "original_purchase_date": int,
    "expires_date": int,
    "quantity": int,
    "type": JWSTransactionType,
    "in_app_ownership_type": InAppOwnershipType,
    "signed_date": int,
    "environment": Environment,
})

class TransactionHistoryResponse(TypedDict):
    revision: str
    bundleId: str
    environment: Environment
    hasMore: bool
    signedTransactions: List[str]


JWSTransactionResponse = TypedDict(
    "JWSTransactionResponse",
    {
        "transactionId": str,
        "originalTransactionId": str,
        "webOrderLineItemId": str,
        "bundleId": str,
        "productId": str,
        "subscriptionGroupIdentifier": str,
        "purchaseDate": int,
        "originalPurchaseDate": int,
        "expiresDate": int,
        "quantity": int,
        "type": JWSTransactionType,
        "inAppOwnershipType": InAppOwnershipType,
        "signedDate": int,
        "environment": Environment,
    },
)
