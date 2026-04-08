import logging
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage

logger = logging.getLogger("pages.login_page")


class LoginPage(BasePage):
    SIGN_IN_CONTAINER = ".gh-identity"
    USER_ID_INPUT = "data-testid=userid"
    CONTINUE_BTN = "data-testid=signin-continue-btn"
    PASS_INPUT = "data-testid=pass"
    SIGNIN_BTN = "data-testid=sgnBt"

    def login(self, base_url, username, password) -> None:
        self.navigate(base_url)
        self.click_by_text(self.SIGN_IN_CONTAINER, "Sign in")

        try:
            self.fill_field(self.USER_ID_INPUT, username)
            self.click_element(self.CONTINUE_BTN)
            self.fill_field(self.PASS_INPUT, password)
            self.click_element(self.SIGNIN_BTN)
        except PlaywrightTimeoutError:
            logger.warning("Login failed or Captcha appeared, continue as a guest")
            self.navigate(base_url)
