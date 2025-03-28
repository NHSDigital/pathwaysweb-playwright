from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, page: Page) -> None:
        self.page = page
        expect(self.page.get_by_role("heading")).to_contain_text(
            "Welcome to NHS Pathways Web"
        )
