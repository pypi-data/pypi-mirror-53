from canvasscraper.objects.Course import Course
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from canvasscraper.RegexCheck import Regex


# TODO: Will probably want to break this down further, permitting scrap of individual courses/pages (of course)
# TODO: you can current just provide the functions with a single index array.
class LinkScraper:

    def __init__(self, base_url, driver):
        self.base_url = base_url
        self.driver = driver
        self.courses = []
        self.has_class_list = False
        self.has_page_list = False
        self.has_vid_list = False

    def get_class_list(self):
        url = self.base_url + "/courses"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.title_contains("Courses"))
        print("=========================\n"
              "Retrieving Active Courses\n"
              "=========================")
        for course in self.driver.find_elements_by_tag_name('a'):
            self.__if_class_get_class(course, self.courses)
        self.has_class_list = True

    @staticmethod
    def __if_class_get_class(link, arr):
        if "/courses/" in link.get_attribute('href'):
            print(f"Found class: {link.get_attribute('title')[0:7]}")
            arr.append(Course(link.get_attribute('title')[0:7], link.get_attribute('href')))

    def get_page_list(self):
        for course in self.courses:
            self.__get_pages(course)
        self.has_page_list = True

    def __get_pages(self, course_obj):
        print("=============================================\n"
              "Retrieving Course Pages for: " + course_obj.name + "  \n"
              "=============================================")
        url = course_obj.url + "/modules"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.title_contains(course_obj.name))
        for page in self.driver.find_elements_by_tag_name('a'):
            self.__if_page_get_page(page, course_obj)

    @staticmethod
    def __if_page_get_page(page, course_obj):
        if "for-nvda" in page.get_attribute('class'):
            if page.get_attribute('aria-label') is not "":
                print(f"Found Page at: {page.get_attribute('href')}")
                course_obj.add_page(page.get_attribute('aria-label'), page.get_attribute('href'))

    def get_vid_list(self):
        regex_checker = Regex()
        for course in self.courses:
            print("================================\n"
                  f"Searching {course.name} Pages for Videos \n"
                  "================================")
            for name, obj in course.pages.items():
                count = 0
                print('___________________________\n'
                      f'Currently Checking: {obj.course} {name}')
                self.driver.get(obj.url)
                iframes = self.driver.find_elements_by_xpath("//iframe")
                for frame in iframes:
                    if regex_checker.is_valid(frame.get_attribute('src')):
                        count += 1
                        print(f"Found Video at: {frame.get_attribute('src')}")
                        obj.add_vid(count, frame.get_attribute('src'))
        self.has_vid_list = True

    def return_data(self):
        return self.courses

