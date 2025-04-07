from playwright.sync_api import Page, expect
from enum import Enum


class UserSkillset(Enum):
    OPTION_111_CALL_HANDLER = "111 Call Handler"
    OPTION_999_CALL_HANDLER = "999 Call Handler"
    OPTION_111_CLINICIAN = "111 Clinician"
    PACCS = "PaCCS"
    INJURY_MODULE = "Injury Module"


class CallQueuePage:

    def __init__(self, page: Page) -> None:
        self.page = page

    def go_to_call_queue_as(self, user_skillset: str) -> None:
        self.page.get_by_label("User Skillset").select_option(user_skillset)
        self.page.get_by_role("button", name="Call Queue").click()

    def add_to_call_queue(self) -> None:
        self.page.get_by_role("button", name="Add to Call Queue").click()
        self.page.get_by_role("button", name="Yes").click()
        self.page.locator("[id='btnClose']").click()

    def find_in_call_queue_and_continue_paccs_triage(self, case_id: str) -> None:
        # look for custom attribute to click and continue triage for case id
        self.page.locator(f"[data-id='{case_id}']").click()
        self.page.get_by_role("button", name="Yes").click()
        expect(self.page.locator("#confirmationModal")).to_contain_text("Case Summary")
        expect(self.page.locator("#confirmationModal")).to_contain_text(case_id)
        self.page.get_by_text("Close", exact=True).click()

    def dx03_injury_module_triage_continued_from_call_queue(self) -> None:
        expect(self.page.locator("h1")).to_contain_text("Pathways Injury Module")
        self.page.locator("#PartialStandard div").filter(
            has_text="bite or sting No 111 Online answer text This means a bite by a human, animal or"
        ).nth(2).click()
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("button", name="sunburn").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="passing less urine than normal").click()
        expect(self.page.locator("#main-content")).to_contain_text(
            "PW987.1800 Refer to a Treatment Centre within 4 hours"
        )
        self.page.get_by_role("button", name="Accept").click()
        self.page.get_by_text("Take any medicines and").click()
        self.page.get_by_role("button", name="Next").click()
        expect(self.page.locator("h1")).to_contain_text(
            "Interim care advice for: Burn, Sun"
        )
        self.page.get_by_title("47850377").click()
        self.page.get_by_role("button", name="Save and Close").click()
