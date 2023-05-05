import random
import threading
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class PoleEmploie(threading.Thread):

    def __init__(self, setting, name=None):
        super(PoleEmploie, self).__init__(name=name)
        self.setting = setting
        self.user = setting['pole-emploie']["auth"]
        self.keywords = self.setting['inputs']['keywords']
        self.list_jobs_url = f"https://candidat.pole-emploi.fr/offres/recherche?motsCles={self.keywords[random.randint(0, len(self.keywords)-1)]}&offresPartenaires=true"
        options = Options()
        options.add_experimental_option("detach", True)
        if self.setting['options']['headless']:
            options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        return

    # ---------------- LOGIN -------------------- #

    def login(self):
        self.driver.get("https://candidat.pole-emploi.fr/espacepersonnel/")
        self.driver.maximize_window()
        for i in range(5):
            try:
                self.driver.find_element(By.CSS_SELECTOR, '#footer_tc_privacy_button_2').click()
            except:
                time.sleep(3)
        time.sleep(5)
        identifier = self.driver.find_elements(By.CSS_SELECTOR, '#identifiant')
        while len(identifier) == 0:
            time.sleep(5)
            identifier = self.driver.find_elements(By.CSS_SELECTOR, '#identifiant')
        self.driver.find_element(By.CSS_SELECTOR, '#identifiant').send_keys(self.user['email'])
        self.driver.find_element(By.CSS_SELECTOR, '#submit').click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, '#password').send_keys(self.user['password'])
        self.driver.find_element(By.CSS_SELECTOR, '#submit').click()
        time.sleep(2)

    # ---------------- SCRAPPER -------------------- #

    # ---------------- JOB APPLICATION -------------------- #

    def application_exit(self):
        p = self.driver.window_handles[0]
        self.driver.close()
        self.driver.switch_to.window(p)

    def application(self):
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
        # Check If already Apply
        time.sleep(2)
        if len(self.driver.find_elements(By.CSS_SELECTOR, 'section .validation button')) == 0:
            # print('Already Applied')
            self.application_exit()
            return
        # Profil
        buttons = self.driver.find_elements(By.CSS_SELECTOR, '#contents bloc-profil .container-action-selectionner label')
        if len(buttons) > 0:
            buttons[0].click()
        # Submit
        self.driver.find_element(By.CSS_SELECTOR, 'bloc-coordonnees form label').click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, 'section .validation button.btn-primary').click()
        time.sleep(2)
        print("Pole Emploie: +1 Application")
        # Exit
        self.application_exit()

    def application_loop(self):
        self.login()
        # Go to Job Listing
        self.driver.get(self.list_jobs_url)
        time.sleep(7)
        for i in range(5):
            try:
                self.driver.find_element(By.CSS_SELECTOR, 'ul.result-list > li a').click()
            except:
                time.sleep(7)
        time.sleep(2)
        # loop
        while 1 == 1:
            time.sleep(3)
            self.driver.find_element(By.CSS_SELECTOR, '#detail-apply').click()
            time.sleep(2)
            begin_apply = self.driver.find_elements(By.CSS_SELECTOR, '#contactZone > .dropdown-contact-btn > a')
            if len(begin_apply) == 0:
                # print('External Application')
                next_button = self.driver.find_elements(By.CSS_SELECTOR, '#PopinDetails .modal-details-pager button.next')
                if len(next_button) > 0:
                    next_button[0].click()
                else:
                    self.driver.get(self.list_jobs_url)
                continue
            begin_apply[0].click()
            time.sleep(2)
            self.application()
            time.sleep(2)
            self.driver.find_element(By.CSS_SELECTOR, '#PopinDetails .modal-details-pager button.next').click()
