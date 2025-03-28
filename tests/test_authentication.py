"""
This file contains tests to test validation on log in.
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def initial_navigation(page: Page) -> None:
    """
    This fixture (or hook) is used for each test in this file to navigate to this repository before
    each test, to reduce the need for repeated code within the tests directly.

    This specific fixture has been designated to run for every test by setting autouse=True.
    """

    # Navigate to page
    page.goto("https://pathweb-qa.pathways.nhs.uk")


def test_invalid_email(page: Page) -> None:
    """
    Test attempts to log in with an email that is not in use, then asserts the expected message is returned
    """
    page.get_by_label("Email").fill("nhspathways.test+adminnn@nhs.net")
    page.get_by_label("Password").fill("Test")
    page.get_by_role("button", name="Log in").click()
    expect(page.get_by_text("Invalid login attempt.")).to_be_visible()


def test_incorrect_password(page: Page) -> None:
    """
    Test attempts to log in with a valid email but incorrect password, then asserts the expected message is returned
    """
    page.get_by_label("Email").fill("nhspathways.test+admin@nhs.net")
    page.get_by_label("Password").fill("Test")
    page.get_by_role("button", name="Log in").click()
    expect(page.get_by_text("Invalid login attempt.")).to_be_visible()


def test_empty_email(page: Page) -> None:
    """
    Test attempts to log in without entering an email address, then asserts the expected message is returned
    """
    page.get_by_label("Email").fill("")
    page.get_by_label("Password").fill("Test")
    page.get_by_role("button", name="Log in").click()
    expect(page.get_by_text("The Email field is required.")).to_be_visible()


def test_empty_password(page: Page) -> None:
    """
    Test attempts to log in without entering a password, then asserts the expected message is returned
    """
    page.get_by_label("Email").fill("nhspathways.test+admin@nhs.net")
    page.get_by_label("Password").fill("")
    page.get_by_role("button", name="Log in").click()
    expect(page.get_by_text("The Password field is required.")).to_be_visible()
