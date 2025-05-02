"""
This file contains tests that complete triages.
"""

import pytest
from playwright.sync_api import Page, expect
from utils.user_tools import UserTools
from utils.patient_tools import PatientTools
from utils.pdf_reader import extract_data_from_pdf
from pages.triage_page import TriagePage, UserSkillset
from pages.triage_question_page import TriageQuestionPage
from pages.early_exit_page import EarlyExitPage
from pages.consultation_report_page import ConsultationReportPage


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


def test_early_exit_from_question_screen(page: Page, patient_details: dict) -> None:
    """
    This test early exits from a question screen and completes to consultation report.
    It then clicks change triage, goes back to the screen we early exited from, changes the answer and completes to consultation report without early exiting.
    Each completion checks the details on the consultation report page.
    Manual regression reference: PCORE-7530
    """
    triage_page = TriagePage(page)
    triage_page.launch_as(UserSkillset.OPTION_111_CALL_HANDLER.value)

    page.get_by_role("textbox", name="Additional Text").fill("Test1")

    # early exit
    early_exit_page = EarlyExitPage(page)
    early_exit_page.early_exit_from_main_triage(" User comment - Test1")
    early_exit_page.early_exit_transfer_to_clinician_route()

    # consultation report
    expect(page.locator("#main-content")).to_contain_text(
        f"Consultation Report for {patient_details["first_name"]} {patient_details["last_name"]}"
    )
    # in Consultation Summary section
    expect(
        page.locator("#main-content")
        .locator("ul:below(:text('CONSULTATION SUMMARY:'))")
        .first
    ).to_contain_text("Early Exit from main triage - Test1")
    # in Pathways Assessment section
    expect(
        page.locator("#main-content")
        .locator("ul:below(:text('PATHWAYS ASSESSMENT:'))")
        .first
    ).to_contain_text("Early Exit from main triage - Test1")

    # download and extract data from PDF
    pdf_text = extract_data_from_pdf(ConsultationReportPage(page).export_as_pdf())
    expected_text = "Early Exit from main triage - Test1"
    assert expected_text in pdf_text

    # change triage, go to screen we early exited from
    page.get_by_role("link", name="< Change Triage").click()
    page.get_by_role("button", name="Early Exit from main triage").click()

    # takes you back to screen we early exited from, retained additional text
    expect(page.locator("#PartialStandard")).to_contain_text(
        "What is the reason for the contact?"
    )
    expect(page.locator("#addText")).to_contain_text("Test1")

    # change answer
    page.get_by_role("button", name="Change Answer").click()

    # still retains additional text
    expect(page.locator("#addText")).to_contain_text("Test1")

    # call report and summary is cleared
    triage_question_page = TriageQuestionPage(page)
    expect(triage_question_page.summary_content).to_have_text("\n")
    expect(triage_question_page.call_report_content).to_have_text("\n")

    # complete triage without early exiting
    triage_question_page.basic_triage_as_111_call_handler()
    expect(page.locator("#main-content")).to_contain_text(
        f"Consultation Report for {patient_details["first_name"]} {patient_details["last_name"]}"
    )
    expect(page.locator("#main-content")).not_to_contain_text(
        "Early Exit from main triage - Test1"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Test/results request - Test1"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "A report of results or tests was the reason for contact. - Test1"
    )


def test_early_exit_from_disposition_screen(page: Page, patient_details: dict) -> None:
    """
    This test early exits from a disposition screen and completes to consultation report.
    It then clicks change triage, goes back to the screen we early exited from, changes the answer and completes to consultation report without early exiting.
    Each completion checks the details on the consultation report page.
    Manual regression reference: PCORE-7531
    """
    triage_page = TriagePage(page)
    triage_page.launch_as(UserSkillset.OPTION_111_CALL_HANDLER.value)

    # navigate to and update dispo screen
    page.get_by_role("button", name="a report of results or tests").click()

    page.get_by_role("textbox", name="Additional Text").fill("Test1")
    page.get_by_role("radio", name="Repeat Caller: The individual").check()
    page.get_by_role("button", name="Accept").click()
    page.get_by_role("checkbox", name="Because you have called").check()

    # early exit
    early_exit_page = EarlyExitPage(page)
    early_exit_page.early_exit_from_main_triage(" User comment - Test1")
    early_exit_page.early_exit_transfer_to_clinician_route()

    # consultation report checks
    expect(page.locator("#main-content")).to_contain_text(
        f"Consultation Report for {patient_details["first_name"]} {patient_details["last_name"]}"
    )
    # in Consultation Summary section
    expect(
        page.locator("#main-content")
        .locator("ul:below(:text('CONSULTATION SUMMARY:'))")
        .first
    ).to_contain_text("Early Exit from main triage - Test1")
    # in Pathways Assessment section
    expect(
        page.locator("#main-content")
        .locator("ul:below(:text('PATHWAYS ASSESSMENT:'))")
        .first
    ).to_contain_text("Early Exit from main triage - Test1")

    # download and extract data from PDF
    pdf_text = extract_data_from_pdf(ConsultationReportPage(page).export_as_pdf())
    expected_text = "Early Exit from main triage - Test1"
    assert expected_text in pdf_text

    # change triage
    page.get_by_role("link", name="< Change Triage").click()

    # click early exit log in call report takes you back to screen we early exited from
    page.get_by_role("button", name="Early Exit from main triage").click()

    # has retained previously inputted data
    expect(page.locator("#main-content")).to_contain_text(
        "PA110.5 Receive report of results or tests from laboratory"
    )
    expect(page.locator("#addText")).to_contain_text("Test1")
    expect(
        page.get_by_role("radio", name="Repeat Caller: The individual")
    ).to_be_checked()
    expect(page.locator('[id="\\34 7320427"]')).to_be_checked()

    # change answer
    page.get_by_role("button", name="Change Answer").click()

    # has retained previously inputted data
    expect(page.locator("#main-content")).to_contain_text(
        "PA110.5 Receive report of results or tests from laboratory"
    )
    expect(page.locator("#addText")).to_contain_text("Test1")
    expect(
        page.get_by_role("radio", name="Repeat Caller: The individual")
    ).to_be_checked()
    expect(page.locator('[id="\\34 7320427"]')).to_be_checked()

    # call report and summary does not contain early exit logs
    triage_question_page = TriageQuestionPage(page)
    expect(triage_question_page.summary_content).to_have_text("Test/results request")
    expect(triage_question_page.summary_content).not_to_have_text(
        "Early Exit from main triage User comment - Test1"
    )
    expect(triage_question_page.call_report_content).to_contain_text(
        "A report of results or tests was the reason for contact."
    )
    expect(triage_question_page.call_report_content).not_to_contain_text(
        "Early Exit from main triage User comment - Test1"
    )

    # complete triage without early exiting
    page.get_by_role("radio", name="I will pass the information").click()
    page.get_by_role("button", name="Accept").click()
    page.get_by_role("checkbox", name="We will pass the details onto").check()
    page.get_by_role("button", name="Save and Close").click()

    # expect no mention of early exit
    expect(page.locator("#main-content")).to_contain_text(
        f"Consultation Report for {patient_details["first_name"]} {patient_details["last_name"]}"
    )
    expect(page.locator("#main-content")).not_to_contain_text(
        "Early Exit from main triage - Test1"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Dx78 - I will pass the information on to one of my colleagues. - Test1"
    )
    expect(page.locator("#main-content")).to_contain_text("Test/results request")
    expect(page.locator("#main-content")).to_contain_text(
        "A report of results or tests was the reason for contact."
    )


def test_early_exit_from_disposition_ep_override_screen(
    page: Page, patient_details: dict
) -> None:
    """
    This test early exits from a disposition EP override screen and completes to consultation report.
    It then clicks change triage, goes back to the screen we early exited from, changes the answer and completes to consultation report without early exiting.
    Each completion checks the details on the consultation report page.
    Manual regression reference: PCORE-7532
    """
    triage_page = TriagePage(page)
    triage_page.launch_as(UserSkillset.OPTION_111_CLINICIAN.value)

    # navigate to and update dispoEPoverride screen
    page.get_by_role("button", name="a report of results or tests").click()

    page.get_by_role("textbox", name="Additional Text").fill("Test1")
    page.get_by_role(
        "radio",
        name="Disposition considered appropriate - caller unlikely to follow disposition",
    ).check()
    page.get_by_role("radio", name="Home Management").check()
    page.get_by_role("checkbox", name="I am going to give you some").check()

    # early exit
    early_exit_page = EarlyExitPage(page)
    early_exit_page.early_exit_from_main_triage(" User comment - Test1")
    early_exit_page.early_exit_home_management_route()

    # consultation report checks
    expect(page.locator("#main-content")).to_contain_text(
        f"Consultation Report for {patient_details["first_name"]} {patient_details["last_name"]}"
    )
    # in Consultation Summary section
    expect(
        page.locator("#main-content")
        .locator("ul:below(:text('CONSULTATION SUMMARY:'))")
        .first
    ).to_contain_text("Early Exit from main triage - Test1")
    # in Pathways Assessment section
    expect(
        page.locator("#main-content")
        .locator("ul:below(:text('PATHWAYS ASSESSMENT:'))")
        .first
    ).to_contain_text("Early Exit from main triage - Test1")

    # download and extract data from PDF
    pdf_text = extract_data_from_pdf(ConsultationReportPage(page).export_as_pdf())
    expected_text = "Early Exit from main triage - Test1"
    assert expected_text in pdf_text

    # change triage
    page.get_by_role("link", name="< Change Triage").click()

    # click early exit log in call report takes you back to screen we early exited from
    page.get_by_role("button", name="Early Exit from main triage").click()

    # has retained previously inputted data
    expect(
        page.get_by_text("PA110.5 Receive report of results or tests from laboratory")
    ).to_be_visible()
    expect(
        page.get_by_role(
            "radio",
            name="Disposition considered appropriate - caller unlikely to follow disposition",
        )
    ).to_be_checked()
    expect(page.get_by_role("radio", name="Home Management")).to_be_checked()
    expect(
        page.get_by_role(
            "checkbox",
            name="I am going to give you some information that will help to manage the symptoms at home.",
        )
    ).to_be_checked()
    expect(page.get_by_role("textbox", name="Additional Text")).to_have_value("Test1")

    # change answer
    page.get_by_role("button", name="Change Answer").click()

    # has retained previously inputted data
    expect(
        page.get_by_text("PA110.5 Receive report of results or tests from laboratory")
    ).to_be_visible()
    expect(
        page.get_by_role(
            "radio",
            name="Disposition considered appropriate - caller unlikely to follow disposition",
        )
    ).to_be_checked()
    expect(page.get_by_role("radio", name="Home Management")).to_be_checked()
    expect(
        page.get_by_role(
            "checkbox",
            name="I am going to give you some information that will help to manage the symptoms at home.",
        )
    ).to_be_checked()
    expect(page.get_by_role("textbox", name="Additional Text")).to_have_value("Test1")

    # call report and summary does not contain early exit logs
    triage_question_page = TriageQuestionPage(page)
    expect(triage_question_page.summary_content).to_have_text("Test/results request")
    expect(triage_question_page.summary_content).not_to_have_text(
        "Early Exit from main triage User comment - Test1"
    )
    expect(triage_question_page.call_report_content).to_contain_text(
        "A report of results or tests was the reason for contact."
    )
    expect(triage_question_page.call_report_content).not_to_contain_text(
        "Early Exit from main triage User comment - Test1"
    )

    # complete triage without early exiting
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox", name="Please specify reason for").fill("test comment 3")
    page.get_by_role("button", name="Ok").click()
    page.get_by_role("checkbox", name="If there are any new symptoms").check()
    page.get_by_role("button", name="Save and Close").click()

    # expect no mention of early exit
    expect(page.locator("#main-content")).to_contain_text(
        f"Consultation Report for {patient_details["first_name"]} {patient_details["last_name"]}"
    )
    expect(page.locator("#main-content")).not_to_contain_text(
        "Early Exit from main triage - Test1"
    )
    expect(page.locator("#main-content")).to_contain_text(
        "Dx25 - From what you have told me, the problem can safely be looked after at home. - Additional Text: Test1"
    )
    expect(page.locator("#main-content")).to_contain_text("Test/results request")
    expect(page.locator("#main-content")).to_contain_text(
        "A report of results or tests was the reason for contact."
    )
