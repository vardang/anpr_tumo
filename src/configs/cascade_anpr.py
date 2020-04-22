import cv2
import numpy as np
import pytesseract
from PIL import Image
import os


def computeSafeRegion(shape: tuple, bounding_rect: tuple) -> tuple:
    """

    Args:
        shape(np.ndarray): Image shape
        bounding_rect(tuple): Rectangle x,y,w,h

    Returns:
        Safe region coordinates

    """
    top = bounding_rect[1]  # y
    bottom = bounding_rect[1] + bounding_rect[3]  # y +  h
    left = bounding_rect[0]  # x
    right = bounding_rect[0] + bounding_rect[2]  # x +  w
    min_top = 0
    max_bottom = shape[0]
    min_left = 0
    max_right = shape[1]

    if top < min_top:
        top = min_top
    if left < min_left:
        left = min_left
    if bottom > max_bottom:
        bottom = max_bottom
    if right > max_right:
        right = max_right

    return [left, top, right - left, bottom - top]


def cropImage(image: np.ndarray, rect: tuple) -> np.ndarray:
    """

    Args:
        image(np.ndarray): Image
        rect(tuple): rectangle x,y,h,w

    Returns:
        First cropped image

    """
    x, y, w, h = computeSafeRegion(image.shape, rect)
    return image[y:y + h, x:x + w]


def detectPlateRough(image_gray: np.ndarray, resize_h: int = 720, en_scale: float = 1.08,
                     top_bottom_padding_rate: float = 0.05) -> list:
    """

    Args:
        image_gray(np.ndarray): Image
        resize_h(int): Height
        en_scale(float): Scale
        top_bottom_padding_rate(float): padding rate

    Returns:
        List of probable plate numbers

    """
    path = "..//..//resources//cascade.xml"
    watch_cascade = cv2.CascadeClassifier(os.path.realpath(path))
    if top_bottom_padding_rate > 0.2:
        print("error:top_bottom_padding_rate > 0.2:", top_bottom_padding_rate)
        exit(1)
    height = image_gray.shape[0]
    padding = int(height * top_bottom_padding_rate)
    scale = image_gray.shape[1] / float(image_gray.shape[0])
    image = cv2.resize(image_gray, (int(scale * resize_h), resize_h))
    image_color_cropped = image[padding:resize_h - padding, 0:image_gray.shape[1]]
    image_gray = cv2.cvtColor(image_color_cropped, cv2.COLOR_RGB2GRAY)
    watches = watch_cascade.detectMultiScale(image_gray, en_scale, 2, minSize=(36, 9), maxSize=(36 * 40, 9 * 40))
    cropped_images = []
    for (x, y, w, h) in watches:
        x -= w * 0.14
        w += w * 0.28
        y -= h * 0.15
        h += h * 0.3

        cropped = cropImage(image_color_cropped, (int(x), int(y), int(w), int(h)))
        cropped_images.append(cropped)

    return cropped_images


def resizeImage(img: np.ndarray) -> Image.Image:
    """

    Args:
        img(np.ndarray): Image

    Returns:
        Resized image Image.Image

    """
    im = Image.fromarray(img)
    length_x, width_y = im.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    im_resized = im.resize(size, Image.ANTIALIAS)

    return im_resized


def secondCrop(img: np.ndarray) -> np.ndarray:
    """

    Args:
        img(array): Image

    Returns:
        Second cropped image np.ndarray


    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]
    if len(areas) != 0:
        max_index = np.argmax(areas)
        cnt = contours[max_index]
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        secondCropped = img[y:y + h, x:x + w]
    else:
        secondCropped = img

    return secondCropped


def recognise(image: str) -> str:
    """

    Args:
        image (str): Image path

    Returns:
        Detected number plate string

    """
    img = cv2.imread(image)
    images = detectPlateRough(image_gray=img, resize_h=img.shape[0], top_bottom_padding_rate=0.1)

    for plate in images:
        cv2.imwrite("plate.png", plate)
        resizedImage = np.asarray(resizeImage(plate))
        croppedImage = secondCrop(resizedImage)
        gray_plate = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
        plate_blur = cv2.blur(gray_plate, (5, 5))
        plate_blur = cv2.blur(plate_blur, (5, 5))
        conf = '-l eng --oem 3 --psm 8'
        text = pytesseract.image_to_string(plate_blur, config=conf)
        if len(text) >= 10:
            text = text[-10:]
            space1 = text.find(" ")
            space2 = text.find(" ", space1 + 1)
            index1 = space1 - 2
            index2 = space2 + 4
            platenumber = text[index1:index2]
        else:
            print("Number plate not found")

    return platenumber
