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
    # TODO: To find a way to merge open_alpr with open_alpr_window by making the config paths platform independent

    # Change this paths correspondingly
    config_file = 'C:\\Users\\Ani\\Downloads\\openalpr\\openalpr-2.3.0\\config\\openalpr.conf.defaults'
    runtime_dir = "C:\\Users\\Ani\\Downloads\\openalpr\\openalpr-2.3.0\\runtime_data"

    alpr = Alpr('eu', config_file, runtime_dir)

    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

    alpr.set_top_n(1)
    results = alpr.recognize_file(image)
    plate_number = results['results'][0]['plate'][-7:]

    if plate_number:
        return plate_number

    return "Plate number not found"
