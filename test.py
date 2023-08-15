from pprint import pprint
import time

from selenium_sequence import Sequence
from selenium_driver import SeleniumDriver
data = []

# --- TESTING ZONE ---

url = f"https://www.linkedin.com/jobs/search/?currentJobId=3620288377&f_AL=true&f_JT=I&keywords=seo&location=Ile-de-France"
filename = "testing"

sequence = Sequence(url=url, filename=filename, data=data, driver=driver)
sequence.play()

data = sequence.data
pprint(data)

time.sleep(9999)
