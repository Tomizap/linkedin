import time
from pprint import pprint

from linkedin import LinkedIn

config = {
    "_id": "",
    "urls" : ["https://www.linkedin.com/jobs/search/?currentJobId=3671928543&geoId=105015875&keywords=rh&location=France&refresh=true"],
    "user": {
        "email": "zaptom.pro@gmail.com",
        "password": "Tom01032000",
    },
    "setting": {
        "excluded_keywords": [],
        "excluded_companies": ['iscod', 'aston'],
        "infinite": True,
        "scrap": False,
        "presets": {
            "phone": "066577418",
            "name": "tom",
            "nom": "tom",
            "pays": "fr",
            "mail": "zaptom.pro@gmail.com",
            "linkedin": "https://www.linkedin.com/in/tom-zapico/",
        }
    }
}

bot = LinkedIn(config)

bot.multi_apply()

pprint(bot.data)

time.sleep(999999)
