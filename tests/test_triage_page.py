"""
This file contains tests that complete triages.
"""

import pytest
from playwright.sync_api import Page, expect
from utils.user_tools import UserTools
from utils.patient_tools import PatientTools
from pages.triage_page import TriagePage, UserSkillset
from pages.triage_question_page import TriageQuestionPage


@pytest.fixture(autouse=True)
def admin_login(page: Page) -> None:
    UserTools.log_in_as_user(page, "Admin")
    page.get_by_role("link", name="Start").click()


def test_triage_data_retained_after_triage(page: Page) -> None:
    """
    Manual regression reference: PCORE-3942, PCORE-3943
    """

    dropdown_values = {
        "Female": "2",
        "111 Clinician": "6",
        "Child (5 to less than 16 years)": "2",
    }

    triage_page = TriagePage(page)
    patient_details = PatientTools.retrieve_patient("All Details Patient")
    triage_page.populate_patient_details(patient_details)
    triage_page.populate_dob_patient_details(patient_details)
    triage_page.populate_extra_patient_details(patient_details)
    triage_page.select_release("46.2.0")
    triage_page.launch_as(UserSkillset.OPTION_111_CLINICIAN.value)

    TriageQuestionPage(page, patient_details["party"]).basic_triage_as_111_clinican()
    page.get_by_role("button", name="Close").click()

    expect(page.get_by_label("First Name", exact=True)).to_have_value(
        patient_details["first_name"]
    )
    expect(page.get_by_label("Last Name", exact=True)).to_have_value(
        patient_details["last_name"]
    )
    expect(page.get_by_label("Age", exact=True)).to_have_value(
        dropdown_values["Child (5 to less than 16 years)"]
    )
    expect(page.get_by_label("Date of Birth", exact=True)).to_have_value(
        patient_details["dob"]
    )
    expect(page.get_by_label("Postcode", exact=True)).to_have_value(
        patient_details["postcode"]
    )
    expect(page.get_by_label("Telephone", exact=True)).to_have_value(
        patient_details["telephone"]
    )
    expect(page.get_by_label("Gender", exact=True)).to_have_value(
        dropdown_values["Female"]
    )
    expect(page.get_by_label(patient_details["party"])).to_be_checked()
    expect(page.get_by_label("Notes", exact=True)).to_have_value(
        patient_details["notes"]
    )
    expect(page.get_by_label("Home GP ODS code", exact=True)).to_have_value(
        patient_details["home_gp"]
    )
    expect(page.get_by_label("Select Pathways Release", exact=True)).to_have_value(
        "46.2.0"
    )
    expect(page.get_by_label("User Skillset", exact=True)).to_have_value(
        dropdown_values["111 Clinician"]
    )
