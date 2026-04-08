from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, url: str) -> None:
        self.page.goto(url)

    def click_element(self, selector: str) -> None:
        locator = self.page.locator(selector)
        locator.wait_for(state="visible")
        locator.click()

    def click_by_text(self, selector: str, text: str) -> None:
        locator = self.page.locator(selector).get_by_text(text, exact=False)
        locator.wait_for(state="visible")
        locator.click()

    def fill_field(self, selector: str, text: str) -> None:
        locator = self.page.locator(selector)
        locator.wait_for(state="visible")
        locator.fill(text)
