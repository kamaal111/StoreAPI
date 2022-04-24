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


@app.get("/transactions/{transactions_id}")
def read_transactions(transactions_id: str):
    env = get_env()
    store_kit = StoreKit(env=env)
    result = store_kit.get_transaction_history(
        original_transaction_id=transactions_id, preview=True
    )
    match result:
        case Failure(error):
            print("failure", error)
            raise HTTPException(status_code=500, detail="noooo!")
        case Success(data):
            _ = data.pop("signedTransactions", None)
            # print(f"{signed_transactions}")
            return {"status": data}
