from playwright.sync_api import Page, expect
from enum import Enum


class UserSkillset(Enum):
    OPTION_111_CALL_HANDLER = "111 Call Handler"
    OPTION_999_CALL_HANDLER = "999 Call Handler"
    OPTION_111_CLINICIAN = "111 Clinician"
    PACCS = "PaCCS"
    INJURY_MODULE = "Injury Module"


class TriagePage:
    # property of the class option, can be used instead of the enum way
    # OPTION_111_CALL_HANDLER = "111 Call Handler"

    def __init__(self, page: Page) -> None:
        self.page = page

    def populate_patient_details(self, patient_details: dict) -> None:
        self.page.get_by_label("First Name", exact=True).fill(
            patient_details["first_name"]
        )
        self.page.get_by_label("Last Name", exact=True).fill(
            patient_details["last_name"]
        )
        self.page.get_by_label("Age", exact=True).select_option(patient_details["age"])
        self.page.get_by_label("Postcode", exact=True).fill(patient_details["postcode"])
        self.page.get_by_label("Gender").select_option(patient_details["gender"])
        self.page.get_by_label(patient_details["party"]).check()

    def launch_as(self, user_skillset: str) -> None:
        self.page.get_by_label("User Skillset").select_option(user_skillset)
        self.page.get_by_role("button", name="Launch").click()

    def select_release(self, release: str) -> None:
        self.page.get_by_label("Select Pathways Release").select_option(release)

    def report_of_results_for_repeat_caller(self) -> None:
        self.page.get_by_role("button", name="a report of results or tests").click()
        expect(self.page.locator("#main-content")).to_contain_text(
            "PA110.400 Receive report of results or tests from laboratory"
        )
        self.page.get_by_label("Repeat Caller: The individual").check()
        self.page.get_by_role("button", name="Accept").click()
        self.page.get_by_label("Because you have called").check()
        self.page.get_by_role("button", name="Next").click()
        expect(self.page.locator("#main-content")).to_contain_text("Worsening")
        self.page.get_by_text(
            "If there are any new symptoms, or if the condition gets worse, changes or you"
        ).click()
        self.page.get_by_role("button", name="Save and Close").click()

    def emergency_ambluance_response_major_blood_loss(self) -> None:
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("button", name="mugfuls OR MORE").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("button", name="yes").click()
        expect(self.page.locator("#main-content")).to_contain_text(
            "PA123.5900 Emergency Ambulance Response for Major Blood Loss (Category 2)"
        )
        self.page.get_by_role("button", name="An emergency ambulance is").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="the scene is safe", exact=True).click()
        self.page.get_by_label("Unless you are in immediate").check()
        self.page.get_by_role("button", name="Next").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="leg, foot or groin").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_label("Use a dry dressing or a clean").check()
        self.page.get_by_role("button", name="Next").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_label("NO INSTRUCTIONS GIVEN AS NOT").check()
        self.page.get_by_role("button", name="Save and Close").click()
