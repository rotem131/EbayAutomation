import logging
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage
from config.env_config import get_base_url

logger = logging.getLogger("pages.login_page")


class LoginPage(BasePage):
    _IDENTITY_AREA = ".gh-identity"
    _USER_NAME_INPUT = "userid"
    _CONTINUE_BTN = "signin-continue-btn"
    _PASS_INPUT = "pass"
    _SIGN_IN_BTN = "sgnBt"

    def __init__(self, page: Page, run_id: str) -> None:
        super().__init__(page, run_id)
        self._identity_area = self.page.locator(self._IDENTITY_AREA)
        self._user_name_input = self.page.get_by_test_id(self._USER_NAME_INPUT)
        self._continue_btn = self.page.get_by_test_id(self._CONTINUE_BTN)
        self._pass_input = self.page.get_by_test_id(self._PASS_INPUT)
        self._sign_in_btn = self.page.get_by_test_id(self._SIGN_IN_BTN)

    async def open_sign_in(self) -> None:
        sign_in_page = self._identity_area.get_by_text("Sign in")
        await self.click_element(sign_in_page)

    async def login(self, username: str, password: str) -> None:
        await self.open_sign_in()

        try:
            await self.fill_field(self._user_name_input, username)
            await self.click_element(self._continue_btn)
            await self.fill_field(self._pass_input, password)
            await self.click_element(self._sign_in_btn)
        except PlaywrightTimeoutError:
            logger.warning("Login failed or Captcha appeared, continue as a guest")
            await self.navigate_to(get_base_url())
