import time

from selenium.webdriver.common.keys import Keys

from selenium_driver import SeleniumDriver
from selenium_sequence import Sequence
from .application import application


class LinkedIn:

    def __init__(self, config, driver=None):
        print('-> create LinkedIn bot')
        self.config = config
        self.data = []
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

    def apply(self, url=None):
        print('-> apply')
        self.login()

        self.driver.get(url) if url is not None else ''
        url = self.driver.current_url()

        application_ok = application(self.driver, self.config['setting']).run(url=url)

        item = {}
        if self.config['setting']['scrap']:
            sequence = Sequence(driver=self.driver)
            sequence.play()
            sequence.data
            print(sequence.data)
            item = sequence.data[0]
        item['url'] = url
        item['application_ok'] = application_ok

        self.data.extend([item.copy()])
        print(self.data)

        return item

    def multi_apply(self):
        print('-> multi_apply')
        self.login()

        urlIndex = -1
        try:
            while 1 == 1:
                
                print(self.config['urls'][urlIndex])
                self.driver.get(self.config['urls'][urlIndex])
                
                # print('find urls')
                print('scrapping ..')
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

                # print(sequence.data)
                # for url in sequence.data:
                #     url = url.split('?')[0]

                uris = sequence.data
                i = 0
                for uri in uris:
                    print(f"application {i} / {len(uris)} ")
                    i = i + 1
                    if self.apply(url=uri) is True:
                        print('Application Successful')
                
                
                urlIndex = urlIndex + 1
                if urlIndex > len(self.config['urls']):
                    if not self.config['setting']['infinite']:
                        break
                    else:
                        urlIndex = 0

                print('continue because infinite')

        except:
            print('Une erreur est survenue')

        return self.data

    # def contact_job_recruiters(self):
    #     return self.data
