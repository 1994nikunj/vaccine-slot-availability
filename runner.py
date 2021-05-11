__Author__ = ' NIKUNJ SHARMA '
__Date__ = '   21th May 2021 '

from selenium import webdriver


class Scrapper(object):
    URL = "https://www.cowin.gov.in/home"
    DRIVER_PATH = 'C:\\Python39\\Lib\\site-packages\\chromedriver\\chromedriver.exe'

    def __init__(self):
        self.driver = None
        self.page_source = None

        # Caller methods
        self.init_driver()
        self.get_page_source()

    def init_driver(self):
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.headless = True

        # initializing the chrome driver object
        self.driver = webdriver.Chrome(executable_path=self.DRIVER_PATH,
                                       options=options)

    def get_page_source(self):
        # making request to the url
        self.driver.get(url=self.URL)

        # fetching the html page source
        self.page_source = self.driver.page_source
        print(self.page_source)

        self.start_extracting()

        # Exit the chrome-driver
        self.exit_chromedriver()

    def start_extracting(self):
        return

    def exit_chromedriver(self):
        self.driver.quit()


def simpler_implementation():
    from selenium.webdriver.chrome.options import Options

    url = "https://www.cowin.gov.in/home"
    driver = 'C:\\Python39\\Lib\\site-packages\\chromedriver\\chromedriver.exe'

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path=driver, options=options)
    driver.get(url=url)
    print('Page Title:', driver.title)
    print('Page Source:', driver.page_source)

    driver.quit()


if __name__ == '__main__':
    simpler_implementation()
    # Scrapper()
