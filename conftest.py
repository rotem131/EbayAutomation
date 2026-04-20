import pytest
import allure
import logging
import time
import pytest_asyncio
from pathlib import Path
from datetime import datetime
from playwright.async_api import Page
from utils.test_data_provider import get_data
from pages.base_page import BasePage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from config.env_config import load_env
from config.env_config import get_base_url

logger = logging.getLogger("conftest")

load_env()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    yield

    test_artifacts_path = item.funcargs.get("output_path")

    if test_artifacts_path:
        test_artifacts_dir = Path(test_artifacts_path)

        if test_artifacts_dir.is_dir():
            for file in test_artifacts_dir.glob("*.zip"):
                try:
                    allure.attach.file(
                        str(file),
                        name="Playwright Trace",
                        attachment_type=allure.attachment_type.ZIP,
                    )
                except Exception as e:
                    logger.error(f"Failed to attach trace: {e}")


@pytest_asyncio.fixture(scope="function", loop_scope="session")
async def ebay_page(page: Page, run_id: str):
    base_page = BasePage(page, run_id)
    await base_page.navigate_to(get_base_url())
    return page


@pytest_asyncio.fixture(scope="function", loop_scope="session")
async def search_page(ebay_page: Page, run_id: str) -> SearchPage:
    return SearchPage(ebay_page, run_id)


@pytest_asyncio.fixture(scope="function", loop_scope="session")
async def product_page(ebay_page: Page, run_id: str) -> ProductPage:
    return ProductPage(ebay_page, run_id)


@pytest_asyncio.fixture(scope="function", loop_scope="session")
async def cart_page(ebay_page: Page, run_id: str) -> CartPage:
    return CartPage(ebay_page, run_id)

@pytest.fixture(scope="session")
def login_data() -> dict:
    return get_data("data", "login.json")

@pytest.fixture(scope="session")
def run_id() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
