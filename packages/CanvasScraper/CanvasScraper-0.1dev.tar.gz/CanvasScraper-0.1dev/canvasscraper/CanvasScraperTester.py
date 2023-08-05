import sys
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.support import expected_conditions as EC
from canvasscraper.LinkScraper import LinkScraper
from canvasscraper.fileops.DirMaker import DirMaker
from canvasscraper.fileops.URLLogger import URLLogger


AUTHOR = "stucampbell.git@gmail.com"

"""
"""
"""
SELENIUM PACKAGES AND A WEBDRIVER ARE REQUIRED ALSO, THE DOWNLOAD FUNCTION IS DESIGNED 
TO WORK WITH YOUTUBE-DL, BUT THE SCRIP DOES PRODUCE A STANDARDIZED LIST OF VIDEO NAMES 
AND LINKS YOU MAY BE ABLE TO FIND ANOTHER DOWNLOADER THAT WORKS FOR YOU.
"""
"""
"""
try:
    driver = webdriver.Chrome()
except SessionNotCreatedException:
    print("===========================================================================\n"
          "Chrome Version does not match driver version.  Please ensure they match. I \n"
          "will add some functionality here to select a path for different driver than\n"
          "what python had automatically retrieved.  For now just ensure that the right\n"
          "chromedriver is install in the root dir (CanvasScraper).                   \n"
          "https://sites.google.com/a/chromium.org/chromedriver/downloads             \n"
          "===========================================================================\n")
    driver = webdriver.Chrome('../chromedriver')

base_url = ""

# Testing new course/page/vid objects and Linkscraper functions
course_arr = []


# TODO: Maybe obscure the log-in details... all just plain text at the moment
def login():
    un = input("Enter username: ")
    pw = input("Enter password: ")
    sub = input("Enter school subdomain, [asu] by default: ")

    global base_url

# Left as modifiable given there are other schools in the world that probably use Canvas;
    if sub == "":
        sub = 'asu'

    base_url = "https://" + sub + ".instructure.com"
    url = base_url + "/login"

    driver.get(url)
    WebDriverWait(driver, 10).until(EC.title_contains("ASURITE Sign-In"))

    driver.find_element_by_id('username').send_keys(un)
    driver.find_element_by_id('password').send_keys(pw)
    driver.find_element_by_class_name('submit').click()

    WebDriverWait(driver, 10).until(EC.title_contains("Dashboard"))


def test_link_scraper():
    global course_arr
    link_scraper = LinkScraper(base_url, driver)

    print("\nTesting Class Finder\n")
    if not link_scraper.has_class_list:
        link_scraper.get_class_list()

    print("\nTesting Page Finder\n")
    if link_scraper.has_class_list and not link_scraper.has_page_list:
        link_scraper.get_page_list()

    print("\nTesting Video Link Finder\n")
    if link_scraper.has_class_list and link_scraper.has_page_list and not link_scraper.has_vid_list:
        link_scraper.get_vid_list()

    print("\nTesting Return of Objects\n")
    for course in link_scraper.return_data():
        course_arr.append(course)
    for course in course_arr:
        course.print_info()


def test_dir_maker():
    global course_arr
    print("\nTesting DirMaker\n")
    saver = DirMaker()
    saver.save_all(course_arr)


def test_URL_logger():
    global course_arr
    print("\nTesting URLLogger\n")
    logger = URLLogger(course_arr)
    logger.write_URLs_to_file()


def user_quit():
    driver.quit()
    sys.exit("User initiated Quit")


# TODO: Finish user interface options to include loading an existing file, selection of classes to download, etc.
def main():
    print("Functions currently commented out for testing purposes.")
    # login()
    # test_link_scraper()
    # test_dir_maker()
    # test_URL_logger()
    # user_quit()


if __name__ == '__main__':
    main()
