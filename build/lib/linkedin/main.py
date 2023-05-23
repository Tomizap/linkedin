import time

from selenium.webdriver.common.keys import Keys

from selenium_driver import selenium_driver
from selenium_scrapper import selenium_scrapper
from .application import application as linkedin_application


class LinkedIn:

    def __init__(self, config, driver=None):
        self.config = config
        if driver is None:
            self.driver = selenium_driver()
        else:
            self.driver = driver
        return

    def login(self):
        print('login')
        time.sleep(1)
        while not self.driver.is_attached('body > .application-outlet *'):
            self.driver.get('https://linkedin.com')
            if self.driver.is_attached('#session_key'):
                self.driver.write('#session_key', self.config['user']['email'])
                self.driver.write('#session_password',
                                  self.config['user']['password'])
                self.driver.write('#session_password', Keys.ENTER)
                time.sleep(3)
            time.sleep(1)
            self.driver.captcha()
        print('logged in !')
        return self.driver

    # ---------------- POSTS -------------------- #

    class posts:

        def __init__(self, driver=None, url=None, data=None) -> None:
            self.driver = driver
            if url is not None:
                self.driver.get(url)
            if data is None:
                data = selenium_scrapper(driver=self.driver)
            self.data = data
            return

        def post(self, url=None, setting={}):
            return self.data

        def like(self, url=None, setting={}):
            return self.data

        def comment(self, url=None, setting={}):
            return self.data

    # ---------------- CONTACTS -------------------- #

    class contacts:

        def __init__(self, driver=None, url=None, data=None) -> None:
            self.driver = driver
            if url is not None:
                self.driver.get(url)
            if data is None:
                data = selenium_scrapper(driver=self.driver)
            self.data = data
            return

        def invite(self, url=None, setting={}):
            if url is not None:
                self.driver.get(url)
            print('invite')
            if len(self.data) > 0:
                for item in self.data:
                    self.driver.get(item['contact_link'])
                    for item in self.driver.find_elements('.pvs-profile-actions button'):
                        if 'invite' in item.getProperty('data-label').lower() or "connect" in item.getProperty('innexText').lower():
                            item.click()
                            self.driver.click('.artdeco-modal__content button:lastchild')
                            break
            return self.data

        def message(self, url=None, setting={}):
            return self.data

    # ---------------- GROUPS -------------------- #

    class groups:

        def __init__(self, driver=None, url=None, data=None) -> None:
            self.driver = driver
            if url is not None:
                self.driver.get(url)
            if data is None:
                data = selenium_scrapper(driver=self.driver)
            self.data = data
            return

        def join(self, url=None, setting={}):
            return self.data

    # ---------------- JOB APPLICATION -------------------- #

    class application:

        def __init__(self, driver=None, url=None, data=None) -> None:
            self.driver = driver
            if url is not None:
                self.driver.get(url)
            if data is None:
                data = selenium_scrapper(driver=self.driver)
            self.data = data
            return

        def apply(self, url=None, setting={}):
            if url is not None:
                self.driver.get(url)
            print('apply')
            if len(self.data) > 0:
                for item in self.data:
                    linkedin_application(
                        self.driver, setting).run(item['job_link'])
            return self.data

        def contact_recruiters(self):
            return self.data
