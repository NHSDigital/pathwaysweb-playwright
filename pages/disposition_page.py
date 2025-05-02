from playwright.sync_api import Page, expect
from enum import Enum


class DispositionPage:

    def __init__(self, page: Page) -> None:
        self.page = page

    def repeat_caller_rejects_first_service(self) -> None:
        self.page.get_by_label("Repeat Caller: The individual").check()
        self.page.get_by_text("Because you have called").click()
        self.page.get_by_role("button", name="Reject").click()
        self.page.get_by_label("Please select a reason for").select_option("99")
        self.page.get_by_role("button", name="Ok").click()
        self.page.get_by_role("button", name="Next").click()
        self.page.get_by_role("button", name="Accept", exact=True).nth(0).click()
