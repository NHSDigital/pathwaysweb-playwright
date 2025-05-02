from playwright.sync_api import Page, expect
from enum import Enum


class PaccsPage:

    def __init__(self, page: Page) -> None:
        self.page = page
