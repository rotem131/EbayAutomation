import random
from playwright.async_api import Page, Locator
from pages.base_page import BasePage
from utils.quantity_parser import get_number_quantity
from constants.urls import SEARCH_RESULTS_URL_PATTERN


class ProductPage(BasePage):
    _ADD_TO_CART_AREA = "x-atc-action"
    _ADD_TO_CART_BTN = "ux-call-to-action"
    _ADDED_TO_CART_DIALOG = "ux-overlay"
    _ADDED_TO_CART_DIALOG_INFO = "x-atc-layer-v3"
    _QUANTITY_INPUT = "input[name='quantity']"
    _QUANTITY_AVAILABILITY = "#qtyAvailability"
    _VARIANT_BLOCKS = "div.vim.x-sku"
    _VARIANTS_DROPDOWNS_BTN = "button.listbox-button__control"

    def __init__(self, page: Page, run_id: str) -> None:
        super().__init__(page, run_id)
        self._add_product_to_cart_area = self.page.get_by_test_id(
            self._ADD_TO_CART_AREA
        )
        self._add_product_to_cart_btn = self._add_product_to_cart_area.get_by_test_id(
            self._ADD_TO_CART_BTN
        )
        self._added_to_cart_dialog = self._add_product_to_cart_area.get_by_test_id(
            self._ADDED_TO_CART_DIALOG
        )
        self._added_to_cart_dialog_info = self._added_to_cart_dialog.get_by_test_id(
            self._ADDED_TO_CART_DIALOG_INFO
        )
        self._quantity_input = self.page.locator(self._QUANTITY_INPUT)
        self._quantity_availability = self.page.locator(self._QUANTITY_AVAILABILITY)
        self._variants_blocks = self.page.locator(self._VARIANT_BLOCKS)

    async def add_items_to_cart(self, urls: list[str]) -> None:
        for index, url in enumerate(urls, start=1):
            await self._open_product_page(url)
            await self._add_product_to_cart()
            await self._wait_for_added_to_cart_dialog_to_finish_loading()
            await self.screenshot(category="products", file_name=f"product_{index}.png")
            await self.go_back(wait_for_url=SEARCH_RESULTS_URL_PATTERN)

    async def _open_product_page(self, url_product: str) -> None:
        await self.navigate_to(url_product)

    async def _add_product_to_cart(self) -> None:
        await self._fill_random_variants_if_needed()
        await self.click_element(self._add_product_to_cart_btn)

    async def _fill_random_variants_if_needed(self) -> None:
        variants_blocks_count = await self._variants_blocks.count()

        for index in range(variants_blocks_count):
            select_block = self._variants_blocks.nth(index)
            await self._fill_select_if_needed(select_block)

        await self._fill_quantity_if_needed()

    async def _fill_select_if_needed(self, select_block: Locator) -> None:
        if not await select_block.is_visible():
            return None

        await self._select_random_option_from_listbox(select_block)

    async def _select_random_option_from_listbox(self, select_block: Locator) -> None:
        select = select_block.locator(self._VARIANTS_DROPDOWNS_BTN)
        await self.click_element(select, timeout=8000)

        options = select_block.get_by_role("option")
        if await options.count() == 0:
            return None

        await self.wait_for_element(options.first, timeout=8000)
        valid_options = await self._get_valid_options(options)

        if not valid_options:
            return None

        selected_option = random.choice(valid_options)
        await self.click_element(selected_option, timeout=8000)

    async def _get_valid_options(self, options_list: Locator) -> list[Locator]:
        valid_options: list[Locator] = []
        options_count = await options_list.count()

        for index in range(options_count):
            option = options_list.nth(index)
            aria_disabled = await option.get_attribute("aria-disabled")
            aria_selected = await option.get_attribute("aria-selected")
            text = (await self.get_inner_text(option)).lower()

            if aria_disabled == "true":
                continue

            if aria_selected == "true":
                continue

            if text == "select":
                continue

            valid_options.append(option)

        return valid_options

    async def _fill_quantity_if_needed(self) -> None:
        if (
            await self._quantity_input.count() > 0
            and await self._quantity_input.is_visible()
        ):

            if await self._quantity_availability.count() > 0:
                text = await self.get_inner_text(self._quantity_availability)
                availability_number = get_number_quantity(text)

                if not availability_number:
                    return None

                random_quantity = random.randint(1, availability_number)
                await self.fill_field(self._quantity_input, str(random_quantity))

    async def _wait_for_added_to_cart_dialog_to_finish_loading(self) -> None:
        await self.wait_for_element(self._added_to_cart_dialog)
        await self.wait_for_element(self._added_to_cart_dialog_info)
