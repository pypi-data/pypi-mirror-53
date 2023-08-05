import sys
import pyderman as dr
from selenium.webdriver.chrome import webdriver as ch
from selenium.webdriver.firefox import webdriver as ff
from selenium.webdriver.phantomjs import webdriver as pjs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import SessionNotCreatedException
from canvasscraper.LinkScraper import LinkScraper
from canvasscraper.fileops.DirMaker import DirMaker
from canvasscraper.fileops.URLLogger import URLLogger


AUTHOR = "stucampbell.git@gmail.com"


def __browser_select():

    browsers = {'1': 'Chrome',
                '2': 'Firefox',
                '3': 'Safari',
                '4': 'Edge',
                '5': 'IE',
                '6': 'PhantomJS',
                '10': 'Quit',
                }

    print("=====================================================\n"
          "Please select your system Browser:                   \n"
          "=====================================================\n")
    for key, choice in browsers.items():
        print(f"{key}) {choice}")
    pick_em = input()

    if pick_em is '10':
        sys.exit("User elected to quit")
    elif pick_em is '6':
        path = dr.install(browser=dr.phantomjs, file_directory='./lib/', verbose=True, chmod=True, overwrite=False,
                          version=None, filename=None, return_info=False)
        return path, pick_em
    elif pick_em is '5':
        __get_out()
    elif pick_em is '4':
        __get_out()
    elif pick_em is '3':
        __get_out()
    elif pick_em is '2':
        path = dr.install(browser=dr.firefox, file_directory='./lib/', verbose=True, chmod=True, overwrite=False,
                          version=None, filename=None, return_info=False)
        return path, pick_em
    elif pick_em is '1':
        path = dr.install(browser=dr.chrome, file_directory='./lib/', verbose=True, chmod=True, overwrite=False,
                          version=None, filename=None, return_info=False)
        return path, pick_em
    else:
        print("No valid selections")
        return None, None


def __get_out():
    print("You're a Software Engineering student... you should know better.")
    sys.exit("Program refuses to work with a user with such poor judgement.  Exiting.")


def __set_driver(path, choice):
    if choice is '1':
        try:
            print("grabbed chromedriver")
            return ch.WebDriver(executable_path=path)
        except SessionNotCreatedException:
            __exception_print('Chrome', 'ChromeDriver', 'https://chromedriver.chromium.org/downloads')
    elif choice is '2':
        try:
            print("grabbed geckodriver")
            return ff.WebDriver(executable_path=path)
        except SessionNotCreatedException:
            __exception_print('Firefox', 'GeckoDriver', 'https://github.com/mozilla/geckodriver/releases')
    elif choice is '6':
        try:
            print("grabbed phantomjsdriver")
            return pjs.WebDriver(executable_path=path)
        except SessionNotCreatedException:
            __exception_print('PhantomJS', 'Headless', 'https://phantomjs.org/download.html')
    else:
        print("===========================================================================\n"
              "No Appropriate webdriver found!!!!!!                                       \n"
              "===========================================================================\n")
        sys.exit(1)


def __exception_print(browser, driver, link):
    print(f"============================================================================\n"
          f"{browser} Version does not match driver version.  Please ensure they match. \n"
          f"For now just ensure that the right {driver} version is install in the       \n"
          f"./CanvasScraper/canvasscraper/lib/                                          \n"
          f"{browser} Driver Download Link: {link}                                      \n"
          f"============================================================================\n")


# TODO: Maybe obscure the log-in details... all just plain text at the moment
def __login(driver):

    un = input("Enter username: ")
    pw = input("Enter password: ")
    sub = input("Enter school subdomain, [asu] by default: ")

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

    print(f"{driver.title} - {driver.current_url}")

    return base_url


def __test_link_scraper(driver, url):

    course_arr = []

    link_scraper = LinkScraper(url, driver)

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


def __test_dir_maker(course_arr):
    print("\nTesting DirMaker\n")
    saver = DirMaker()
    saver.save_all(course_arr)


def __test_URL_logger(course_arr):
    print("\nTesting URLLogger\n")
    logger = URLLogger(course_arr)
    logger.write_URLs_to_file()


def __user_quit(driver):
    print("Quitting...")
    driver.quit()
    sys.exit("User initiated Quit")


# TODO: Finish user interface options to include loading an existing file, selection of classes to download, etc.
def main():
    # print("Functions currently commented out for testing purposes.")
    driver_path, browser = __browser_select()
    print(driver_path, browser)
    driver = __set_driver(driver_path, browser)
    base_url = __login(driver)
    print(f"Base URL Recroded as: {base_url}")
    # __test_link_scraper()
    # __test_dir_maker()
    # __test_URL_logger()
    __user_quit(driver)


if __name__ == '__main__':
    main()
