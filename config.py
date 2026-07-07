import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

DB_PATH = os.path.join(DATA_DIR, "qr_history.db")

SECRET_KEY = os.getenv("SECRET_KEY", "cambia-esta-clave")

BASE_URL = os.getenv("BASE_URL")
