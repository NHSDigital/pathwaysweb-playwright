from playwright.sync_api import Page, expect
import pytest


class TriageQuestionPage:

    def __init__(self, page: Page, party: str = None) -> None:
        self.page = page
        if party is not None:
            if party == "1st Party":
                expect(
                    self.page.get_by_role("heading", name="Calling About Self")
                ).to_be_visible()
            elif party == "3rd Party":
                expect(
                    self.page.get_by_role("heading", name="Calling About Someone Else")
                ).to_be_visible()
            else:
                pytest.fail("The party provided is invalid")

        self.main_content = self.page.locator("#main-content")

        self.save_and_close = "Save and Close"

        self.report_of_results = "a report of results or tests"

        self.summary_content = page.locator("[aria-labelledby='panelSummary']").locator(
            ".panel-body"
        )

        self.call_report_content = page.locator(
            "[aria-labelledby='call-report-heading']"
        ).locator(".panel-body")

    def answer_question(self, answer: str | tuple) -> None:
        """
        If a string is provided then the button matching the text is clicked.
        If a tuple is provided then the button matching the first text is clicked,
        and the second text provided is entered in the please specify field.

        Providing the following in the test step:
        ("illness or other health problem (specify)", "test illness")
        results in clicking the button with the text "illness or other health problem (specify)"
        and then entering "test illness" in the please specify field.
        """
        if isinstance(answer, tuple):
            self.page.get_by_role("button", name=answer[0], exact=True).click()
            self.page.get_by_role("textbox", name="Please specify").fill(answer[1])
            self.page.get_by_role("button", name="Ok").click()
        else:
            self.page.get_by_role("button", name=answer, exact=True).click()

    def answer_multiple_questions(self, answers: list[str | tuple]) -> None:
        """
        Uses answer_question method to allow answering multiple questions.
        """
        for answer in answers:
            self.answer_question(answer)

    def restart_triage(self) -> None:
        self.page.get_by_role("button", name="Restart Triage").click()

    def basic_triage_as_111_call_handler(self) -> None:
        self.answer_question(self.report_of_results)
        self.page.get_by_role("button", name="Accept").click()
        self.page.get_by_text("We will pass the details onto").click()
        self.page.get_by_role("button", name=self.save_and_close).click()

    def basic_triage_as_111_clinican(self) -> None:
        self.answer_question(self.report_of_results)
        self.page.get_by_role("radio", name="I will pass the information").check()
        self.page.get_by_role("radio", name="Disposition is appropriate").check()
        self.page.get_by_role("checkbox", name="We will pass the details onto").check()
        self.page.get_by_role("button", name=self.save_and_close).click()
        self.page.get_by_role("button", name="Accept").click()

    def basic_paccs_triage(self) -> None:
        self.page.get_by_role("textbox", name="Symptom Search").fill("results")
        self.page.get_by_role("link", name="Report of results or tests").click()
        self.page.get_by_role(
            "checkbox",
            name="Report of results or tests - case able to be completed Suspected",
        ).check()
        self.page.get_by_role("button", name="Home Care", exact=True).click()
        self.page.get_by_title("47317975").click()
        # If there are any new symptoms, or if the condition gets worse, changes or you have any other concerns call us back.
        self.page.get_by_role("button", name="Save and Close").click()

    def report_of_results_for_repeat_caller(self) -> None:
        self.answer_question(self.report_of_results)
        expect(self.main_content).to_contain_text(
            "PA110.400 Receive report of results or tests from laboratory"
        )
        self.page.get_by_label("Repeat Caller: The individual").check()
        self.page.get_by_role("button", name="Accept").click()
        self.page.get_by_label("Because you have called").check()
        self.page.get_by_role("button", name="Next").click()
        expect(self.main_content).to_contain_text("Worsening")
        self.page.get_by_text(
            "If there are any new symptoms, or if the condition gets worse, changes or you"
        ).click()
        self.page.get_by_role("button", name=self.save_and_close).click()

    def emergency_ambluance_response_major_blood_loss(self) -> None:
        self.answer_multiple_questions(
            ["yes", "yes", "2 mugfuls OR MORE", "no", "yes", "yes"]
        )
        expect(self.main_content).to_contain_text(
            "PA123.5900 Emergency Ambulance Response for Major Blood Loss (Category 2)"
        )
        self.answer_multiple_questions(
            [
                "An emergency ambulance is being arranged.",
                "no",
                "yes",
                "no",
                "the scene is safe",
            ]
        )
        self.page.get_by_label(
            "Unless you are in immediate danger, e.g. from traffic or chemical hazards, do not move from your current location."
        ).check()
        self.answer_multiple_questions(
            ["Next", "no", "no", "leg, foot or groin", "no", "no"]
        )
        self.page.get_by_label(
            "Use a dry dressing or a clean cloth folded into a pad and press firmly, directly onto the wound to stop the bleeding."
        ).check()
        self.answer_multiple_questions(["Next", "no"])

        self.page.get_by_label(
            "NO INSTRUCTIONS GIVEN AS NOT SAFE AND/OR APPROPRIATE."
        ).check()
        self.page.get_by_role("button", name=self.save_and_close).click()

    def dx_03_eye_or_eyelid_problems_triage(self) -> None:
        self.page.get_by_role("button", name="an injury, illness or other").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="illness or other health").click()
        self.page.get_by_role("textbox", name="Please specify").click()
        self.page.get_by_role("textbox", name="Please specify").fill("test")
        self.page.get_by_role("button", name="Ok").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="more").click()
        self.page.get_by_role("button", name="none of the above").click()
        self.page.get_by_role("button", name="yes - normal, warm or hot").click()
        self.page.get_by_role("button", name="eye").click()
        self.page.get_by_role("button", name="Eye or Eyelid Problems").click()
        self.page.get_by_role("button", name="Start - Eye or Eyelid Problems").click()
        self.page.get_by_role("button", name="eye redness or irritation").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="ONE eye").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("button", name="Accept").click()
        self.page.get_by_text("Someone else should drive the individual.").click()
        self.page.get_by_role("button", name="Next").click()
        self.page.get_by_role("checkbox", name="Don't rub the eye.").check()
        self.page.get_by_role(
            "checkbox",
            name="If there are any new symptoms, or if the condition gets worse, changes or you have any other concerns, call us back.",
        ).check()
        self.page.get_by_role("button", name="Save and Close").click()
