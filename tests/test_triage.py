"""
This file contains tests that complete triages.
"""

import pytest
from playwright.sync_api import Page, expect
from utils.user_tools import UserTools
from utils.patient_tools import PatientTools
from pages.triage_page import TriagePage, UserSkillset


@pytest.fixture(autouse=True)
def admin_login(page: Page) -> None:
    UserTools.log_in_as_user(page, "Admin")
    page.get_by_role("link", name="Start").click()


# @pytest.fixture()
# def patient_details(page: Page) -> None:
#     return PatientTools.retrieve_patient(page, "Joe Bloggs")  # dont need a fixture if we add it in the test. Removed arg - patient_details: dict


def test_repeat_caller(page: Page) -> None:
    """
    This test completes a Dx93 repeat caller triage

    Manual regression reference: Example 1 "Call Handler DoS" in PCORE-3951
    """
    triage_page = TriagePage(page)

    # using utils PatientTools so we can pull in the details of the patient
    patient_details = PatientTools.retrieve_patient("Joe Bloggs")
    # uses retrieved patient details, handled by TriagePage
    triage_page.populate_patient_details(patient_details)

    # method in page triage to select release
    triage_page.select_release("46.2.0")

    # if we were using the class option, use this to initialise the page:
    # (TriagePage(page).OPTION_111_CALL_HANDLER)
    # using enum
    triage_page.launch_as(UserSkillset.OPTION_111_CALL_HANDLER.value)

    triage_page.report_of_results_for_repeat_caller()
    expect(page.locator("#main-content")).to_contain_text(
        "Consultation Report for Joe Bloggs"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SYMPTOM GROUP: SG1191 - Health and Social Information"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SYMPTOM DISCRIMINATOR: SD4328 - PC Receive report of results or tests"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "DISPOSITION: Dx93 - Repeat Caller: The individual needs to speak to the GP practice within 1 hour. If the practice is not open within this period they need to speak to the out of hours service."
    )


def test_emergency_ambulance_response(page: Page) -> None:
    """
    This test completes a Dx0116 Emergency Ambulance response triage

    Manual regression reference: Example 2 "DxDispositionIL" in PCORE-3951
    """
    triage_page = TriagePage(page)
    patient_details = PatientTools.retrieve_patient("Joe Bloggs")
    triage_page.populate_patient_details(patient_details)
    triage_page.select_release("46.2.0")
    triage_page.launch_as(UserSkillset.OPTION_999_CALL_HANDLER.value)

    triage_page.emergency_ambluance_response_major_blood_loss()
    expect(page.locator("#main-content")).to_contain_text(
        "SG1193 - Immediate threats to life"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SD4215 - AMB major blood loss, trauma"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Dx0116 - Emergency Ambulance Response for Major Blood Loss (Category 2)"
    )
