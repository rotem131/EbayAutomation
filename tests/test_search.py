import pytest
from utils.test_data_provider import get_data
from config.env_config import get_base_url

def get_parametrized_data():
    raw_data = get_data("data", "search_data.json")
    return [
        (item["search_value"], item["max_price"], item["limit"])
        for item in raw_data
    ]

@pytest.mark.parametrize("search_value, max_price, limit", get_parametrized_data())
@pytest.mark.asyncio
async def test_search_and_buy_under_budget(search_page, product_page, cart_page, search_value, max_price, limit) -> None:
    urls = await search_page.search_items_by_name_under_price(
        search_value,
        max_price,
        limit
    )
    await product_page.add_items_to_cart(urls)
    await cart_page.assert_cart_total_not_exceeds(max_price, len(urls))