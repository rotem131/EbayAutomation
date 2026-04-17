from pages.base_page import BasePage
from playwright.async_api import Page
from constants.urls import CART_URL
from utils.price_parser import extract_price

class CartPage(BasePage):
    _CART_BTN = f'a[href="{CART_URL}"]'
    _TOTAL_ITEMS_PRICE = "[data-test-id='ITEM_TOTAL']"

    def __init__(self, page: Page, run_id:str) -> None:
        super().__init__(page, run_id)
        self._cart_btn = self.page.locator(self._CART_BTN)
        self._total_items_price = self.page.locator(self._TOTAL_ITEMS_PRICE)

    async def assert_cart_total_not_exceeds(self, budget_per_item: float, items_count: int) -> None:
        await self._open_cart()
        await self.screenshot(
                category="cart",
                file_name="cart.png",
                full_page=True)

        threshold_price = budget_per_item * items_count
        total_price = extract_price(await self.get_inner_text(self._total_items_price))

        assert total_price <= threshold_price, f"Too expensive: {total_price} > {threshold_price}"

    async def _open_cart(self) -> None:
        await self.click_element(self._cart_btn)
        await self.page.wait_for_url(CART_URL, timeout=15000)
