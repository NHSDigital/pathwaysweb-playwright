from playwright.sync_api import Page, expect
from enum import Enum
from xml.etree import ElementTree
import os


class ConsultationReportPage:

    def __init__(self, page: Page) -> None:
        self.page = page

    def export_as_xml(self) -> None:
        with self.page.expect_download() as download1_info:
            self.page.get_by_role("link", name="Export triage to XML").click()
        downloaded_file_path = f"{os.getcwd()}/test-results/{download1_info.value.suggested_filename}"
        download1_info.value.save_as(downloaded_file_path)
        # checking its contents is a WIP!
        # xml_output = ElementTree.parse(downloaded_file_path)
        # print(xml_output)

    def get_consultation_report_items(self) -> dict:
        # grabbing dt/dd items from page
        section = self.page.locator("div").filter(has_text="CONSULTATION REPORT PRINTED").nth(2)
        all_dt = section.locator("dt")
        all_dd = section.locator("dd")

        # creating a dictionary for dt/dd items
        print(all_dt.count() == all_dd.count())
        element_count = all_dt.count()
        element_nth = 0
        results = {}

        # populates dictionary with dt/dd items
        while element_nth < element_count:
            results[all_dt.nth(element_nth).text_content().replace(":", "")] = all_dd.nth(element_nth).text_content()
            element_nth += 1

        return results
    