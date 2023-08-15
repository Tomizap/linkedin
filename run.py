import time
from pprint import pprint

from linkedin import LinkedIn

config = {
    "url" : 'https://www.linkedin.com/jobs/search/?currentJobId=3671928543&geoId=105015875&keywords=rh&location=France&refresh=true',
    "user": {
        "email": "zaptom.pro@gmail.com",
        "password": "Tom01032000",
        # "phone": "066577418"
    },
    "automnation": {
        "_id": ""
    },
    'setting': {
        'excluded_keywords': [],
        'excluded_companies': ['iscod', 'aston'],
        'presets': {
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
