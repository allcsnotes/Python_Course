import json
import urllib.request

import pytest

from pages import save_page
from site_app import start_server
from slug import slugify


def test_unit_slug():
    assert slugify("Intro to Python") == "intro-to-python"


def test_integration_page_file(tmp_path):
    save_page(tmp_path, "Intro to Python", "Welcome!")
    page = tmp_path / "intro-to-python.html"
    assert page.read_text() == "Welcome!"


@pytest.fixture
def site():
    server = start_server(8135)
    yield "http://127.0.0.1:8135"
    server.shutdown()


def test_end_to_end_over_http(site):
    url = site + "/?title=Intro%20to%20Python"
    with urllib.request.urlopen(url) as reply:
        data = json.load(reply)
    assert data == {"address": "/courses/intro-to-python"}
