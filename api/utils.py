from datetime import datetime
from preprocess_data import Data
from report import Report


def validate_date(date_str: str) -> bool:
    """
    Validates the format of a date string.

    This function checks if the provided date string follows the "YYYY-MM-DD" format.

    Args:
        date_str (str): A date string.

    Returns:
        bool: True if the date string is in a valid format, False otherwise.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def construct_report(date: str):
    """
    Constructs a report for a given date.

    This function builds and returns a report if records exist for the provided date.
    If no records exist, it returns a string stating that no entries exist for this date.

    Args:
        date (str): A valid date string in the format of "YYYY-MM-DD".

    Returns:
        Union[dict, str]: The report as a dictionary if records from that date exist.
        Otherwise, a string stating that no entries exist for this date.
    """
    data = Data()
    data.isolate_data_by_date(date)

    if len(data.orders):
        report = Report()
        return report.get_report(data)
    else:
        return "There are no records available for the specified date."
