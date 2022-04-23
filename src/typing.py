from typing import List, Literal, TypedDict


class Env(TypedDict):
    key_id: str
    issuer_id: str
    app_id: str


class Transaction(TypedDict):
    revision: str
    bundleId: str
    environment: Literal["Sandbox", "Production"]
    hasMore: bool
    signedTransactions: List[str]
