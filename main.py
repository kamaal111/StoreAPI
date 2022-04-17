from dotenv import load_dotenv

from src.utils.get_env import get_env
from src.utils.make_jwt_token import make_jwt_token


load_dotenv()


def main():
    env = get_env()
    jwt_payload = make_jwt_token(env=env)
    print(jwt_payload)


if __name__ == "__main__":
    main()
