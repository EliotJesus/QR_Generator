import secrets
import string
from datetime import datetime
from urllib.parse import urlparse

from flask import request

from config import BASE_URL
from database import get_db


def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ["http", "https"] and bool(parsed.netloc)


def generate_code(length=7):
    alphabet = string.ascii_letters + string.digits

    with get_db() as conn:
        while True:
            code = "".join(secrets.choice(alphabet) for _ in range(length))

            exists = conn.execute(
                "SELECT id FROM links WHERE code = ?",
                (code,)
            ).fetchone()

            if not exists:
                return code


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_public_base_url():
    if BASE_URL:
        return BASE_URL.rstrip("/")

    return request.url_root.rstrip("/")