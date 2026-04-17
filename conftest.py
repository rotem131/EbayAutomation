import pytest
from datetime import datetime
from playwright.async_api import Page
from utils.test_data_provider import get_data
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from config.env_config import load_env

load_env()

@pytest.fixture(scope="session")
def login_data() -> dict:
    return get_data("data", "login.json")

@pytest.fixture(scope="session")
def run_id() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

@pytest.fixture
def login_page(page: Page, run_id:str) -> LoginPage:
    return LoginPage(page, run_id)

@pytest.fixture
def search_page(page: Page, run_id:str) -> SearchPage:
    return SearchPage(page, run_id)

@pytest.fixture
def product_page(page: Page, run_id:str) -> ProductPage:
    return ProductPage(page, run_id)

@pytest.fixture
def cart_page(page: Page, run_id:str) -> CartPage:
    return CartPage(page, run_id)