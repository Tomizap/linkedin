import time

from selenium.webdriver.common.keys import Keys

from selenium_driver import SeleniumDriver
from selenium_sequence import Sequence
from .application import application


class LinkedIn:

    def __init__(self, config, driver=None):
        print('-> create LinkedIn bot')
        self.config = config
        self.driver = SeleniumDriver() if driver is None else driver
        return

    def login(self):
        print('-> login')
        time.sleep(1)
        while not self.driver.is_attached('body > .application-outlet *'):
            self.driver.get('https://linkedin.com')
            if self.driver.is_attached('#session_key'):
                self.driver.write('#session_key', self.config['user']['email'])
                self.driver.write('#session_password',
                                  self.config['user']['password'])
                self.driver.click("#main-content .sign-in-form__footer--full-width > button")
                time.sleep(3)
            time.sleep(1)
            self.driver.captcha()
        print('logged in !')
        return self.driver

    # ---------------- JOB APPLICATION -------------------- #

    class Jobs:

        def __init__(self, driver=None, url=None) -> None:
            print('-> init Jobs')
            if driver is None:
                self.driver = SeleniumDriver()
            else:
                self.driver = driver
            # self.driver = SeleniumDriver() if driver is None else driver
            # self.driver.get(url) if url is not None else ''
            if url is not None:
                self.driver.get(url)
            # url = f"https://www.linkedin.com/jobs/search/?currentJobId=3620288377&f_AL=true&f_JT=I&keywords=seo&location=Ile-de-France"
            # filename = "testing"
            # sequence = Sequence(url=url, driver=self.driver)
            # sequence.play()
            # self.data = sequence.data
            self.data = []
            return

        def apply(self, url=None):
            print('-> apply')
            self.driver.get(url) if url is not None else ''
            sequence = Sequence(driver=self.driver)
            sequence.play()
            print(sequence.data)
            self.data.extend(sequence.data)
            application(self.driver).run()
            return

        def multi_apply(self, urls=None):
            print('-> multi_apply')
            # print('apply')
            if urls is None:
                print('find urls')
                sequence = Sequence(driver=self.driver, sequence={
                    ":loop": {
                        "pagination": 1,
                        # "pagination": 'div.jobs-search-results-list__pagination li:last-child',
                        "listing": {
                            ":execute_script": 'document.querySelector("div.jobs-search-results-list").scroll(0, 999999)',
                            ":get:all": {"property": "href",
                                        "selector": 'div.artdeco-entity-lockup__title > a.job-card-container__link'},
                            ":click": 'div.jobs-search-results-list__pagination li.selected + li',
                        },
                        "deep": False
                    }
                })
                sequence.play()
                print(sequence.data)
                urls = sequence.data
            print(urls)
            for uri in urls:
                self.apply(url=uri)
            return self.data

        def contact_job_recruiters(self):
            return self.data
