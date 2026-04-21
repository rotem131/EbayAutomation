from playwright.async_api import Page
from pages.base_page import BasePage
from pages.search_results_page import SearchResultsPage
from pages.filter_page import FilterPage
from constants.urls import SEARCH_RESULTS_URL_PATTERN


class SearchPage(BasePage):
    _SEARCH_INPUT = "#gh-ac"
    _SEARCH_BTN = "#gh-search-btn"
    _PAGINATION_ITEM_NEXT = "a.pagination__next"
    _PAGINATION_ITEM_CURRENT = "a.pagination__item[aria-current='page']"

    def __init__(self, page: Page, run_id: str) -> None:
        super().__init__(page, run_id)
        self._search_input = self.page.locator(self._SEARCH_INPUT)
        self._search_btn = self.page.locator(self._SEARCH_BTN)
        self._pagination_next_btn = self.page.locator(self._PAGINATION_ITEM_NEXT)
        self._current_page_results_btn = self.page.locator(
            self._PAGINATION_ITEM_CURRENT
        )

    async def _search(self, value: str) -> None:
        await self.fill_field(self._search_input, value)
        await self.click_element(self._search_btn)
        await self.page.wait_for_url(SEARCH_RESULTS_URL_PATTERN, timeout=15000)

    async def _has_next_page(self) -> bool:
        return (
            await self._pagination_next_btn.count() > 0
            and await self._pagination_next_btn.is_visible()
            and await self._pagination_next_btn.is_enabled()
        )

    async def _go_to_next_page(self) -> bool:
        if not await self._has_next_page():
            return False

        current_page = int(await self.get_inner_text(self._current_page_results_btn))
        await self.click_element(self._pagination_next_btn)

        results_page = SearchResultsPage(self.page, self.run_id)
        await results_page.wait_for_results()

        next_page = int(await self.get_inner_text(self._current_page_results_btn))
        return next_page == current_page + 1

    async def search_items_by_name_under_price(
        self, query: str, max_price: float, limit: int = 5
    ) -> list[str]:
        urls: list[str] = []
        filter_page = FilterPage(self.page, self.run_id)
        results_page = SearchResultsPage(self.page, self.run_id)

        await self._search(query)
        await results_page.wait_for_results()

        await filter_page.open_dialog_filters()
        await filter_page.add_max_price_filter(max_price)
        await results_page.wait_for_results()

        if await results_page.get_results_count() == 0:
            return []

        while len(urls) < limit:
            current_page_urls = (
                await results_page.get_result_urls_under_price_from_current_page(
                    max_price=max_price,
                    limit=limit - len(urls),
                )
            )
            urls.extend(current_page_urls)

            if len(urls) >= limit:
                break

            moved = await self._go_to_next_page()
            if not moved:
                break

        return urls
