import time
from colorama import Fore, Style

from selenium_driver import SeleniumDriver

class LinkedIn:

    def __init__(self, config, driver=None):
        print('init LinkedIn bot')
        self.config = config
        self.driver = SeleniumDriver(headless=False) if driver is None else driver

    # ---------------- JOB APPLICATION -------------------- #

    def accept_cookies(self) -> None:
        self.driver.click('.artdeco-global-alert__action-wrapper > button')

    def login(self) -> bool:
        self.driver.get('https://linkedin.com/')
        time.sleep(1)
        if '/feed' not in self.driver.current_url():
            for cookie in self.config['user']['cookies']:
                # cookie = {'name': cookie.get('name'), 'value': cookie.get('value')}
                self.driver.add_cookie({'name': cookie.get('name'), 'value': cookie.get('value')})
                self.driver.get('https://linkedin.com/')    
        return True

    # ---------------- USER -------------------- #

    def create_user(self):
        pass

    # ---------------- JOB APPLICATION -------------------- #
    
    def application_exit(self) -> None:
        # Clear Toasts
        for _ in range(3):
            time.sleep(1)
            if self.driver.is_attached("#artdeco-toasts__wormhole .artdeco-toasts_toasts > *"):
                self.driver.click(
                    "#artdeco-toasts__wormhole .artdeco-toasts_toasts .artdeco-toast-item__dismiss")
        # Dismiss Modal
        dismiss_button = self.driver.find_elements(
            "#artdeco-modal-outlet .artdeco-modal__dismiss")
        if len(dismiss_button) > 0:
            dismiss_button[0].click()
            time.sleep(1)
        confirm_close_button = self.driver.find_elements(
            ".artdeco-modal--layer-confirmation .artdeco-modal__confirm-dialog-btn")
        if len(confirm_close_button) > 0:
            confirm_close_button[0].click()
            time.sleep(2)

    def application_hide(self) -> None:
        pass

    def application_end(self) -> None:
        time.sleep(2)
        for _ in range(2):
            submit_button = self.driver.find_elements(
                ".jobs-easy-apply-content footer button.artdeco-button--primary")
            if len(submit_button) > 0:
                submit_button[0].click()
                time.sleep(2)
        self.application_exit()
        # if not self.options['hide_jobs']:
        #     self.application_hide()

    def application_is_ended(self) -> bool:
        time.sleep(3)
        if len(self.driver.find_elements("#artdeco-modal-outlet .jpac-modal-header")) > 0:
            self.application_end()
            return True
        else:
            return False

    def application_has_error(self) -> bool:
        if not self.driver.is_attached(".jobs-easy-apply-content h3") or self.driver.is_attached(".artdeco-toasts_toasts .artdeco-toast-item__icon--error, .artdeco-inline-feedback--error"):
            print(Fore.RED + "application_has_error")
            print(Style.RESET_ALL)
            self.application_exit()
            return True
        else:
            return False

    def application_question(self) -> None:
        qn = 1 + len(self.driver.find_elements(".jobs-easy-apply-form-section__grouping"))
        print(f'nb questions: {str(qn)}')

        loop = True
        step_title = self.driver.find_element('.jobs-easy-apply-content form h3').get_attribute('innerText').lower()
        for title in ['resume', 'CV', 'Vérifiez votre candidature']:
            if title in step_title:
                loop = False
                break

        if loop == True:
            for qi in range(qn):
                print(f'question: {str(qi + 1)}')
                ok = False
                time.sleep(1)

                # if self.driver.is_attached('.jobs-easy-apply-modal__content .ui-attachment.jobs-document-upload-redesign-card__container') == True:
                #     continue

                css_selector = ".jobs-easy-apply-content form > * > * > div:nth-child(" + str(
                    qi + 2) + ") label"
                q_labels = self.driver.find_elements(css_selector)
                if len(q_labels) == 0:
                    print(Fore.RED + "No Label")
                    print(Style.RESET_ALL)
                    continue
                q_label = q_labels[0].get_property('innerText').lower()
                
                # Text Field
                selector = ".jobs-easy-apply-content form > * > * > div:nth-child(" + str(
                    qi + 2) + ") .artdeco-text-input--input"
                q_inputs = self.driver.find_elements(selector)
                if len(q_inputs) > 0:
                    print('Text Field')
                    if q_inputs[0].get_property('value') != "":
                        continue
                    for preset in self.config['setting']['presets']:
                        if ok:
                            break
                        if preset in q_label:
                            q_inputs[0].send_keys(
                                self.config['setting']['presets'][preset])
                            ok = True
                    if not ok:
                        q_inputs[0].send_keys("5")
                    continue

                # Select Field
                q_inputs = self.driver.find_elements(
                    ".jobs-easy-apply-content form > * > * > div:nth-child(" + str(qi + 2) + ") select")
                if len(q_inputs) > 0:
                    print('Select Field')
                    if q_inputs[0].get_property('value') != "" and q_inputs[0].get_property('value') != "Select an option":
                        continue
                    q_inputs[0].click()
                    options = self.driver.find_elements(
                        ".jobs-easy-apply-content form > * > * > div:nth-child(" + str(qi + 2) + ") select option")
                    if len(q_inputs) > 0:
                        ok = False
                        for option in options:
                            if ok:
                                continue
                            for preset in self.config['setting']['presets']:
                                if preset in q_label and self.config['setting']['presets'][preset] in option.get_property('innerText').lower():
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
                selector = ".jobs-easy-apply-content form > * > * > div:nth-child(" + str(
                    qi + 2) + ") div.fb-text-selectable__option > label"
                q_inputs = self.driver.find_elements(selector)
                if len(q_inputs) > 0:
                    print('Checkbox Field')
                    q_inputs[0].click()
                    continue
                
                print(Fore.RED + "field type not found")
                print(Style.RESET_ALL)

        time.sleep(1)
        self.driver.click(".jobs-easy-apply-content footer button.artdeco-button--primary")

    def application(self) -> None:
        print('application')

        if not self.driver.click('button.jobs-apply-button'):
            return
            
        if self.application_is_ended():
            return
        
        for _ in range(10):
            self.application_question()
            if self.application_is_ended():
                print(Fore.GREEN + "+1 Application")
                print(Style.RESET_ALL)
                return
            if self.application_has_error():
                break
            
        time.sleep(2)
        self.application_exit()
        print(Fore.RED + "application doesn't finish successfuly")
        print(Style.RESET_ALL)

    def application_loop(self) -> None:
        print('application_loop')
        self.login()

        for url in self.config['urls']:

            self.driver.get(url)
            # time.sleep

            self.accept_cookies()

            i_page = 1
            while True:
                i_page = i_page + 1
                print(i_page)
                time.sleep(2)

                self.driver.execute_script("document.querySelector('.jobs-search-results-list').scroll(0, 9999)")
                
                jobs = self.driver.find_elements('.job-card-container a')
                i_job = -1
                for job in jobs:
                    i_job = i_job + 1

                    ok = True
                    job_title = job.get_attribute('innerText').strip()
                    if job_title is not None:
                        print(job_title)
                        for excluded_keywords in self.config['setting']['excluded_keywords']:
                            if excluded_keywords in job_title:
                                ok = False
                                print(Fore.RED + 'item excluded by keyword')
                                print(Style.RESET_ALL)
                                break
                    else:
                        print(Fore.MAGENTA + 'Impossible to get job_title from listing')
                        print(Style.RESET_ALL)
                    company_title = self.driver.find_element(f'.scaffold-layout__list-container > li:nth-child({i_job + 1}) .job-card-container__primary-description')
                    if company_title is not None:
                        company_title = company_title.get_attribute('innerText').strip()
                        print(company_title)
                        for excluded_company in self.config['setting']['excluded_companies']:
                            if excluded_company in company_title:
                                ok = False
                                print(Fore.RED + 'item excluded by company')
                                print(Style.RESET_ALL)
                                break
                        if not ok:
                            return False
                    else:
                        print(Fore.MAGENTA + 'Impossible to get company_title from listing')
                        print(Style.RESET_ALL)
                    
                    try:
                        job.click()
                    except:
                        continue

                    self.application()

                if not self.driver.click('.artdeco-pagination__indicator.selected'):
                    break

    def application_contact_recruiters(self) -> None:
        pass

