import time
from pprint import pprint

from linkedin import LinkedIn

config = {
    "user": {
        "email": "zaptom.pro@gmail.com",
        "password": "Tom01032000",
        "phone": "066577418"
    },
}

linkedin = LinkedIn(config)
driver = linkedin.login()

# ========== JOBS ============ #

url = f"https://www.linkedin.com/jobs/search/keywords=seo&location=Clichy%2C%20%C3%8Ele-de-France%2C%20France&refresh=true"
data = linkedin.application(driver=driver, url=url).apply()

# ============= CONTACTS ==================== #

# url = f"https://www.linkedin.com/search/results/people/?keywords=recruteur"
# feature = linkedin.contacts(driver=driver, url=url)
# feature.invite()
# feature.contact()

# ============== GROUPS ================= #

pprint(data)
time.sleep(999999)
