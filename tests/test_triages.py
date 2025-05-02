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


@pytest.fixture()
def select_release(page: Page, admin_login) -> None:
    TriagePage(page).select_release("46.2.0")


@pytest.fixture()
# chained fixtures so only need to add the last one in to test
def patient_details(page: Page, select_release) -> dict:
    patient = PatientTools.retrieve_patient("Male First")
    TriagePage(page).populate_patient_details(patient)
    TriagePage(page).select_release("46.2.0")
    return patient


def test_triage_data_cleared_when_triage_is_restarted(
    page: Page, patient_details: dict
) -> None:
    """
    This test begins a triage, clicks Restart Triage and confirms the Summary and Call Report are cleared
    Manual regression reference: PCORE-3954
    """
    triage_page = TriagePage(page)
    triage_page.launch_as(UserSkillset.OPTION_111_CALL_HANDLER.value)

    triage_question_page = TriageQuestionPage(page, patient_details["party"])
    triage_question_page.answer_multiple_questions(
        [
            "an injury, illness or other health problem",
            "no",
            ("illness or other health problem (specify)", "test illness"),
            "no",
            "more",
            "none of the above",
        ]
    )

    triage_question_page.restart_triage()
    expect(triage_question_page.summary_content).to_have_text("\n")
    expect(triage_question_page.call_report_content).to_have_text("\n")


def test_change_first_answer_after_reaching_consultation_report(
    page: Page, patient_details: dict
) -> None:
    """
    This test completes a triage then chooses change triage from the consulatation summary screen and changes the first answer.
    The test confirms that the consultation summary screen reflects the changed answer/triage.
    Manual regression reference: PCORE-6961
    """
    triage_page = TriagePage(page)
    triage_page.launch_as(UserSkillset.OPTION_111_CALL_HANDLER.value)

    triage_question_page = TriageQuestionPage(page, patient_details["party"])
    triage_question_page.basic_triage_as_111_call_handler()

    expect(page.locator("#main-content")).to_contain_text("PMA1 - Calling About Self")
    expect(page.locator("#main-content")).to_contain_text(
        "SG1191 - Health and Social Information"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SD4328 - PC Receive report of results or tests"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Dx78 - I will pass the information on to one of my colleagues."
    )
    expect(page.locator("#main-content")).to_contain_text("Test/results request")

    # change triage/first answer
    page.get_by_role("link", name="< Change Triage").click()
    page.get_by_role(
        "button", name="A report of results or tests was the reason for contact."
    ).click()
    page.get_by_role("button", name="Change Answer").click()

    # complete new triage
    triage_question_page.dx_03_eye_or_eyelid_problems_triage()

    # expects new triage data, does not expect previous triage data
    expect(page.locator("#main-content")).to_contain_text(
        "PW1629 - Eye or Eyelid Problems"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SG1073 - Eye, Red or Irritable"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SD4312 - ED extended ophthalmic assessment and prescribing capability (MECS)"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Dx03 - The individual needs to be referred to a treatment centre within 4 hours."
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Injury, illness or other health problem"
    )
    expect(page.locator("#main-content")).not_to_contain_text(
        "PMA1 - Calling About Self"
    )
    expect(page.locator("#main-content")).not_to_contain_text(
        "SG1191 - Health and Social Information"
    )
    expect(page.locator("#main-content")).not_to_contain_text(
        "SD4328 - PC Receive report of results or tests"
    )
    expect(page.locator("#main-content")).not_to_contain_text(
        "Dx78 - I will pass the information on to one of my colleagues."
    )
    expect(page.locator("#main-content")).not_to_contain_text("Test/results request")


def test_change_mid_triage_answer_after_reaching_conultation_report(
    page: Page, patient_details: dict
) -> None:
    """
    This test completes a triage then chooses change triage from the consulatation summary screen and changes a mid triage answer.
    The test confirms that the consultation summary screen reflects the changed answer.
    Manual regression reference: PCORE-6961
    """
    triage_page = TriagePage(page)
    triage_page.launch_as(UserSkillset.OPTION_111_CALL_HANDLER.value)

    triage_question_page = TriageQuestionPage(page, patient_details["party"])
    triage_question_page.dx_03_eye_or_eyelid_problems_triage()

    expect(page.locator("#main-content")).to_contain_text(
        "PW1629 - Eye or Eyelid Problems"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SG1073 - Eye, Red or Irritable"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SD4312 - ED extended ophthalmic assessment and prescribing capability (MECS)"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Dx03 - The individual needs to be referred to a treatment centre within 4 hours."
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Injury, illness or other health problem"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "The problem affected one eye."
    )

    # change triage/first answer
    page.get_by_role("link", name="< Change Triage").click()
    page.get_by_role("button", name="The problem affected one eye.").click()
    page.get_by_role("button", name="Change Answer").click()

    # new answer to question, then complete triage
    page.get_by_role("button", name="BOTH eyes").click()
    page.get_by_role("button", name="yes", exact=True).click()
    page.get_by_role("button", name="Accept").click()
    page.get_by_text("Someone else should drive the individual.").click()
    page.get_by_role("button", name="Next").click()
    page.get_by_role("checkbox", name="Don't rub the eye.").check()
    page.get_by_text(
        "If there are any new symptoms, or if the condition gets worse, changes or you"
    ).click()
    page.get_by_role("button", name="Save and Close").click()

    expect(page.locator("#main-content")).to_contain_text(
        "PW1629 - Eye or Eyelid Problems"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SG1073 - Eye, Red or Irritable"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "SD4312 - ED extended ophthalmic assessment and prescribing capability (MECS)"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Dx03 - The individual needs to be referred to a treatment centre within 4 hours."
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Injury, illness or other health problem"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "The problem affected both eyes."
    )
