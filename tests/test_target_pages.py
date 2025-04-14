"""
This file contains the manual regression test from the target pages spreadsheet attached to PCORE-3951.

Its a lift and shift to be reviewed later.
"""

import pytest
from playwright.sync_api import Page, expect, Selectors
from utils.user_tools import UserTools
from utils.patient_tools import PatientTools
from pages.triage_page import TriagePage, UserSkillset
from pages.target_pages_page import TargetPagesPage
from pages.consultation_report_page import ConsultationReportPage
from pages.call_queue_page import CallQueuePage, UserSkillset
from pages.triage_question_page import TriageQuestionPage


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
        f"Consultation Report for {patient_details["first_name"]} {patient_details["last_name"]}"
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
        f"Consultation Report for {patient_details["first_name"]} {patient_details["last_name"]}"
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
        f"Consultation Report for {patient_details["first_name"]} {patient_details["last_name"]}"
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
        f"Consultation Report for {patient_details["first_name"]} {patient_details["last_name"]}"
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
        f"Consultation Report for {patient_details["first_name"]} {patient_details["last_name"]}"
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
        f"Consultation Report for {patient_details["first_name"]} {patient_details["last_name"]}"
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


def test_paccs_exploratory(page: Page) -> None:
    """
    This test does some exploratory checks on PaCCS
    Manual regression reference: PaCCS example (part1) on Target Pages tab in spreadsheet in PCORE-3951
    """
    triage_page = TriagePage(page)
    patient_details = PatientTools.retrieve_patient("Male First")
    triage_page.populate_patient_details(patient_details)

    triage_page.select_release("46.2.0")

    triage_page.launch_as(UserSkillset.PACCS.value)
    # complete paccs triage, including going back and return no change, add to call queue
    page.get_by_role("textbox", name="Symptom Search").fill("leg")
    page.get_by_role("link", name="Leg Injury, Blunt").click()
    page.get_by_role("checkbox", name="Multiple Injuries Considered").check()
    page.get_by_role(
        "checkbox", name="New or Worsening Pain and/or Swelling Suspected"
    ).check()
    page.get_by_role("button", name="Home Care", exact=True).click()
    page.get_by_role("button", name="Leg Injury, Blunt/New or").click()
    expect(page.locator("h1")).to_contain_text("Pathways Clinical Consultation Support")
    page.get_by_role("button", name="Return No Change").click()
    expect(page.locator("h1")).to_contain_text(
        "Home care advice for: PaCCS Home Management Suite"
    )
    page.get_by_title("47317975").click()
    page.get_by_role("button", name="Save and Close").click()


def test_picking_up_non_paccs_triage_from_call_queue_as_paccs_user(page: Page) -> None:
    """
    This test adds a basic triage to call queue, picked up as a PaCCS user to complete
    Manual regression reference: PaCCS example (part2) on Target Pages tab in spreadsheet in PCORE-3951
    """
    triage_page = TriagePage(page)

    patient_details = PatientTools.retrieve_patient("Male First")
    triage_page.populate_patient_details(patient_details)

    triage_page.select_release("46.2.0")

    triage_page.launch_as(UserSkillset.OPTION_111_CALL_HANDLER.value)

    TriageQuestionPage(
        page, patient_details["party"]
    ).basic_triage_as_111_call_handler()

    # grab case id and other info
    items = ConsultationReportPage(page).get_consultation_report_items()

    # add to call queue
    CallQueuePage(page).add_to_call_queue()

    # go to call queue as PaCCS user
    CallQueuePage(page).go_to_call_queue_as(UserSkillset.PACCS.value)

    # find and continue paccs triage
    CallQueuePage(page).find_in_call_queue_and_continue_paccs_triage(
        items["CASE ID"], items["PATIENT"]
    )

    # triage continued
    TriageQuestionPage(page).basic_paccs_triage()
    page.get_by_role("button", name="Close").click()

    # check triage is gone from call queue
    CallQueuePage(page).go_to_call_queue_as(UserSkillset.PACCS.value)
    expect(page.locator(f"[data-id='{items["CASE ID"]}']")).to_have_count(0)


def test_picking_up_injury_module_triage_from_call_queue_as_injury_module_user(
    page: Page,
) -> None:
    """
    This test adds an injury module triage to call queue, and picked up as a Injury Module user to complete
    Manual regression reference: Injury module example on Target Pages tab in spreadsheet in PCORE-3951
    """
    triage_page = TriagePage(page)

    patient_details = PatientTools.retrieve_patient("Male First")
    triage_page.populate_patient_details(patient_details)

    triage_page.select_release("42.2.0")
    page.get_by_role("checkbox", name="Injury Module").check()

    triage_page.launch_as(UserSkillset.OPTION_111_CALL_HANDLER.value)

    TargetPagesPage(page, patient_details["party"]).injury_module_triage()

    items = ConsultationReportPage(
        page
    ).get_consultation_report_items()  # case ID grabbed in here

    # add to call queue
    CallQueuePage(page).add_to_call_queue()

    # go to call queue as injury module user
    CallQueuePage(page).go_to_call_queue_as(UserSkillset.INJURY_MODULE.value)

    # find and continue triage
    CallQueuePage(page).find_in_call_queue_and_continue_injury_module_triage(
        items["CASE ID"], items["PATIENT"]
    )

    # triage continued
    CallQueuePage(page).dx03_injury_module_triage_continued_from_call_queue()

    # assertions for injury module outcome and completion
    expect(page.locator("#main-content")).to_contain_text("Injury Module")
    expect(page.locator("#main-content")).to_contain_text("SG1158 - Sunburn")
    expect(page.locator("#main-content")).to_contain_text("SD4050 - ED dehydration")
    expect(page.locator("#main-content")).to_contain_text(
        "Dx03 - The individual needs to be referred to a treatment centre within 4 hours."
    )
    page.get_by_role("button", name="Close").click()

    # check triage is gone from call queue
    CallQueuePage(page).go_to_call_queue_as(UserSkillset.INJURY_MODULE.value)
    expect(page.locator(f"[data-id='{items["CASE ID"]}']")).to_have_count(0)
