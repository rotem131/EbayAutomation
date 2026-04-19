import pytest
import allure
import re
from pathlib import Path
from datetime import datetime
from playwright.async_api import Page
from utils.test_data_provider import get_data
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from config.env_config import load_env

load_env()

SCREENSHOT_NAME_PATTERN = re.compile(r"^test-failed-\d+\.png$")
TRACE_FILE_PATTERN = re.compile(r".*trace.*\.zip$")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    yield

    try:
        test_artifacts_path = item.funcargs.get("output_path")

        if test_artifacts_path:
            test_artifacts_dir = Path(test_artifacts_path)

            if test_artifacts_dir.is_dir():
                for file in test_artifacts_dir.iterdir():
                    if file.is_file() and SCREENSHOT_NAME_PATTERN.match(file.name):
                        allure.attach.file(
                            str(file),
                            name="Failure Screenshot",
                            attachment_type=allure.attachment_type.PNG,
                        )
                    elif TRACE_FILE_PATTERN.match(file.name):
                            allure.attach.file(
                                str(file),
                                name="Playwright Trace",
                                attachment_type=allure.attachment_type.ZIP,
                            )

    except Exception as e:
        print(f"Error attaching screenshot: {e}")

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