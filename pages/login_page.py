from playwright.sync_api import Page, expect


class LoginPage:

    def __init__(self, page: Page) -> None:
        self.page = page

    def login(self, email: str, password: str, accept_cookies: bool = True) -> None:
        self.page.goto("/")  # using base url set in pytest.ini
        if accept_cookies:
            self.page.get_by_role("button", name="Allow all cookies").click()
            # checks if cookies is there before clicking, arg added to user_tools too
        self.page.get_by_role("textbox", name="Email").fill(email)
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="Log in").click()
