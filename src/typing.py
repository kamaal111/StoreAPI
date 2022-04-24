from typing import List, Literal, Optional, TypedDict


class Env(TypedDict):
    key_id: str
    issuer_id: str
    app_id: str


Environment = Literal["Sandbox", "Production"]


class TransactionHistory(TypedDict):
    revision: str
    bundleId: str
    environment: Environment
    hasMore: bool
    signedTransactions: List[str]
    transactions: Optional[List["JWSTransaction"]]


JWSTransaction = TypedDict(
    "JWSTransaction",
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
        "type": Literal[
            "Auto-Renewable Subscription",
            "Non-Consumable",
            "Consumable",
            "Non-Renewing Subscription",
        ],
        "inAppOwnershipType": Literal["FAMILY_SHARED", "PURCHASED"],
        "signedDate": int,
        "environment": Environment,
    },
)
