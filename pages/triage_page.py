from playwright.sync_api import Page, expect
from enum import StrEnum


class UserSkillset(StrEnum):
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

    def return_to_triage_page(self) -> None:
        self.page.get_by_role("link", name="Home NHS Pathways Web").click()
        self.page.get_by_role("link", name="Start").click()

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

    def populate_dob_patient_details(self, patient_details: dict) -> None:
        self.page.get_by_role("checkbox", name="Include Date of Birth?").check()
        self.page.get_by_role("textbox", name="Date of Birth").fill(
            patient_details["dob"]
        )

    def populate_extra_patient_details(self, patient_details: dict) -> None:
        self.page.get_by_label("Telephone").fill(patient_details["telephone"])
        self.page.get_by_label("Notes").fill(patient_details["notes"])
        self.page.get_by_label("Home GP ODS code").fill(patient_details["home_gp"])

    def launch_as(self, user_skillset: str) -> None:
        self.page.get_by_label("User Skillset").select_option(user_skillset)
        self.page.get_by_role("button", name="Launch").click()

    def select_release(self, release: str) -> None:
        self.page.get_by_label("Select Pathways Release").select_option(release)

    def jump_to(self, item: str) -> None:
        self.page.get_by_role("textbox", name="Jump to:").fill(item)
        self.page.get_by_role("button", name="Jump").click()
