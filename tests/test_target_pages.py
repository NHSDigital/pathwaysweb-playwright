"""
This file contains the manual regression test from the target pages spreadsheet attached to PCORE-3951.

Its a lift and shift to be reviewed later.
"""

import pytest
from playwright.sync_api import Page, expect
from utils.user_tools import UserTools
from utils.patient_tools import PatientTools
from pages.triage_page import TriagePage, UserSkillset
from pages.target_pages_page import TargetPagesPage


@pytest.fixture(autouse=True)
def admin_login(page: Page) -> None:
    UserTools.log_in_as_user(page, "Admin")
    page.get_by_role("link", name="Start").click()


def test_call_handler_dos(page: Page) -> None:
    """
    This test completes a report of results triage for a repeat caller who rejects the first service

    Manual regression reference: Example 1 "Call Handler DoS" in PCORE-3951
    """
    triage_page = TriagePage(page)

    patient_details = PatientTools.retrieve_patient("Male First")
    triage_page.populate_patient_details(patient_details)

    triage_page.select_release("46.2.0")

    triage_page.launch_as(UserSkillset.OPTION_111_CALL_HANDLER.value)

    TargetPagesPage(page, patient_details["party"]).call_handler_dos_triage()
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


def test_dx_disposition_il(page: Page) -> None:
    """
    This test early exits from a Dx0116 emergency ambulance response triage

    Manual regression reference: Example 2 "DxDispositionIL" in PCORE-3951
    """
    triage_page = TriagePage(page)
    patient_details = PatientTools.retrieve_patient("Male First")
    triage_page.populate_patient_details(patient_details)
    triage_page.select_release("46.2.0")
    triage_page.launch_as(UserSkillset.OPTION_999_CALL_HANDLER.value)

    TargetPagesPage(page, patient_details["party"]).dx_disposition_il_triage()
    expect(page.locator("#main-content")).to_contain_text(
        "Consultation Report for Joe Bloggs"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SG1193 - Immediate threats to life"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SD4215 - AMB major blood loss, trauma"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Dx0116 - Emergency Ambulance Response for Major Blood Loss (Category 2)"
    )
    expect(page.locator("#main-content")).to_contain_text("Early Exit from main triage")
    expect(page.locator("#main-content")).to_contain_text(
        "EITHER: check the call report to confirm that a disposition has been accepted, then continue."
    )


def test_cx_care_advice_hc(page: Page) -> None:
    """
    This test completes a Dx25 home management, disposition override triage

    Manual regression reference: Example 3 "CxCareAdviceHC" in PCORE-3951
    """
    triage_page = TriagePage(page)
    patient_details = PatientTools.retrieve_patient("Male Third")
    triage_page.populate_patient_details(patient_details)

    triage_page.select_release("46.2.0")
    page.get_by_role("checkbox", name="COVID Level 1").check()
    page.get_by_role("checkbox", name="COVID Level 2").check()
    page.get_by_role("checkbox", name="MERS virus").check()

    triage_page.launch_as(UserSkillset.OPTION_111_CLINICIAN.value)

    TargetPagesPage(page, patient_details["party"]).cx_care_advice_hc_triage()
    expect(page.locator("#main-content")).to_contain_text(
        "Consultation Report for Simon Smith"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SG1191 - Health and Social Information"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SD4328 - PC Receive report of results or tests"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Dx25 - From what you have told me, the problem can safely be looked after at home."
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Unless advised not to, or it has already been given, paracetamol may relieve abdominal pain. Follow the instructions in the pack. If in doubt ask a pharmacist."
    )


def test_cx_care_advice_il(page: Page) -> None:
    """
    This test completes a Dx0116 emergency ambulance response triage with inline care advice

    Manual regression reference: Example 4 "CxCareAdviceIL" in PCORE-3951
    """
    triage_page = TriagePage(page)
    patient_details = PatientTools.retrieve_patient("Male First")
    triage_page.populate_patient_details(patient_details)

    triage_page.select_release("46.2.0")

    triage_page.launch_as(UserSkillset.OPTION_999_CALL_HANDLER.value)

    TargetPagesPage(page, patient_details["party"]).cx_care_advice_il_triage()
    expect(page.locator("#main-content")).to_contain_text(
        "Consultation Report for Joe Bloggs"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SG1193 - Immediate threats to life"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SD4215 - AMB major blood loss, trauma"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Dx0116 - Emergency Ambulance Response for Major Blood Loss (Category 2)"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Unless you are in immediate danger, e.g. from traffic or chemical hazards, do not move from your current location."
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Use a dry dressing or a clean cloth folded into a pad and press firmly, directly onto the wound to stop the bleeding."
    )
    expect(page.locator("#main-content")).to_contain_text(
        "If you can, ask for someone to meet and direct the vehicle."
    )


def test_pa1(page: Page) -> None:
    """
    This test completes a Dx010 emergency ambulance response triage with inline care advice

    Manual regression reference: Example 5 "PA1" in PCORE-3951
    """
    triage_page = TriagePage(page)
    patient_details = PatientTools.retrieve_patient("Female Third")
    triage_page.populate_patient_details(patient_details)

    triage_page.select_release("46.2.0")

    triage_page.launch_as(UserSkillset.OPTION_999_CALL_HANDLER.value)

    TargetPagesPage(page, patient_details["party"]).pa1_triage()
    expect(page.locator("#main-content")).to_contain_text(
        "Consultation Report for Joanne Smith"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SG1193 - Immediate threats to life"
    )
    expect(page.locator("#main-content")).to_contain_text("SD4212 - AMB cardiac arrest")
    expect(page.locator("#main-content")).to_contain_text(
        "Dx010 - Emergency Ambulance Response for Potential Cardiac Arrest (Category 1)"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "EITHER: check the call report to confirm that a disposition has been accepted, then continue."
    )


def test_clinician_dos(page: Page) -> None:
    """
    This test completes a Dx0116 emergency ambulance response triage with inline care advice

    Manual regression reference: Example 6 "Clinician DoS" in PCORE-3951
    """
    triage_page = TriagePage(page)
    patient_details = PatientTools.retrieve_patient("Male Third")
    triage_page.populate_patient_details(patient_details)

    triage_page.select_release("46.2.0")
    page.get_by_role("checkbox", name="COVID Level 1").check()
    page.get_by_role("checkbox", name="COVID Level 2").check()
    page.get_by_role("checkbox", name="MERS virus").check()

    triage_page.launch_as(UserSkillset.OPTION_111_CLINICIAN.value)

    TargetPagesPage(page, patient_details["party"]).clinician_dos_triage()
    expect(page.locator("#main-content")).to_contain_text(
        "Consultation Report for Simon Smith"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SG1140 - Predetermined Management Plan"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SD4170 - PC syringe driver management capability - palliative care services"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Dx117 - The individual needs to speak to a local service within 1 hour for palliative care."
    )
    expect(page.locator("#main-content")).to_contain_text(
        "NO INSTRUCTIONS GIVEN AS CALL RELATES TO AN INDIVIDUAL WHO HAS DIED."
    )
