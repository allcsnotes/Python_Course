# Q16 (mock) - Mocking: patch the name where it is LOOKED UP
from unittest.mock import patch

import pytest

from Q16_app import service


def test_patching_the_wrong_place_does_not_help():
    # service already holds its own reference, so this patch changes nothing for it
    with patch("Q16_app.mailer.send_email") as fake:
        with pytest.raises(RuntimeError):
            service.welcome("asha@example.com")
        fake.assert_not_called()


def test_patch_where_it_is_used():
    with patch("Q16_app.service.send_email") as fake:
        assert service.welcome("asha@example.com") == "sent"
    fake.assert_called_once_with("asha@example.com", "Welcome to allcsvideos")


def test_monkeypatch_does_the_same(monkeypatch):
    sent = []
    monkeypatch.setattr(service, "send_email", lambda to, text: sent.append(to))
    service.welcome("lukas@example.com")
    assert sent == ["lukas@example.com"]
