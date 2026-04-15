from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class AuthModal(BasePage):
    ACCOUNT_BTN = (By.CSS_SELECTOR, "button.ui-btn-account")
    LOGIN_INPUT = (By.CSS_SELECTOR, "input#auth-login")
    PASSWORD_INPUT = (By.NAME, "auth_password")
    ERROR_MSG = (By.CSS_SELECTOR, "p.validation-error")

    REGISTER_LINK = (By.XPATH, "//button[contains(@class, 'ui-btn-link') and contains(text(), 'Зареєструватися')]")
    REGISTER_SUBMIT_BTN = (By.ID, "reg-submit")

    def open_login_modal(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ACCOUNT_BTN)
        )
        self.driver.execute_script("arguments[0].click();", btn)

    def enter_login(self, text):
        login_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.LOGIN_INPUT)
        )
        login_field.clear()
        login_field.send_keys(text)

    def click_password_field(self):
        login_field = self.driver.find_element(*self.LOGIN_INPUT)
        login_field.send_keys(Keys.TAB)

    def get_login_error_message(self):
        error_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.ERROR_MSG)
        )
        return error_element.text.strip()

    def click_register_link(self):
        link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.REGISTER_LINK)
        )
        self.driver.execute_script("arguments[0].click();", link)

    def click_register_submit(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.REGISTER_SUBMIT_BTN)
        )
        self.driver.execute_script("arguments[0].click();", btn)

    def get_all_error_messages(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.ERROR_MSG)
            )
        except:
            pass
        elements = self.driver.find_elements(*self.ERROR_MSG)
        return [el.text.strip() for el in elements if el.text.strip() != ""]