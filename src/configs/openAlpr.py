import sys
from openalpr import Alpr


def recognise(image: str) -> str:
    """

    Args:
        image(str): Image path

    Returns:
        Plate number string

    """
    config_file = 'C:\\Users\\Ani\\Downloads\\openalpr\\openalpr-2.3.0\\config\\openalpr.conf.defaults'
    runtime_dir = "C:\\Users\\Ani\\Downloads\\openalpr\\openalpr-2.3.0\\runtime_data"
    alpr = Alpr('eu', config_file, runtime_dir)

    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

    alpr.set_top_n(1)
    results = alpr.recognize_file(image)
    platenumber = results['results'][0]['plate'][-7:]

    if len(platenumber) != 0:
        return platenumber
    else:
        return "Plate number not found"
