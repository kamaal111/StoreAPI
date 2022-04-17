from dotenv import load_dotenv
from returns.result import Success, Failure

from src.clients.store_kit import StoreKit
from src.utils.get_env import get_env


load_dotenv()


def main():
    env = get_env()
    store_kit = StoreKit(env=env)
    result = store_kit.get_transaction_history(original_transaction_id="123")
    match result:
        case Failure(error):
            print("failure", error)
        case Success(data):
            print("success", data)


if __name__ == "__main__":
    main()
