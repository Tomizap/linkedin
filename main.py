from poleEmploi import PoleEmploie
from indeed import Indeed
from linkedin import LinkedIn


class AutoApply:

    def __init__(self, s):
        super(AutoApply, self).__init__()
        # self.indeed = Indeed(s, name="indeed")
        self.linkedin = LinkedIn(s, name="linkedin")
        # self.pole_emploie = PoleEmploie(s, name="pole-emploie")

    def start(self):
        
        # self.indeed.application_loop()
        self.linkedin.application_loop()
        # self.pole_emploie.application_loop()

    def end(self):
        pass


config = {
    "inputs": {
        "keywords": ['seo', 'webmarketing', 'wordpress', 'e-commerce'],
        "localization": "Ile-de-France",
        "excluded_keywords": ['stag'],
        "included_keywords": [],
        "contract_type": [],
        "remote": False,
        "mininum_salary": 0
    },
    "options": {
        "hide_jobs": False,
        "message_to_recruiter": False,
        "DEBUG": False,
        "headless": False,
        "infinite": True,
        "safe_mode": False
    },
    "presets": {
        "phone": "0665774180",
        "name": "Tom",
        "nom": "Tom",
        "pays": "fr",
        "mail": "zaptom.pro@gmail.com",
        "twitter": "https://twitter.com/tom_zapico",
        "linkedin": "https://www.linkedin.com/in/tom-zapico/",
        "internet": "https://tom-zapico.com"
    },
    "indeed": {
        "auth": {
            "mail": "t.zapico@ldeclic.fr",
            "password": "Tom01032000",
            "phone": "0665774180"
        },
        "preset": {}
    },
    "linkedin": {
        "auth": {
            "email": "zaptom.pro@gmail.com",
            "password": "Tom01032000",
            "phone": "0665774180"
        },
        "preset": {}
    },
    "pole-emploie": {
        "auth": {
            "email": "TomZAP",
            "password": "Tom01032000.",
            "phone": "0665774180"
        },
        "preset": {}
    }
}
AutoApply(config).start()
