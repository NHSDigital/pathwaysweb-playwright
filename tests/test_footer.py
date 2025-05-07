"""
This file contains tests that relate to the footer items.
"""

import pytest
from playwright.sync_api import Page, expect
from utils.user_tools import UserTools
from pages.base_page import BasePage


@pytest.fixture()
def admin_login(page: Page) -> dict:
    return UserTools.log_in_as_user(page, "Admin")


def test_terms_of_use_available_when_logged_in_or_out(
    page: Page, admin_login: dict
) -> None:
    page.get_by_role("contentinfo").get_by_role("link", name="Terms Of Use").click()
    expect(page.locator(".panel-heading")).to_contain_text("Pathways Web Terms Of Use")
    BasePage(page).show_personal_menu(admin_login["email"])
    BasePage(page).select_log_off()
    page.get_by_role("contentinfo").get_by_role("link", name="Terms Of Use").click()
    expect(page.locator(".panel-heading")).to_contain_text("Pathways Web Terms Of Use")
