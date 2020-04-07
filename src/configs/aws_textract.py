import boto3

from lib.commons.validator import is_armenian_number_plate


def recognise(image: str) -> str:
    """

    Args:
        image (str): Image path

    Returns:
        Detected number plate string

    """

    # Read image content
    with open(image, 'rb') as document:
        imageBytes = bytearray(document.read())

    # Amazon Textract client
    textract = boto3.client('textract')

    # Call Amazon Textract
    response = textract.detect_document_text(Document={'Bytes': imageBytes})

    # Print detected text
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            sentence = ''.join(item["Text"].split())
            if is_armenian_number_plate(sentence):
                return sentence
