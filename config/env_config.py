import os
from dotenv import load_dotenv


def load_env():
    env = os.getenv("ENVIRONMENT", "example")
    load_dotenv(f".env.{env}")


def get_base_url() -> str:
    return os.getenv("BASE_URL")