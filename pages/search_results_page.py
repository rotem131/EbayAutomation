from playwright.async_api import Page, Locator 
from pages.base_page import BasePage 
from utils.price_parser import extract_prices

class SearchResultsPage(BasePage): 
    _RESULTS_CONTAINER = "#srp-river-results"
    _CARD_RESULTS = "#srp-river-results li.s-card"
    _ALL_PRICES_RESULT = "xpath=.//span[contains(@class, 's-card__price')]"
    _ALL_URL_RESULT = "a.s-card__link"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._results_container = self.page.locator(self._RESULTS_CONTAINER)
        self._results = self.page.locator(self._CARD_RESULTS)

    async def _wait_for_results(self) -> None:
        await self.wait_for_element(self._results_container)
        await self.wait_for_element(self._results.first)

    async def get_prices_from_result(self, result: Locator) -> list[float]:
        price_texts = await result.locator(self._ALL_PRICES_RESULT).all_inner_texts()
        return extract_prices(price_texts)

    async def get_min_price_from_result(self, result: Locator) -> float | None:
        prices = await self.get_prices_from_result(result)
        return min(prices) if prices else None

    async def get_url_from_result(self, result: Locator) -> str | None:
        return await result.locator(self._ALL_URL_RESULT).first.get_attribute("href")

    async def get_result_urls_under_price_from_current_page(self, max_price: float, limit: int) -> list[str]:
        urls: list[str] = []
        await self._wait_for_results()

        count = await self._results.count()
        for i in range(count):
            if len(urls) >= limit:
                break

            result = self._results.nth(i)
            price = await self.get_min_price_from_result(result)

            if price is not None and price <= max_price:
                url = await self.get_url_from_result(result)
                if url:
                    urls.append(url)

        return urls
