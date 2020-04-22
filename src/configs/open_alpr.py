import sys
from openalpr import Alpr

from lib.commons.constants import OPEN_ALPR_RUNTIME, OPEN_ALPR_CONFIG


def recognise(image: str) -> str:
    """

    Args:
        image(str): Image path

    Returns:
        Plate number string

    """
    alpr = Alpr('eu', OPEN_ALPR_CONFIG, OPEN_ALPR_RUNTIME)

    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

    alpr.set_top_n(1)
    results = alpr.recognize_file(image)
    plate_number = results['results'][0]['plate'][-7:]

    if plate_number:
        return plate_number

    return "Plate number not found"
