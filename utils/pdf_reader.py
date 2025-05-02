from pypdf import PdfReader


def extract_data_from_pdf(file: str) -> str:
    reader = PdfReader(file)
    page = reader.pages[0]
    # print(page.extract_text())
    return page.extract_text()


# leaving in for testing purposes but it wont run for tests, will eventually delete once happy with the method, and rmeove the test PDF file too
if __name__ == "__main__":
    pdf_text = extract_data_from_pdf(
        "/Users/satu1/Documents/Projects/pathwaysweb-playwright/utils/111_M_A_1st (9).pdf"
    )
    val = """CONSULTATION SUMMARY:
Test/results request
Early Exit from main triage
Assessment ended: call transferred to clinician
Clinician transfer: other complex call - test"""

    print(val in pdf_text)
