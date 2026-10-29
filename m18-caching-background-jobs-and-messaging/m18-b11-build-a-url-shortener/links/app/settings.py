import os

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://allcs:allcs@localhost:18511/links",
)
REDIS_URL = os.environ.get(
    "REDIS_URL", "redis://localhost:18411/0"
)
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8691")
CACHE_ENABLED = os.environ.get("CACHE_ENABLED", "1") == "1"
CACHE_SECONDS = int(os.environ.get("CACHE_SECONDS", "3600"))
FLUSH_SECONDS = float(os.environ.get("FLUSH_SECONDS", "5"))
RATE_LIMIT = int(os.environ.get("RATE_LIMIT", "10"))
RATE_WINDOW = int(os.environ.get("RATE_WINDOW", "60"))
