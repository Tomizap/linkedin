import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class LinkedIn:
    def __init__(self, config):
        super().__init__()
        if config['options']['DEBUG']:
            print('init Indeed')
        self.setting = config
        self.keywords = config['inputs']['keywords']
        self.options = config['options']
        self.presets = config['presets']
        self.user = self.setting['user']
        self.list_jobs_url = f"https://www.linkedin.com/jobs/search/?keywords={self.setting['inputs']['keywords'][random.randint(0, len(self.setting['inputs']['keywords'])-1)]}&location={self.setting['inputs']['localization']}&f_AL=true"
        options = Options()
        options.add_experimental_option("detach", True)
        if self.options['headless']:
            options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        return

    # ---------------- LOGIN -------------------- #

    def new_driver(self):
        self.driver.close()
        options = Options()
        options.add_experimental_option("detach", True)
        if self.options['headless']:
            options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()

    def find_element(self, selector):
        return self.driver.find_element(By.CSS_SELECTOR, selector)

    def find_elements(self, selector):
        return self.driver.find_elements(By.CSS_SELECTOR, selector)

    # ---------------- LOGIN -------------------- #

    def pass_captcha(self) -> bool:
        time.sleep(40)
        return True

    def is_logged_in(self) -> bool:
        if len(self.find_elements('body div > .authentication-outlet')) > 0:
            return True
        else:
            return False

    def login(self):
        ok = False
        for x in range(10):
            self.driver.get("https://www.linkedin.com")
            for i in range(15):
                try:
                    self.find_element("#session_key").send_keys(self.user['email'])
                    self.find_element("#session_password").send_keys(self.user['password'])
                    time.sleep(3)
                    self.find_element("form .sign-in-form__footer--full-width > button").click()
                    ok = True
                    break
                except:
                    time.sleep(2)
            if ok:
                break
        self.pass_captcha()
        if not self.is_logged_in():
            self.login()

    # ---------------- GENERAL -------------------- #

    def clear_message(self) -> bool:
        pass

    def send_message(self) -> bool:
        pass

    # ---------------- PROSPECTING -------------------- #

    # ---------------- JOB APPLICATION -------------------- #

    def contact_recruiter(self):
        self.clear_message()
        try:
            self.find_element('').click()
            self.find_element('').send_keys(self.setting['options']['message_to_recruiter'])
        except:
            pass

    def application_exit(self):
        if self.options['DEBUG']:
            print('Linkedin: application_exit')
        # Clear Toasts
        for i in range(3):
            time.sleep(1)
            if len(self.find_elements("#artdeco-toasts__wormhole .artdeco-toasts_toasts > *")) > 0:
                self.find_element("#artdeco-toasts__wormhole .artdeco-toasts_toasts .artdeco-toast-item__dismiss").click()
        # Dismiss Modal
        dismiss_button = self.driver.find_elements(By.CSS_SELECTOR, "#artdeco-modal-outlet .artdeco-modal__dismiss")
        if len(dismiss_button) > 0:
            dismiss_button[0].click()
            time.sleep(1)
        confirm_close_button = self.find_elements(".artdeco-modal--layer-confirmation .artdeco-modal__confirm-dialog-btn")
        if len(confirm_close_button) > 0:
            confirm_close_button[0].click()
            time.sleep(2)

    def application_hide(self):
        if self.options['hide_jobs']:
            if self.options['DEBUG']:
                print('Linkedin: application_hide')
            hide_button = self.find_elements(".jobs-search-results-list__list-item--active .job-card-container__action--visible-on-hover > button")
            if len(hide_button) > 0:
                hide_button[0].click()
                time.sleep(2)

    def application_end(self):
        if self.options['DEBUG']:
            print('Linkedin: application_end')
        time.sleep(2)
        for i in range(2):
            submit_button = self.find_elements(".jobs-easy-apply-content footer button.artdeco-button--primary")
            if len(submit_button) > 0:
                submit_button[0].click()
                time.sleep(2)
        self.application_exit()
        if not self.options['hide_jobs']:
            self.application_hide()

    def application_is_ended(self):
        time.sleep(3)
        if len(self.find_elements("#artdeco-modal-outlet .jpac-modal-header")) > 0:
            if self.options['DEBUG']:
                print('Linkedin: application_is_ended')
            self.application_end()
            return True
        else:
            return False

    def application_has_error(self):
        if len(self.find_elements(".jobs-easy-apply-content h3")) == 0 or len(self.find_elements(".artdeco-toasts_toasts .artdeco-toast-item__icon--error")) > 0:
            if self.options['DEBUG']:
                print('Linkedin: application_has_error')
            self.application_exit()
            return True
        else:
            return False

    def application_question(self):
        if self.options['DEBUG']:
            print('Linkedin: application_question')
        for qi in range(1 + len(self.driver.find_elements(By.CSS_SELECTOR, ".jobs-easy-apply-form-section__grouping"))):
            ok = False
            time.sleep(1)
            css_selector = ".jobs-easy-apply-content form > * > * > div:nth-child(" + str(qi + 2) + ") label"
            q_labels = self.driver.find_elements(By.CSS_SELECTOR, css_selector)
            if len(q_labels) == 0:
                continue
            q_label = q_labels[0].get_property('innerText').lower()
            print("q_label: " + q_label)
            # Text Field
            selector = ".jobs-easy-apply-content form > * > * > div:nth-child(" + str(qi + 2) + ") .artdeco-text-input--input"
            q_inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
            if len(q_inputs) > 0:
                print('Text Field')
                if q_inputs[0].get_property('value') == "":
                    for preset in self.presets:
                        if ok:
                            break
                        if preset in q_label:
                            q_inputs[0].send_keys(self.presets[preset])
                            ok = True
                    if not ok:
                        q_inputs[0].send_keys("5")
                continue
            # Select Field
            q_inputs = self.find_elements(".jobs-easy-apply-content form > * > * > div:nth-child(" + str(qi + 2) + ") select")
            if len(q_inputs) > 0:
                print('Select Field')
                q_inputs[0].click()
                options = self.find_elements(".jobs-easy-apply-content form > * > * > div:nth-child(" + str(qi + 2) + ") select option")
                if len(q_inputs) > 0:
                    ok = False
                    for option in options:
                        if ok:
                            continue
                        for preset in self.presets:
                            if preset in q_label and self.presets[preset] in option.get_property('innerText').lower():
                                option.click()
                                ok = True
                                break
                        if ok:
                            break
                    if not ok:
                        for option in options:
                            if "yes" in option.get_property('innerText').lower() or "oui" in option.get_property('innerText').lower():
                                option.click()
                                ok = True
                                break
                    if not ok:
                        options[len(options)-1].click()
                time.sleep(1)
                q_inputs[0].click()
                continue
            # Checkbox Field
            selector = ".jobs-easy-apply-content form > * > * > div:nth-child(" + str(qi + 2) + ") div.fb-text-selectable__option > label"
            q_inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
            if len(q_inputs) > 0:
                print('Checkbox Field')
                q_inputs[0].click()
                continue
        time.sleep(1)
        try:
            self.find_element(".jobs-easy-apply-content footer button.artdeco-button--primary").click()
            time.sleep(3)
        except:
            pass

    def application(self):
        if self.options['DEBUG']:
            print('Linkedin: application')
        if self.application_is_ended():
            return
        for i in range(10):
            self.application_question()
            if self.application_is_ended() or self.application_has_error():
                print("+1 Application")
                return
        time.sleep(2)
        self.application_exit()

    def application_loop(self):
        self.login()
        if self.options['DEBUG']:
            print('Linkedin: application_loop')
        while 1 == 1:
            try:
                self.driver.get(self.list_jobs_url)
                time.sleep(3)
                # Get All Job Card Link
                self.driver.execute_script('document.querySelector("#main > div > div.scaffold-layout__list > div").scroll(0 ,99999)')
                select_job_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".job-card-container a")
                # Begin Loop
                i_jobs = -1
                for select_job_button in select_job_buttons:
                    i_jobs += 1
                    job_title = str(select_job_button.get_property('innerText')).lower()
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
                    # Select Jobs
                    select_job_button.click()
                    time.sleep(3)
                    # Check if Already Applied
                    start_buttons = self.driver.find_elements(By.CLASS_NAME, "jobs-apply-button")
                    if len(start_buttons) == 0:
                        continue
                    else:
                        # Begin Easy Apply
                        self.driver.find_element(By.CSS_SELECTOR, ".jobs-unified-top-card .jobs-apply-button").click()
                        time.sleep(3)
                        self.application()
                try:
                    self.driver.find_element(By.CSS_SELECTOR, ".jobs-search-results-list__pagination li.active + li").click()
                    time.sleep(10)
                except:
                    continue
            except Exception as e:
                print('FatalError: ' + str(e))
                if not self.options['safe_mode']:
                    break
            if not self.options['infinite']:
                break
