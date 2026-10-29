import pytest
from pydantic import ValidationError

from app.settings import Settings

GOOD = {
    "database_url": "postgresql+psycopg://u:p@db:5432/x",
    "redis_url": "redis://cache:6379/0",
    "secret_key": "a-long-enough-secret-key",
}


def make(**changes):
    return Settings(_env_file=None, **{**GOOD, **changes})


def test_good_settings_load():
    assert make().environment == "dev"


def test_missing_database_url_fails(monkeypatch):
    monkeypatch.delenv("DATABASE_URL")
    values = dict(GOOD)
    del values["database_url"]
    with pytest.raises(ValidationError):
        Settings(_env_file=None, **values)


def test_short_secret_fails():
    with pytest.raises(ValidationError, match="secret_key"):
        make(secret_key="short")


def test_prod_must_not_log_debug():
    with pytest.raises(ValidationError, match="DEBUG"):
        make(environment="prod", log_level="DEBUG")


def test_text_false_is_false():
    assert make(signup_open="false").signup_open is False
