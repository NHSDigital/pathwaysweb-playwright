"""
This file contains tests to confirm users can see the expected menu options based on their role.
"""

import pytest
from playwright.sync_api import Page, expect
from utils.user_tools import UserTools
from pages.home_page import HomePage


@pytest.fixture()
def admin_login(page: Page) -> dict:
    return UserTools.log_in_as_user(page, "Admin")  # returning to use in test.


@pytest.fixture()
def user_login(page: Page) -> dict:
    return UserTools.log_in_as_user(page, "User")


@pytest.fixture()
def pua_login(page: Page) -> dict:
    return UserTools.log_in_as_user(page, "Provider User Admin")


@pytest.fixture()
def ua_login(page: Page) -> dict:
    return UserTools.log_in_as_user(page, "User Admin")


@pytest.fixture()
def deactivated_login(page: Page) -> dict:
    return UserTools.log_in_as_user(page, "Deactivated")


# @pytest.fixture()
# def api_other(api_login: None) -> None:
# print("hello")   #chaining fixtures ", api_other: None" in test


def test_admin_example(page: Page, admin_login: dict) -> None:
    """
    This test accepts cookies, logs in as admin and checks it can see the expected menu options.
    It then logs out and back in, not needed to accept cookies a second time.
    """
    home_page = HomePage(page)

    home_page.show_admin_menu()
    home_page.select_manage_users()

    home_page.navigate_home()  # works for now, but can be tidied to use manage_users_page here later

    home_page.show_admin_menu()  # this could eventually use manage users page as thats where we are when we select this option, but for the purpose of these simp;e tests, its ok for now
    home_page.select_system_settings()

    home_page.navigate_home()  # works for now, but can be tidied to use system_settings_page here later

    home_page.show_admin_menu()
    home_page.select_release_management()

    home_page.navigate_home()  # works for now, but can be tidied to use release_management_page here later

    home_page.show_personal_menu(
        admin_login["email"]
    )  # passing in the email we return in the admin_login fixture
    home_page.select_manage_account()

    home_page.show_personal_menu(admin_login["email"])
    home_page.select_log_off()
    UserTools.log_in_as_user(
        page, "Admin", False
    )  # accept cookies is false because we're not expecting the banner here


def test_user_example(page: Page, user_login: dict) -> None:
    """
    This test accepts cookies, logs in as user and checks it can see/not see the expected menu options.
    It then logs out and back in, not needed to accept cookies a second time.
    """
    home_page = HomePage(page)

    home_page.check_menu_item_not_present("Admin")

    home_page.show_personal_menu(
        user_login["email"]
    )  # passing in the email we return in the user_login fixture
    home_page.select_manage_account()

    home_page.show_personal_menu(user_login["email"])
    home_page.select_log_off()
    UserTools.log_in_as_user(
        page, "User", False
    )  # accept cookies is false because we're not expecting the banner here


def test_pua_example(page: Page, pua_login: dict) -> None:
    """
    This test accepts cookies, logs in as provider user admin and checks it can see/not see the expected menu options.
    It then logs out and back in, not needed to accept cookies a second time.
    """
    home_page = HomePage(page)

    home_page.show_admin_menu()
    home_page.select_manage_users()

    home_page.navigate_home()  # works for now, but can be tidied to use manage_users_page here later

    home_page.check_menu_item_not_present("System Settings")
    home_page.check_menu_item_not_present("Release Management")

    home_page.show_personal_menu(
        pua_login["email"]
    )  # passing in the email we return in the pua_login fixture
    home_page.select_manage_account()

    home_page.navigate_home()  # works for now, but can be tidied to use manage_account_page here later

    home_page.show_personal_menu(pua_login["email"])
    home_page.select_log_off()
    UserTools.log_in_as_user(
        page, "User", False
    )  # accept cookies is false because we're not expecting the banner here


def test_ua_example(page: Page, ua_login: dict) -> None:
    """
    This test accepts cookies, logs in as user admin and checks it can see/not see the expected menu options.
    It then logs out and back in, not needed to accept cookies a second time.
    """
    home_page = HomePage(page)

    home_page.show_admin_menu()
    home_page.select_manage_users()

    home_page.navigate_home()  # works for now, but can be tidied to use manage_users_page here later

    home_page.check_menu_item_not_present("System Settings")
    home_page.check_menu_item_not_present("Release Management")

    home_page.show_personal_menu(
        ua_login["email"]
    )  # passing in the email we return in the pua_login fixture
    home_page.select_manage_account()

    home_page.navigate_home()  # works for now, but can be tidied to use manage_account_page here later

    home_page.show_personal_menu(ua_login["email"])
    home_page.select_log_off()
    UserTools.log_in_as_user(
        page, "User", False
    )  # accept cookies is false because we're not expecting the banner here


def test_deactivated_example(page: Page, deactivated_login: dict) -> None:
    expect(page.get_by_role("heading")).to_contain_text("Login")
    expect(page.locator("#loginForm")).to_contain_text(
        "Your account has been deactivated."
    )
