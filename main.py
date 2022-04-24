from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from returns.result import Success, Failure

from src.clients.store_kit import StoreKit
from src.utils.get_env import get_env


load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/transaction-history/{transactions_id}")
def read_transaction_history(transactions_id: str):
    env = get_env()
    store_kit = StoreKit(env=env)
    result = store_kit.get_transaction_history(original_transaction_id=transactions_id)
    match result:
        case Failure(error):
            raise HTTPException(
                status_code=error.status_code, detail=error.message
            ) from error
        case Success(data):
            _ = data.pop("signedTransactions", None)
            return data
