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


def test_triage_data_cleared_when_triage_is_restarted(page: Page, patient_details: dict) -> None:
    """
    This test begins a triage, clicks Restart Triage and confirms the Summary and Call Report are cleared
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
                "none of the above"
            ]
        )
    
    triage_question_page.restart_triage()
    expect(triage_question_page.summary_content).to_have_text("\n")
    expect(triage_question_page.call_report_content).to_have_text("\n")

