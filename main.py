from typing import TYPE_CHECKING
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from returns.result import Success, Failure

from src.clients.store_kit import StoreKit
from src.utils.get_env import get_env

if TYPE_CHECKING:
    from requests import Response


load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/transactions/{transactions_id}")
def read_transactions(transactions_id: str):
    env = get_env()
    store_kit = StoreKit(env=env)
    result = store_kit.get_transaction_history(original_transaction_id=transactions_id)
    match result:
        case Failure(error):
            print("failure", error)
            response: "Response" = error.response
            raise HTTPException(status_code=response.status_code, detail="noooo!")
        case Success(data):
            signed_transactions = data.pop("signedTransactions", None)
            print(f"{signed_transactions}")
            return {"status": data}
