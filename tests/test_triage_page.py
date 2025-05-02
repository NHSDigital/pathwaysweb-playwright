"""
This file contains tests related to the Triage page.
"""

import pytest
import logging
from playwright.sync_api import Page, expect, Dialog
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
    triage_page.launch_as(UserSkillset.OPTION_111_CLINICIAN)

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


def test_valid_jump_to(page: Page) -> None:
    """
    Manual regression reference: PCORE-3959
    """
    triage_page = TriagePage(page)

    triage_page.select_release("46.2.0")
    triage_page.jump_to("Dx97")
    expect(page.locator("#main-content")).to_contain_text(
        "Emergency Contraception required within 2 hours."
    )
    expect(page.locator("[title='Dx97'][class='panel-heading']")).to_be_visible()

    triage_page.return_to_triage_page()

    triage_page.jump_to("Cx1910")
    expect(page.locator("h1")).to_contain_text(
        "Interim care advice for: Calling About Self"
    )
    expect(page.locator("#main-content")).to_contain_text("Worsening")
    expect(
        page.locator("[title='Cx1910'][class='row panel-heading-internal']")
    ).to_be_visible()

    triage_page.return_to_triage_page()

    triage_page.jump_to("Tx100001")
    expect(page.locator("h1")).to_contain_text("Stopped Breathing 3rd Party")
    expect(page.locator("#PartialStandard")).to_contain_text(
        "Can you see an object in their mouth?"
    )
    expect(
        page.locator("#PartialStandard").locator(
            "[title='Tx100001'][class='heading-question']"
        )
    ).to_be_visible()


def test_invalid_jump_to(page: Page) -> None:
    """
    Manual regression reference: PCORE-3959
    """

    def interact_with_dialog_dx(dialog: Dialog) -> None:
        # Handle the dialog (alert) here
        assert dialog.message == "Dx000001 not found in release 46.2.0."
        dialog.accept()

    def interact_with_dialog_cx(dialog: Dialog) -> None:
        assert dialog.message == "Cx000001 not found in release 46.2.0."
        dialog.accept()

    def interact_with_dialog_tx(dialog: Dialog) -> None:
        assert dialog.message == "Tx000001 not found in release 46.2.0."
        dialog.accept()

    def interact_with_dialog(dialog: Dialog, text: str) -> None:
        assert dialog.message == text
        dialog.accept()

    triage_page = TriagePage(page)

    triage_page.select_release("46.2.0")

    page.once(
        "dialog",
        lambda dialog: interact_with_dialog(
            dialog, "Dx000001 not found in release 46.2.0."
        ),
    )
    triage_page.jump_to("Dx000001")

    page.once("dialog", interact_with_dialog_cx)
    triage_page.jump_to("Cx000001")

    page.once("dialog", interact_with_dialog_tx)
    triage_page.jump_to("Tx000001")
