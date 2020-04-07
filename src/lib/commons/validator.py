import re


def is_armenian_number_plate(text: str) -> bool:
    """

    Args:
        text (str): Number plate string

    Returns:
        True if the input string corresponds to armenian number plate convention
    """

    number_plate_patter_1 = re.compile(r'\d{2}[A-Z]{2}\d{3}')  # for xxYYxxx case, example: 22AM222
    number_plate_patter_2 = re.compile(r'\d{3}[A-Z]{2}\d{2}')  # for xxxYYxx case, example: 222AM22
    result_1 = number_plate_patter_1.match(text)
    result_2 = number_plate_patter_2.match(text)
    return len(text) == 7 and result_1 or result_2
