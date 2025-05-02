from playwright.sync_api import Page, expect
import pytest


class EarlyExitPage:

    def __init__(self, page: Page) -> None:
        self.page = page

        self.save_and_close = page.get_by_role("button", name="Save and Close")

        self.please_specify = page.get_by_role("textbox", name="Please specify")

    def early_exit_from_main_triage(self, user_comment: str) -> None:
        self.page.get_by_role("button", name="Early Exit").click()
        expect(
            self.page.get_by_role("button", name="Early Exit from main triage")
        ).to_be_visible()
        expect(self.page.get_by_label("Call Report")).to_contain_text(
            "Early Exit from main triage" + user_comment
        )

    def early_exit_transfer_to_clinician_route(self) -> None:
        self.page.get_by_role("button", name="transfer to a clinician").click()
        self.page.get_by_role("button", name="other (specify)").click()
        self.please_specify.click()
        self.please_specify.fill("test comment")
        self.page.get_by_role("button", name="Ok").click()
        self.page.get_by_role("checkbox", name="No worsening instructions").check()
        self.save_and_close.click()

    def early_exit_home_management_route(self) -> None:
        self.page.get_by_role("button", name="more").click()
        self.page.get_by_role("button", name="caller refuses disposition (").click()
        self.page.get_by_role("textbox", name="Please specify").fill("test comment 2")
        self.page.get_by_role("button", name="Ok").click()
        self.page.get_by_role("button", name="other").click()
        self.page.get_by_role("button", name="more").click()
        self.page.get_by_role("button", name="home management").click()
        self.page.get_by_text("I am going to give you some").click()
        self.page.get_by_role("button", name="Next", exact=True).click()
        self.page.get_by_title("47317975").click()
        self.save_and_close.click()
