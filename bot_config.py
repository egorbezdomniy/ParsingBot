import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parent
PHOTO_DIR = PROJECT_DIR / "photo"
load_dotenv(PROJECT_DIR / ".env")


def subscription_api_url():
    return os.environ["SUBSCRIPTION_API_URL"].rstrip("/") + "/"


def subscription_admin_credentials():
    return {
        "app_password": os.environ["SUBSCRIPTION_API_PASSWORD"],
        "chat_id": os.environ["SUBSCRIPTION_API_ADMIN_ID"],
    }
