import os

from dotenv import load_dotenv

load_dotenv()


def get_symbols():
    return [s.strip() for s in os.getenv("SYMBOLS", "").split(",") if s.strip()]


def get_interval():
    return os.getenv("INTERVAL", "15m")


def get_days():
    return int(os.getenv("DAYS", "365"))


def get_backend_host():
    return os.getenv("BACKEND_HOST", "localhost")


def get_backend_port():
    return int(os.getenv("BACKEND_PORT", "5002"))
