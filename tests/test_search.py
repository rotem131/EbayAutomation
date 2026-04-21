import pytest
from playwright.async_api import Page
from utils.test_data_provider import get_data


def get_parametrized_data() -> list[tuple[str, float, int]]:
    raw_data = get_data("data", "search_data.json")
    return [
        (item["search_value"], item["max_price"], item["limit"]) for item in raw_data
    ]


@pytest.mark.parametrize("search_value, max_price, limit", get_parametrized_data())
@pytest.mark.asyncio
async def test_search_and_buy_under_budget(
    search_page: Page,
    product_page: Page,
    cart_page: Page,
    search_value: str,
    max_price: str,
    limit: str,
) -> None:
    urls = await search_page.search_items_by_name_under_price(
        search_value, max_price, limit
    )
    await product_page.add_items_to_cart(urls)
    await cart_page.assert_cart_total_not_exceeds(max_price, len(urls))
