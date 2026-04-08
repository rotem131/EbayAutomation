import pytest
from utils.test_data_provider import get_data
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture(scope="session")
def config() -> dict:
    return get_data("config", "config.json")


@pytest.fixture(scope="session")
def login_data() -> dict:
    return get_data("data", "login.json")
