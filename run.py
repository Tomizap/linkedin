from linkedin import LinkedIn


class AutoApply:

    def __init__(self, s):
        super(AutoApply, self).__init__()
        self.linkedin = LinkedIn(s, name="linkedin")

    def start(self):
        self.linkedin.application_loop()

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
        "minium_salary": 0
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
    "user": {
        "email": "zaptom.pro@gmail.com",
        "password": "Tom01032000",
        "phone": "0665774180"
    }
}
AutoApply(config).start()