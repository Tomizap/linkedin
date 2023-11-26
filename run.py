from linkedin import LinkedIn
from tzmongo import mongo

config = {
#   "_id": "",
  "name": "Auto Apply Indeed Test",
  # "description": "",
  # "website": "indeed.com",
  # "message": "",
  "urls": [
    f"https://www.linkedin.com/jobs/search/?currentJobId=3757161933&f_AL=true&f_JT=I&geoId=104246759&keywords=marketing&location=%C3%8Ele-de-France%2C%20France&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R"
  ],
  "user": {
    "email": "reinofabrice@gmail.com",
    "password": "Paris75017",
    "cookies": [{'name': 'li_at', 'value': 'AQEDAS3LRfIBhUA3AAABi-K3K7IAAAGML2cf-U0AvSfJpJ7UKN3E1dcURuf2WVsAcqmNqUBwfY_mowGKw5iCp_h8GTfXaUxpFxvDvsKAJfRzNQVWI-HR_3u9Bv7ZS_3m1a9v7CArQbIgeHq09u2v_s9F'}]
  },
  "setting": {
    "excluded_keywords": [
      'formation',
      'bts',
      "diplome",
      "bachelor"
    ],
    "excluded_companies": [
      "iscod",
      "aston",
      "talia.fr",
      "institut de management",
      "formation",
      "ima business",
      "iag",
      "enaco",
      "institut des langues",
      "studi cfa",
      "talentis",
      "propulsup",
      "france métiers",
      "institut des compétences",
      "f2i",
      "groupe alternance",
      "school",
      "école",
      "education",
      "ecole",
      "cfa",
      "campus",
      "recrutement"
    ],
    "infinite": True,
    "scrap": False,
    "presets": {
      "code pays": "+33",
      "phone": "0665774189",
      "name": "Fabrice",
      "nom": "Fabrice",
      "pays": "fr",
      "mail": "reinofabrice@gmail.com",
      "city": 'Paris',
      "linkedin": "https://www.linkedin.com/in/tom-zapico/"
    }
  },
  "data": []
}

bot = LinkedIn(config)
bot.application_loop()

# ga = mongo({
#     'collection': 'automnations',
#     "selector": {'name': "Auto Candidature"}
# })
# # print(ga)
# if ga['ok'] == True:
#     bot = LinkedIn(ga['data'][0])
#     bot.application_loop()
