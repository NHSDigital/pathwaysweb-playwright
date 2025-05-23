from playwright.sync_api import Page, expect
import pytest


class TargetPagesPage:

    def __init__(self, page: Page, party: str) -> None:
        self.page = page
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

        self.save_and_close = page.get_by_role("button", name="Save and Close")

        self.emergency_ambulance = "An emergency ambulance is being arranged"

    def call_handler_dos_triage(self) -> None:
        self.page.get_by_role("button", name="a report of results or tests").click()
        expect(self.main_content).to_contain_text(
            "PA110.400 Receive report of results or tests from laboratory"
        )
        self.page.get_by_text("Repeat Caller: The individual").click()
        self.page.get_by_role("button", name="Reject").click()
        self.page.get_by_role("button", name="Ok").click()
        self.page.get_by_role("checkbox", name="Because you have called").check()
        self.page.get_by_role("button", name="Next").click()
        self.page.get_by_role("button", name="Accept", exact=True).nth(0).click()
        self.page.get_by_role("checkbox", name="If there are any new symptoms").check()
        expect(self.main_content).to_contain_text("Worsening")
        self.save_and_close.click()

    def dx_disposition_il_triage(self) -> None:
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("button", name="mugfuls OR MORE").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("button", name="yes").click()
        expect(self.main_content).to_contain_text(
            "PA123.5900 Emergency Ambulance Response for Major Blood Loss (Category 2)"
        )
        self.page.get_by_role("button", name=self.emergency_ambulance).click()
        self.page.get_by_role("button", name="Early Exit").click()
        self.page.get_by_role("button", name="the phone line went dead").click()
        self.page.get_by_role("button", name="yes").click()
        expect(self.main_content).to_contain_text(
            "CONTINUING BEYOND THIS SCREEN WILL CLOSE THE CALL"
        )
        self.page.get_by_text("EITHER: check the call report").click()
        self.save_and_close.click()

    def cx_care_advice_hc_triage(self) -> None:
        self.page.get_by_role("button", name="a report of results or tests").click()
        self.page.get_by_text(
            "Disposition considered inappropriate - alternative disposition required"
        ).click()
        self.page.get_by_text("Home Management").click()
        self.page.get_by_role("checkbox", name="I am going to give you some").check()
        self.page.get_by_role("button", name="Next").click()
        self.page.get_by_role("textbox", name="Please specify reason for").fill("test")
        self.page.get_by_role("button", name="Ok").click()
        expect(
            self.page.get_by_role("heading", name="Home care advice for: Social")
        ).to_be_visible()
        self.page.get_by_label("Select a specific area for").select_option("Abdomen")
        self.page.get_by_label("Select a sub group for Abdomen area").select_option(
            "10184849"
        )
        self.page.get_by_role("checkbox", name="Unless advised not to, or it").check()
        self.save_and_close.click()

    def cx_care_advice_il_triage(self) -> None:
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("button", name="mugfuls OR MORE").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("button", name="yes").click()
        expect(self.main_content).to_contain_text(
            "PA123.5900 Emergency Ambulance Response for Major Blood Loss (Category 2)"
        )
        self.page.get_by_role("button", name=self.emergency_ambulance).click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="the scene is safe", exact=True).click()
        expect(self.main_content).to_contain_text("PA123.2400 General Safety")
        self.page.get_by_role("checkbox", name="Unless you are in immediate").check()
        self.page.get_by_role("button", name="Next").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="head or face").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="no", exact=True).click()
        expect(self.main_content).to_contain_text("PA25.3000 Wound, bleeding, head")
        self.page.get_by_role("checkbox", name="Use a dry dressing or a clean").check()
        self.page.get_by_role("button", name="Next").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        expect(self.main_content).to_contain_text("PA25.4600 Closing instructions")
        self.page.get_by_text("If you can, ask for someone").click()
        self.save_and_close.click()

    def pa1_triage(self) -> None:
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="unconscious").click()
        self.page.get_by_role("button", name="no - NOT breathing normally").click()
        expect(self.page.get_by_text("PA111.1500 Emergency")).to_be_visible()
        self.page.get_by_role("button", name=self.emergency_ambulance).click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="the scene is safe", exact=True).click()
        expect(
            self.page.locator("#PartialStandard").get_by_text("PA1.0")
        ).to_be_visible()
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("button", name="Early Exit").click()
        self.page.get_by_role("button", name="the phone line went dead").click()
        self.page.get_by_role("button", name="yes").click()
        self.page.get_by_role("checkbox", name="EITHER: check the call report").check()
        self.save_and_close.click()

    def clinician_dos_triage(self) -> None:
        self.page.get_by_role("button", name="a community service").click()
        self.page.get_by_role("button", name="palliative care team").click()
        self.page.get_by_role("button", name="ongoing management").click()
        self.page.get_by_role("button", name="yes").click()
        expect(self.main_content).to_contain_text(
            "PA99.700 Speak to a local service within 1 hour for palliative care"
        )
        self.page.get_by_role(
            "checkbox", name="I will arrange for a clinician to speak to the individual"
        ).check()
        self.page.get_by_role("button", name="Next").click()
        expect(self.main_content).to_contain_text(
            "PA99.700 Speak to a local service within 1 hour for palliative care"
        )
        self.page.locator("#btnAccept0").click()
        expect(self.page.locator("h1")).to_contain_text(
            "Interim care advice for: Predetermined management Plan"
        )
        expect(self.main_content).to_contain_text("Worsening")
        self.page.get_by_role(
            "checkbox",
            name="NO INSTRUCTIONS GIVEN AS CALL RELATES TO AN INDIVIDUAL WHO HAS DIED.",
        ).check()
        self.save_and_close.click()

    def injury_module_triage(self) -> None:
        self.page.get_by_role("button", name="an injury, illness or other").click()
        self.page.get_by_role("button", name="no", exact=True).click()
        self.page.get_by_role("button", name="injury within 7 days (specify)").click()
        self.page.get_by_role("textbox", name="Please specify").fill("blisters")
        self.page.get_by_role("button", name="Ok").click()
        self.page.get_by_role("button", name="yes - a scratch, graze, minor").click()
        expect(self.main_content).to_contain_text(
            "PA124.12700 Pathways injury module, call transfer advice"
        )
        self.page.get_by_text("THIS INJURY MAY BE SUITABLE").click()
        self.page.get_by_role("button", name="Next").click()
        expect(self.main_content).to_contain_text(
            "DO YOU WANT TO CONTINUE TO TRANSFER? PA124.12500"
        )
        self.page.get_by_role("button", name="yes - transfer the call").click()
        expect(self.main_content).to_contain_text(
            "PA124.12600 Speak to a Service Advisor Immediately for Injury Assessment"
        )
        self.page.get_by_text("If the call gets cut off,").click()
        self.save_and_close.click()
        expect(self.main_content).to_contain_text(
            "Consultation Report for Saru Testpatient"
        )
        expect(self.main_content).to_contain_text(
            "THIS INJURY MAY BE SUITABLE FOR TRANSFER TO A SERVICE ADVISOR UNLESS A REASON NOT TO HAS BEEN IDENTIFIED."
        )
