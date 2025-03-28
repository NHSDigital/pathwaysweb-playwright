import json
import logging
from pathlib import Path


logger = logging.getLogger(__name__)
PATIENTS_FILE = Path(__file__).parent.parent / "test_patients.json"


class PatientTools:
    """
    A utility class for retrieving and populating patient details.
    """

    @staticmethod
    def retrieve_patient(patient: str) -> dict:
        """
        Retrieves the patient information as a dict for the patient provided.

        Args:
            patient (str): The patient details required, using the record key from patients.json.

        Returns:
            dict: A Python dictionary with the details of the patient requested, if present.
        """
        with open(PATIENTS_FILE, "r") as file:
            patient_data = json.loads(file.read())

        if not patient in patient_data:
            raise UserToolsException(
                f"Patient [{patient}] is not present in patients.json"
            )

        logger.debug(f"Returning patient: {patient_data[patient]}")
        return patient_data[patient]


class UserToolsException(Exception):
    pass
