import re 
from playwright.async_api import Page 
from pages.base_page import BasePage

class FilterPage(BasePage): 
    _DIALOG_FILTER = "#refineOverlay[role='dialog']"
    _MAX_PRICE_INPUT = ".x-refine__price input[aria-label*='Maximum']" 
    _APPLY_DIALOG_BTN = ".x-overlay-footer__apply button"

    def __init__(self, page: Page, run_id:str) -> None:
        super().__init__(page, run_id)
        self._dialog_container = self.page.locator(self._DIALOG_FILTER)
        self._max_price_input = self._dialog_container.locator(self._MAX_PRICE_INPUT)
        self._apply_dialog_btn = self._dialog_container.locator(self._APPLY_DIALOG_BTN)
        self._more_filters_btn = self.page.get_by_role("button", name=re.compile(r"More filters", re.I))

    async def open_dialog_filters(self) -> None:
        await self.click_element(self._more_filters_btn.first)
        await self.wait_for_element(self._dialog_container)

    async def _apply_dialog_filters(self) -> None:
        await self.click_element(self._apply_dialog_btn)
        await self.wait_for_element(self._dialog_container, state="hidden")

    async def _choose_category_filter(self, category_name: str) -> None:
        category_tab = self._dialog_container.get_by_role("tab", name=re.compile(category_name, re.I))
        await self.click_element(category_tab)

    async def add_max_price_filter(self, max_price: float) -> None:
        await self._choose_category_filter("Price")
        await self.fill_field(self._max_price_input, str(max_price))
        await self._max_price_input.press("Enter")
        await self._apply_dialog_filters()