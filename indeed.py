import random
import threading
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class Indeed(threading.Thread):

    def __init__(self, setting, name=None):
        super(Indeed, self).__init__(name=name)

        self.setting = setting

        self.user = setting['indeed']["auth"]
        self.inputs = self.setting['inputs']
        self.options = self.setting['options']
        self.presets = self.setting['presets']

        options = Options()
        options.add_experimental_option("detach", True)
        # options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        return

    def find_element(self, selector):
        return self.driver.find_element(By.CSS_SELECTOR, selector)

    def find_elements(self, selector):
        return self.driver.find_elements(By.CSS_SELECTOR, selector)

    # ---------------- LOGIN -------------------- #

    def pass_captcha(self):
        time.sleep(5)
        if len(self.driver.find_elements(By.CSS_SELECTOR, ".pass-Captcha > *")) > 0:
            for i in range(15):
                try:
                    print(self.driver.find_element(By.CSS_SELECTOR, ".pass-Captcha #a11y-label").get_property('innerText').lower())
                    if "vérifié" in self.driver.find_element(By.CSS_SELECTOR, ".pass-Captcha #a11y-label").get_property('innerText').lower():
                        print('try captcha')
                        time.sleep(2)
                    else:
                        break
                except:
                    time.sleep(3)
            return True
        else:
            return False

    def login(self):
        self.driver.get('https://secure.indeed.com/auth')
        time.sleep(3)
        # Accept Cookies
        self.driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler").click()
        # Fill Email
        for i in range(15):
            try:
                self.driver.find_element(By.CSS_SELECTOR, "#emailform input").send_keys(self.user['email'])
                self.driver.find_element(By.CSS_SELECTOR, "#emailform button").click()
                break
            except:
                time.sleep(2)
        if self.pass_captcha():
            for i in range(15):
                try:
                    self.driver.find_element(By.CSS_SELECTOR, "#emailform button").click()
                    break
                except:
                    time.sleep(2)
        # Fill Password
        for i in range(15):
            try:
                self.driver.find_element(By.CSS_SELECTOR, "#loginform span input").click()
                self.driver.find_element(By.CSS_SELECTOR, "#loginform span input").send_keys(self.user["password"])
                self.driver.find_element(By.CSS_SELECTOR, "#loginform > button").click()
                break
            except:
                time.sleep(2)
        if self.pass_captcha():
            for i in range(15):
                try:
                    self.driver.find_element(By.CSS_SELECTOR, "#loginform span input").click()
                    self.driver.find_element(By.CSS_SELECTOR, "#loginform span input").send_keys(self.user["password"])
                    self.driver.find_element(By.CSS_SELECTOR, "#loginform > button").click()
                    break
                except:
                    time.sleep(2)
        # SMS Verification
        for i in range(80):
            if len(self.driver.find_elements(By.CSS_SELECTOR, "#two-factor-auth-form")) > 0:
                time.sleep(2)
            else:
                break
        time.sleep(5)

    # ---------------- GENERAL -------------------- #

    def close_popup(self):
        time.sleep(3)
        if len(self.driver.find_elements(By.CSS_SELECTOR, "#mosaic-modal > *")) > 0:
            for i in range(5):
                try:
                    self.driver.find_element(By.CSS_SELECTOR, "#mosaic-modal > div > div > div.icl-Modal > div > button").click()
                    break
                except:
                    time.sleep(2)

    # ---------------- JOBS APPLICATION -------------------- #

    def application_close(self):
        if len(self.driver.window_handles) > 1:
            p = self.driver.window_handles[0]
            self.driver.close()
            self.driver.switch_to.window(p)

    def application_exit(self):
        try:
            button = self.driver.find_elements(By.CSS_SELECTOR,
                                               "#ia-container .ia-Navigation-exit.css-7pkb4x.eu4oa1w0 button")
            if len(button) > 0:
                button[0].click()
            time.sleep(2)
            button = self.find_elements(
                ".css-mq5q72.eu4oa1w0 > div.css-m05cy0.eu4oa1w0 > div.css-13hn6x1.eu4oa1w0 > button.css-r6nywx.e8ju0x51")
            if len(button) > 0:
                button[0].click()
            time.sleep(2)
        except:
            pass
        self.application_close()
        time.sleep(2)

    def application_end(self):
        time.sleep(5)
        if len(self.find_elements(".ia-PostApply-footer > #returnToSearchButton")) == 0:
            try:
                add_cl_button = self.driver.find_elements(By.CSS_SELECTOR, "#additional_links_section_empty-documents")
                if len(add_cl_button) > 0:
                    add_cl_button[0].click()
                    time.sleep(2)
                    self.driver.find_element(By.CSS_SELECTOR, "#write-cover-letter-selection-card").click()
                    time.sleep(2)
                    self.driver.find_element(By.CSS_SELECTOR, "#ia-container .ia-BasePage-footer button").click()
                    time.sleep(2)
                time.sleep(2)
                self.driver.find_element(By.CSS_SELECTOR, "#ia-container .ia-BasePage-footer button").click()
                time.sleep(2)
                print('Linkedin: +1 application')
            except:
                pass
        self.application_close()
        time.sleep(2)

    def application_is_ended(self):
        if len(self.driver.find_elements(By.CSS_SELECTOR, "#ia-container .ia-Review, .ia-PostApply-footer > #returnToSearchButton")) > 0:
            self.application_end()
            return True
        else:
            return False

    def application_has_error(self):
        if len(self.driver.find_elements(By.CSS_SELECTOR, 'svg.css-1bh9esk, #ia-container .ia-FileQuestion-errorText')) > 0:
            self.application_exit()
            return True
        else:
            return False

    def application_question(self):
        if len(self.driver.find_elements(By.CSS_SELECTOR, '#jobsearch-JapanPage .jobsearch-LeftPane')) > 0:
            return
        if self.application_is_ended():
            self.application_end()

        else:
            nb_question = self.driver.find_elements(By.CSS_SELECTOR, '#ia-container .ia-Questions-item')
            for i_question in range(len(nb_question) + 2):
                if self.application_has_error():
                    break
                time.sleep(2)
                # Checkbox Field
                q_input = self.driver.find_elements(By.CSS_SELECTOR, '#ia-container .ia-Questions-item:nth-child(' + str(i_question) + ') fieldset label')
                if len(q_input) > 0:
                    if "civilité" in 'q_label':
                        pass
                    else:
                        q_input[0].click()
                    continue
                # --------
                q_labels = self.driver.find_elements(By.CSS_SELECTOR, '#ia-container .ia-Questions-item:nth-child(' + str(i_question) + ') label > span > span > span')
                if len(q_labels) == 0:
                    continue
                q_label = q_labels[0].get_property('innerText').lower()
                print('q_label: ' + str(q_label))
                # Textarea Field
                q_input = self.driver.find_elements(By.CSS_SELECTOR, '#ia-container .ia-Questions-item:nth-child(' + str(
                    i_question) + ') textarea')
                if len(q_input) > 0:
                    if "date" in self.find_element(
                            '#ia-container .ia-Questions-item:nth-child(' + str(i_question) + ') label').get_property(
                            'innerText'):
                        q_input[0].send_keys("25/07/2023\n"
                                             "26/07/2023\n"
                                             "27/07/2023\n")
                    else:
                        q_input[0].send_keys('Oui')
                    continue
                # Select Field
                q_input = self.driver.find_elements(By.CSS_SELECTOR, '#ia-container .ia-Questions-item:nth-child(' + str(
                    i_question) + ') select')
                if len(q_input) > 0:
                    q_input[0].click()
                    time.sleep(1)
                    options = self.driver.find_elements(By.CSS_SELECTOR, '#ia-container .ia-Questions-item:nth-child(' + str(i_question) + ') select > option')
                    stop_o = False
                    for o in options:
                        for preset in self.presets:
                            if preset in q_label and self.presets[preset] in o.get_property('value').lower():
                                o.click()
                                stop_o = True
                                break
                        if stop_o:
                            break
                    if not stop_o:
                        options[len(options)-1].click()
                    time.sleep(1)
                    continue
                # File Field
                q_input = self.driver.find_elements(By.CSS_SELECTOR, '#ia-container .ia-Questions-item:nth-child(' + str(
                    i_question) + ') .ia-SmartApplyCard-headerButton')
                if len(q_input) > 0:
                    continue
                # Text Field
                q_input = self.driver.find_elements(By.CSS_SELECTOR, '#ia-container .ia-Questions-item:nth-child(' + str(i_question) + ') input')
                if len(q_input) > 0 and q_input[0].get_property('value') == "":
                    if q_input[0].get_property('type') == "text":
                        ok = False
                        for preset in self.presets:
                            if preset in q_label and q_input[0].get_property('innerText').lower():
                                q_input[0].send_keys(self.presets['presets'])
                                ok = False
                        if not ok:
                            q_input[0].send_keys("5")
                        continue
                    elif q_input[0].get_property('type') == "file":
                        continue
                    elif q_input[0].get_property('type') == "date":
                        if "naissance" in q_label:
                            q_input[0].send_keys('01'
                                                 '03'
                                                 '2000')
                        else:
                            q_input[0].send_keys('22'
                                                 '04'
                                                 '2023')
                        continue
                    else:
                        q_input[0].send_keys(5)
                        continue
            try:
                self.driver.find_element(By.CSS_SELECTOR, "#ia-container div.ia-BasePage-footer button").click()
                time.sleep(2)
            except:
                pass

    def application(self):
        finish = False
        for i in range(7):
            time.sleep(2)
            self.application_question()
            time.sleep(2)
            if self.application_is_ended() or self.application_has_error():
                finish = True
                break
        if finish:
            return
        # Cover Letter Step
        time.sleep(1)
        tile_step = self.driver.find_elements(By.CSS_SELECTOR, "#ia-container h1")
        if len(tile_step) > 0 and "motiv" in tile_step[0].get_property('innerText'):
            self.driver.find_element(By.CSS_SELECTOR, "#write-cover-letter-selection-card").click()
            time.sleep(2)
            self.driver.find_element(By.CSS_SELECTOR, "#ia-container div.ia-BasePage-footer button").click()
            time.sleep(1)
        # Submit
        time.sleep(3)
        if len(self.driver.find_elements(By.CSS_SELECTOR, "#ia-container .ia-Review")) > 0:
            self.application_end()
            return
        # Finish is not finish
        self.application_close()

    def application_loop(self):
        self.driver.maximize_window()
        # Login
        self.login()
        # loop
        i_page = 0
        while 1 == 1:
            try:
                self.driver.get(f"https://fr.indeed.com/jobs?q={self.inputs['keywords'][random.randint(0, len(self.inputs['keywords']) - 1)]}&l={self.inputs['localization']}")
                time.sleep(3)
                if i_page <= 6:
                    i_page += 1
                for job in self.driver.find_elements(By.CSS_SELECTOR, ".jobCard_mainContent .jobTitle a"):
                    job_title = str(job.get_property('innerText')).lower()
                    ok = False
                    if len(self.setting['inputs']['included_keywords']) == 0:
                        ok = True
                    else:
                        for ik in self.setting['inputs']['included_keywords']:
                            if ik in job_title:
                                ok = True
                    for ek in self.setting['inputs']['excluded_keywords']:
                        if ek in job_title:
                            ok = False
                    if not ok:
                        continue
                    # Close Popup
                    self.close_popup()
                    # Select Job
                    job.click()
                    time.sleep(3)
                    # Begin Easy Apply
                    begin_button = self.driver.find_elements(By.CSS_SELECTOR, "#indeedApplyButton")
                    if len(begin_button) == 0:
                        continue
                    try:
                        begin_button[0].click()
                    except:
                        continue
                    for handle in self.driver.window_handles:
                        self.driver.switch_to.window(handle)
                        time.sleep(2)
                    self.application()
                    time.sleep(2)
                try:
                    self.driver.find_element(By.CSS_SELECTOR, '#jobsearch-JapanPage .jobsearch-LeftPane > nav > div:nth-child(' + str(i_page + 1) + ')').click()
                except:
                    continue
                time.sleep(5)
            except:
                print('FatalError')
                if not self.options['safe_mode']:
                    break
            if not self.options['infinite']:
                break
