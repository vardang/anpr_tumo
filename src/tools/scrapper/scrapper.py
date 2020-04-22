import requests
from selenium import webdriver
import os


def download_image(src: str, path: str):
    """
    Downloads the image to the given path

    Args:
        src (str): Image source url
        path (str): Destination path where to save the image

    Returns:

    """
    name = src.split('/')[-1]
    r = requests.get(src)
    with open(os.path.join(path, name), 'wb') as outfile:
        outfile.write(r.content)


# Opens chrome
driver = webdriver.Chrome()
# driver.maximize_window()

# Navigates to the page
driver.get(
    'https://auto.am/search/passenger-cars?q={%22category%22:%221%22,%22page%22:%221%22,%22sort%22:%22latest%22,%22layout%22:%22list%22,%22user%22:{%22dealer%22:%220%22,%22id%22:%22%22},%22year%22:{%22gt%22:%221911%22,%22lt%22:%222021%22},%22usdprice%22:{%22gt%22:%220%22,%22lt%22:%22100000000%22},%22custcleared%22:%221%22,%22mileage%22:{%22gt%22:%2210%22,%22lt%22:%221000000%22}}')

# Finds the search result and selects each element
search_result = driver.find_element_by_css_selector("#search-result")
cards = search_result.find_elements_by_class_name("card")

# Directory path where to save the images
base_path = os.path.join(os.getcwd(), 'cars')

# Iterate over results to extract meta info and download the images
for card in cards:

    # Finds and extracts car year, name and model
    car = card.find_element_by_css_selector('span.card-title.bold').text.split(' ')

    car_year = car[0]
    car_name = car[2]
    car_model = '_'.join(car[3:])

    # Finds img tag by class name
    image_elements = card.find_elements_by_class_name("flipimg")
    if len(image_elements) == 0:
        print(f"Image haven't been found for {car_year} {car} {car_model}")
        continue

    image_element = image_elements[0]

    # Get images source url from attributes
    base_img = image_element.get_attribute('src')
    hover_img = image_element.get_attribute('data-hover-img')

    # Create hierarchic directory structure to download the images
    dir_path = os.path.join(base_path, car_name, car_model, car_year)
    is_failed = False

    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError:
            print("Creation of the directory %s failed" % dir_path)
            is_failed = True

    # Downloads the images to the corresponding path
    if not is_failed:
        download_image(base_img, dir_path)
        download_image('https://auto.am/' + hover_img, dir_path)

# Closes chrome
driver.close()
