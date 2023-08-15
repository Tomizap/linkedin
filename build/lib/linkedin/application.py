import time


class application:

    def __init__(self, driver) -> None:
        self.setting = {}
        self.setting['presets'] = {
            "phone": "066577418",
            "name": "tom",
            "nom": "tom",
            "pays": "fr",
            "mail": "zaptom.pro@gmail.com",
            "linkedin": "https://www.linkedin.com/in/tom-zapico/",
        }
        self.driver = driver
        self.data = {}
        return

    def run(self, url=None):
        print('application')
        if url is not None:
            self.driver.get(url)
            url = self.driver.current_url()
        if self.driver.is_attached('div.jobs-apply-button--top-card > button.jobs-apply-button'):
            self.driver.click(
                'div.jobs-apply-button--top-card > button.jobs-apply-button')
        if self.application_is_ended():
            return
        for _ in range(10):
            self.application_question()
            if self.application_is_ended() or self.application_has_error():
                print("+1 Application")
                return
        time.sleep(2)
        self.application_exit()
        return self.data

    # def contact_recruiter(self):
    #     pass

    def application_exit(self):
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

    # def application_hide(self):
    #     if self.options['hide_jobs']:
    #         if self.options['DEBUG']:
    #             print('Linkedin: application_hide')
    #         hide_button = self.driver.find_elements(
    #             ".jobs-search-results-list__list-item--active .job-card-container__action--visible-on-hover > button")
    #         if len(hide_button) > 0:
    #             hide_button[0].click()
    #             time.sleep(2)

    def application_end(self):
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

    def application_is_ended(self):
        time.sleep(3)
        if len(self.driver.find_elements("#artdeco-modal-outlet .jpac-modal-header")) > 0:
            self.application_end()
            return True
        else:
            return False

    def application_has_error(self):
        if len(self.driver.find_elements(".jobs-easy-apply-content h3")) == 0 or len(self.driver.find_elements(".artdeco-toasts_toasts .artdeco-toast-item__icon--error")) > 0:
            self.application_exit()
            return True
        else:
            return False

    def application_question(self):
        for qi in range(1 + len(self.driver.find_elements(".jobs-easy-apply-form-section__grouping"))):
            ok = False
            time.sleep(1)
            css_selector = ".jobs-easy-apply-content form > * > * > div:nth-child(" + str(
                qi + 2) + ") label"
            q_labels = self.driver.find_elements(css_selector)
            if len(q_labels) == 0:
                continue
            q_label = q_labels[0].get_property('innerText').lower()
            # print("q_label: " + q_label)
            # Text Field
            selector = ".jobs-easy-apply-content form > * > * > div:nth-child(" + str(
                qi + 2) + ") .artdeco-text-input--input"
            q_inputs = self.driver.find_elements(selector)
            if len(q_inputs) > 0:
                # print('Text Field')
                if q_inputs[0].get_property('value') == "":
                    for preset in self.setting['presets']:
                        if ok:
                            break
                        if preset in q_label:
                            q_inputs[0].send_keys(
                                self.setting['presets'][preset])
                            ok = True
                    if not ok:
                        q_inputs[0].send_keys("5")
                continue
            # Select Field
            q_inputs = self.driver.find_elements(
                ".jobs-easy-apply-content form > * > * > div:nth-child(" + str(qi + 2) + ") select")
            if len(q_inputs) > 0:
                # print('Select Field')
                q_inputs[0].click()
                options = self.driver.find_elements(
                    ".jobs-easy-apply-content form > * > * > div:nth-child(" + str(qi + 2) + ") select option")
                if len(q_inputs) > 0:
                    ok = False
                    for option in options:
                        if ok:
                            continue
                        for preset in self.setting['presets']:
                            if preset in q_label and self.setting['presets'][preset] in option.get_property('innerText').lower():
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
                # print('Checkbox Field')
                q_inputs[0].click()
                continue
        time.sleep(1)
        try:
            self.driver.find_element(
                ".jobs-easy-apply-content footer button.artdeco-button--primary").click()
            time.sleep(3)
        except:
            pass
