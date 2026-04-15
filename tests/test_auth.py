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
        auth_modal.enter_login("565")
        auth_modal.click_password_field()
        time.sleep(1)
        assert "Введіть телефон" in auth_modal.get_login_error_message()

    def test_invalid_email_format_tc010(self):
        home_page = HomePage(self.driver)
        auth_modal = AuthModal(self.driver)
        home_page.open()
        home_page.close_ad_if_present()
        auth_modal.open_login_modal()
        time.sleep(1)
        auth_modal.enter_login("testemail.com")
        auth_modal.click_password_field()
        time.sleep(1)
        assert "Введіть телефон" in auth_modal.get_login_error_message()

    def test_empty_registration_fields_tc011(self):
        home_page = HomePage(self.driver)
        auth_modal = AuthModal(self.driver)
        home_page.open()
        home_page.close_ad_if_present()
        auth_modal.open_login_modal()
        time.sleep(1)
        auth_modal.click_register_link()
        auth_modal.click_register_submit()

        errors = auth_modal.get_all_error_messages()
        assert len(errors) > 0, "БАГ! Помилки не з'явилися"
        assert any("обов'язковим" in err.lower() for err in errors)

    def test_password_length_validation_tc012(self):
        home_page = HomePage(self.driver)
        auth_modal = AuthModal(self.driver)

        home_page.open()
        home_page.close_ad_if_present()

        auth_modal.open_login_modal()
        auth_modal.click_register_link()

        auth_modal.fill_registration_data(
            fname="Денис",
            lname="Тестувальник",
            phone="631234567",
            email="denys_qa_test@gmail.com",
            password="123"
        )

        actual_error = auth_modal.get_login_error_message()

        expected_text = "8 або більше символів"
        assert expected_text.lower() in actual_error.lower(), \
            f"БАГ! Текст про 8 символів не знайдено. Отримали: '{actual_error}'"