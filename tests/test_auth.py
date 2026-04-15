import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.home_page import HomePage
from pages.auth_modal import AuthModal


class TestAuth:
    def setup_method(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()

    def teardown_method(self):
        self.driver.quit()

    def test_invalid_login_format_tc008(self):
        home_page = HomePage(self.driver)
        auth_modal = AuthModal(self.driver)

        home_page.open()
        home_page.close_ad_if_present()

        auth_modal.open_login_modal()
        time.sleep(1)

        invalid_data = "565"
        auth_modal.enter_login(invalid_data)

        auth_modal.click_password_field()
        time.sleep(1)

        actual_error = auth_modal.get_login_error_message()

        expected_error = "Введіть телефон у форматі +380671234567 або електронну пошту"

        assert expected_error in actual_error, \
            f"БАГ! Очікували текст '{expected_error}', але отримали '{actual_error}'"

    def test_invalid_email_format_tc010(self):
        home_page = HomePage(self.driver)
        auth_modal = AuthModal(self.driver)

        home_page.open()
        home_page.close_ad_if_present()

        print("\nКрок 1: Відкриваємо вікно входу...")
        auth_modal.open_login_modal()
        time.sleep(1)

        invalid_data = "testemail.com"
        auth_modal.enter_login(invalid_data)

        auth_modal.click_password_field()
        time.sleep(1)

        actual_error = auth_modal.get_login_error_message()

        expected_error = "Введіть телефон у форматі +380671234567 або електронну пошту"

        assert expected_error in actual_error, \
            f"БАГ! Очікували текст '{expected_error}', але отримали '{actual_error}'"