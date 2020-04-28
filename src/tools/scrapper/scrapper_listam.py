import os
import requests
from selenium import webdriver


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


driver = webdriver.Chrome()

base_path = os.path.join(os.getcwd(), 'cars')
current_url = "https://www.list.am/category/23"


def getNextPage():
    """
    Gets next page and downloads all car images from current page
    """
    car_urls = []
    elems_car = driver.find_elements_by_css_selector(".gl [href]")
    for element in elems_car:
        car_urls.append(element.get_attribute('href'))

    for url in car_urls:
        driver.get(url)
        try:
            car_images = driver.find_element_by_class_name("t")
            for car in car_images.find_elements_by_tag_name("div"):
                car.click()

            divs = driver.find_element_by_class_name("p")
            attributes = driver.find_element_by_id("attr")
            tt = attributes.find_elements_by_class_name("t")
            ii = attributes.find_elements_by_class_name("i")
            car_year = None
            car_name = None
            car_model = None

            for i, t in enumerate(tt):
                if t.text == "Տարի":
                    car_year = "".join([c for c in ii[i].text if c.isalpha() or c.isdigit() or c == ' ']).strip()
                if t.text == "Տեսակ":
                    car_name = "".join([c for c in ii[i].text if c.isalpha() or c.isdigit() or c == ' ']).strip()
                if t.text == "Մոդել":
                    car_model = "".join([c for c in ii[i].text if c.isalpha() or c.isdigit() or c == ' ']).strip()

            for div in divs.find_elements_by_tag_name("div"):
                images = div.find_elements_by_tag_name("img")

                for image in images:

                    src = image.get_attribute("src")
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
                        download_image(src, dir_path)
        except Exception as err:
            print("Not found attribute car_name, car_model or car_year .")
            print(err)

            pass

    global current_url
    driver.get(current_url)
    elems = driver.find_elements_by_css_selector(".dlf [href]")
    for elem in elems:
        if elem.text == "Հաջորդը >":
            current_url = elem.get_attribute("href")
            elem.click()


def scrapper(page_count: int):
    """

    Args:
        page_count(int): Page count int <= 250
    Choose from how many pages download car images
    """
    for x in range(page_count):
        driver.get(current_url)
        getNextPage()


# Choose page_count less than 250
scrapper(50)
driver.quit()
