from playwright.sync_api import Page, expect


class BasePage:

    def __init__(self, page: Page) -> None:
        self.page = page

    def check_admin_menu_visible(self) -> None:
        expect(
            self.page.get_by_role("button", name="Admin", exact=True)
        ).to_be_visible()

    def show_admin_menu(self) -> None:
        self.page.get_by_role("button", name="Admin", exact=True).click()

    def manage_users_item_available(self) -> None:
        expect(self.page.get_by_role("list")).to_contain_text("Manage Users")

    def select_manage_users(self) -> None:
        # self.show_admin_menu() #can add this here then dont need to have show_admin_menu in test, or can split them out too.Leaving split out for now as its a bit more readable in the test
        self.page.get_by_role("link", name="Manage Users").click()
        expect(self.page.get_by_role("heading")).to_contain_text("Manage Users")

    def select_system_settings(self) -> None:
        self.page.get_by_role("link", name="System Settings").click()
        expect(self.page.get_by_role("heading")).to_contain_text("System Settings")

    def select_release_management(self) -> None:
        self.page.get_by_role("link", name="Release Management").click()
        expect(self.page.get_by_role("heading")).to_contain_text("Release Management")

    def show_personal_menu(self, email: str = "@") -> None:
        # if we dont pass in an email address to the test then it just checks for @
        self.page.locator("body > header").get_by_text(email).click()

    def select_manage_account(self) -> None:
        self.page.get_by_role("link", name="Manage Account").click()
        expect(self.page.get_by_role("heading")).to_contain_text("Your Account")

    def select_log_off(self) -> None:
        self.page.get_by_role("link", name="Logoff").click()
        expect(self.page.get_by_role("heading")).to_contain_text("Login")

    def check_menu_item_not_present(self, item_to_check: str) -> None:
        expect(
            self.page.locator("body > header").filter(has_text=item_to_check)
        ).to_have_count(0)

    def navigate_home(self) -> None:
        self.page.get_by_role("link", name="Home NHS Pathways Web").click()
        expect(self.page.get_by_role("heading")).to_contain_text(
            "Welcome to NHS Pathways Web"
        )
