import time
from pprint import pprint
from bson import ObjectId
import urllib

from selenium.webdriver.common.keys import Keys
import pymongo

from selenium_driver import SeleniumDriver
from selenium_sequence import Sequence
from .application import application


def update_autoapply(id, update={}):
    client = pymongo.MongoClient("mongodb+srv://alterrecrut:Xw9SZ0QUmVhyWHmd@cluster0.qp93luo.mongodb.net/?retryWrites=true&w=majority")
    db = client["tools"]
    collection = db["automnations"]
    collection.update_one({"_id": ObjectId(id)}, update)


class LinkedIn:

    def __init__(self, config, driver=None):
        print('-> create LinkedIn bot')
        self.config = config
        self.config["_id"] = str(self.config.get('_id'))
        pprint(self.config)
        self.data = []
        self.driver = SeleniumDriver() if driver is None else driver
        auth = config['auth']
        print('-----------')
        print(auth)
        print(config['urls'][0])
        self.driver.get(config['urls'][0])
        if type(auth) is list:
            for cookie in auth:
                cookie = {'name': cookie.get('name'), 'value': cookie.get('value')}
                self.driver.add_cookie(cookie)
                self.driver.get(config['urls'][0])
        # elif type(auth) is str:
        #     if auth == 'indeed.com':
        #         pass
        #     if auth == 'pole-emploi.com':
        #         pass
        update_autoapply(self.config["_id"], {
            "$set": {
                "active": True,
                "status": "active",
                "message": "Initialisation ..."
            }
        })
        return

    # def login(self):
    #     print('-> login')
    #     update_autoapply(self.config["_id"], {
    #         "$set": {
    #             "message": "Connexion en cours ..."
    #         }
    #     })
    #     time.sleep(1)
    #     while not self.driver.is_attached('body > .application-outlet *'):
    #         self.driver.get('https://linkedin.com')
    #         if self.driver.is_attached('#session_key'):
    #             self.driver.write('#session_key', self.config['user']['email'])
    #             self.driver.write('#session_password',
    #                               self.config['user']['password'])
    #             self.driver.click("#main-content .sign-in-form__footer--full-width > button")
    #             time.sleep(3)
    #         time.sleep(1)
    #         self.driver.captcha()
    #     print('logged in !')
    #     update_autoapply(self.config["_id"], {
    #         "$set": {
    #             "message": "Connexion réussie !"
    #         }
    #     })
    #     return self.driver

    # ---------------- JOB APPLICATION -------------------- #

    def apply(self, url=None):
        print('-> apply')
        # self.login()

        # update_autoapply(self.config["_id"], {
        #     "$set": {
        #         "message": f"Application in progress ..."
        #     }
        # })

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
        item['url'] = url.split("?")[0]
        # item['ressourceId'] = urllib.parse.urlparse(item['url']).path.split('/')
        item['application_ok'] = application_ok

        if application_ok is True:
            update_autoapply(self.config["_id"], {
                "$inc": {
                    "result.success": 1
                }
            })

        self.data.extend([item.copy()])
        print(self.data)

        return item

    def multi_apply(self):
        print('-> multi_apply')
        # self.login()

        urlIndex = -1
        try:
            while 1 == 1:
                
                print(self.config['urls'][urlIndex])
                self.driver.get(self.config['urls'][urlIndex])

                update_autoapply(self.config["_id"], {
                    "$set": {
                        "message": "Scrapping ..."
                    }
                })
                
                # print('find urls')
                print('scrapping ..')
                sequence = Sequence(driver=self.driver, sequence={
                    ":loop": {
                        "pagination": 3,
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
                pprint(uris)
                # update_autoapply(self.config["_id"], {
                #     "$set": {
                #         "message": f"{len(uris)} urls founded"
                #     }
                # })

                i = 0
                for uri in uris:
                    print(f"application {i} / {len(uris)}")
                    update_autoapply(self.config["_id"], {
                        "$set": {
                            "message": f"Application {i} / {len(uris)} in progress ..."
                        },
                        "$inc": {
                            "result.attempt": 1
                        }
                    })
                    i = i + 1
                    if self.apply(url=uri) is True:
                        print('Application Successful')
                
                
                urlIndex = urlIndex + 1
                if urlIndex > len(self.config['urls']):
                    if not self.config['setting']['infinite']:
                        update_autoapply(self.config["_id"], {
                            "$set": {
                                "status": "inactif",
                                "active": False,
                                "message": "Le script est fini"
                            }
                        })
                        break
                    else:
                        urlIndex = 0

                print('continue because infinite')

        except Exception as e:
            update_autoapply(self.config['_id'], {
                "$set": {
                    "status": "inactif",
                    "active": False,
                    "message": "Une erreur est survenue: " + str(e)
                },
                "$inc": {
                    "result.error": 1
                }
            })
            print('Une erreur est survenue')

        return self.data

    # def contact_job_recruiters(self):
    #     return self.data
