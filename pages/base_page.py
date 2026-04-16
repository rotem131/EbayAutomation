from playwright.async_api import Page, Locator

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.default_timeout = 10000

    async def navigate_to(self, url: str) -> None:
        await self.page.goto(url)

    async def wait_for_element(self, element: Locator, state: str = "visible", timeout: int | None = None) -> Locator:
        actual_timeout = self.default_timeout if timeout is None else timeout
        await element.wait_for(state=state, timeout=actual_timeout)
    
    async def click_element(self, element: Locator, timeout: int | None = None) -> None:
        await self.wait_for_element(element, timeout=timeout)
        await element.click()

    async def fill_field(self, element: Locator, value: str, timeout: int | None = None) -> None:
        await self.wait_for_element(element, timeout=timeout)
        await element.fill(value)

    async def get_inner_text(self, element: Locator) -> str:
        return (await element.inner_text()).strip()
