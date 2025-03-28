import json
import logging
import os
from pathlib import Path
from playwright.sync_api import Page, expect
from dotenv import load_dotenv
from pages.login_page import LoginPage


logger = logging.getLogger(__name__)
USERS_FILE = Path(__file__).parent.parent / "users.json"


class UserTools:
    """
    A utility class for retrieving and doing common actions with users.
    """

    @staticmethod
    def retrieve_user(user: str) -> dict:
        """
        Retrieves the user information as a dict for the user provided.

        Args:
            user (str): The user details required, using the record key from users.json.

        Returns:
            dict: A Python dictionary with the details of the user requested, if present.
        """
        with open(USERS_FILE, "r") as file:
            user_data = json.loads(file.read())

        if not user in user_data:
            raise UserToolsException(f"User [{user}] is not present in users.json")

        logger.debug(f"Returning user: {user_data[user]}")
        return user_data[user]

    def log_in_as_user(page: Page, user: str, accept_cookies: bool = True) -> dict:
        # Load dotenv to enable retrieval of a password from .env file
        load_dotenv()
        user_details = UserTools.retrieve_user(user)
        LoginPage(page).login(
            user_details["email"], os.getenv("PWW_PASS"), accept_cookies
        )
        return user_details  # returning so we can use the user details in the tests


class UserToolsException(Exception):
    pass
